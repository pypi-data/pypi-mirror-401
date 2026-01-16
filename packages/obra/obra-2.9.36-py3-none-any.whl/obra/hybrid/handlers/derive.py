"""Derive handler for Hybrid Orchestrator.

This module handles the DERIVE action from the server. It takes an objective
and derives an implementation plan using the local LLM invocation.

The derivation process:
    1. Receive DeriveRequest with objective and context
    2. Gather local project context (files, structure, etc.)
    3. Invoke LLM to generate plan
    4. Parse structured output into plan items
    5. Return DerivedPlan to report to server

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 1
    - obra/api/protocol.py
    - obra/hybrid/orchestrator.py
"""
# pylint: disable=too-many-instance-attributes,too-many-arguments,too-many-positional-arguments
# pylint: disable=too-many-locals,too-many-branches,too-many-return-statements,too-many-statements
# pylint: disable=duplicate-code,broad-exception-caught,too-few-public-methods

import json
import logging
import re
import sys
import tempfile
from collections.abc import Callable
from pathlib import Path
from time import sleep
from typing import Any

from obra.api.protocol import DeriveRequest
from obra.config.llm import get_project_planning_config, resolve_tier_config
from obra.display import print_info, print_warning
from obra.execution.derivation import (
    EXPLORATION_LOOKBACK_MINUTES,
    WORK_TYPE_KEYWORDS,
    WORK_TYPES_NEEDING_EXPLORATION,
    detect_recent_exploration,
)
from obra.exceptions import ConfigurationError
from obra.hybrid.json_utils import (
    extract_json_payload,
    is_garbage_response,
    unwrap_claude_cli_json,
    unwrap_gemini_cli_json,
)
from obra.hybrid.prompt_enricher import PromptEnricher
from obra.intent.detection import detect_input_type
from obra.intent.models import EnrichmentLevel, InputType, IntentModel
from obra.intent.scaffolded_planner import ScaffoldedPlanner
from obra.llm.cli_runner import invoke_llm_via_cli
from obra.planning.scaffolded_review import ScaffoldedPlanReviewer
from obra.workflow.tiered_resolver import TieredResolver

logger = logging.getLogger(__name__)
RAW_RESPONSE_LOG_PREVIEW = 500


class DeriveHandler:
    """Handler for DERIVE action.

    Derives an implementation plan from the objective using LLM.
    The plan is structured as a list of plan items (tasks/stories).

    ## Architecture Context (ADR-027)

    This handler implements the two-tier prompting architecture where:
    - **Server (Tier 1)**: Generates strategic base prompts with CLIENT_CONTEXT_MARKER
    - **Client (Tier 2)**: Enriches base prompts with local tactical context

    **Implementation Flow**:
    1. Server sends DeriveRequest with base_prompt containing strategic instructions
    2. Client enriches base_prompt via PromptEnricher (adds file structure, git log)
    3. Client invokes LLM with enriched prompt locally
    4. Client reports plan items and raw response back to server

    ## IP Protection

    Strategic prompt engineering (system patterns, quality standards) stays on server.
    This protects Obra's proprietary prompt engineering IP from client-side inspection.

    ## Privacy Protection

    Tactical context (file contents, git messages, errors) never sent to server.
    Only LLM response summary (plan items) is transmitted.

    See: docs/decisions/ADR-027-two-tier-prompting-architecture.md

    Example:
        >>> handler = DeriveHandler(Path("/path/to/project"))
        >>> request = DeriveRequest(objective="Add user authentication")
        >>> result = handler.handle(request)
        >>> print(result["plan_items"])
    """

    def __init__(  # noqa: PLR0913
        self,
        working_dir: Path,
        on_stream: Callable[[str, str], None] | None = None,
        llm_config: dict[str, Any] | None = None,
        log_event: Callable[..., None] | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        monitoring_context: dict[str, Any] | None = None,
        bypass_modes: list[str] | None = None,
        plan_context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize DeriveHandler.

        Args:
            working_dir: Working directory for file access
            on_stream: Optional callback for LLM streaming chunks (S3.T6)
            llm_config: Optional LLM configuration (S4.T2)
            log_event: Optional logger for hybrid events (ISSUE-OBS-002)
            monitoring_context: Optional monitoring context for liveness checks
                (ISSUE-CLI-016/017 fix)
        """
        self._working_dir = working_dir
        self._on_stream = on_stream
        self._llm_config = llm_config or {}
        self._log_event = log_event
        self._trace_id = trace_id
        self._parent_span_id = parent_span_id
        self._monitoring_context = monitoring_context
        self._bypass_modes = bypass_modes or []
        self._plan_context = plan_context
        self._skip_intent = "skip_intent" in self._bypass_modes
        self._review_intent = "review_intent" in self._bypass_modes
        self._force_scaffolded = "scaffolded" in self._bypass_modes
        self._skip_scaffolded = "no_scaffolded" in self._bypass_modes

    def handle(self, request: DeriveRequest) -> dict[str, Any]:
        """Handle DERIVE action.

        Args:
            request: DeriveRequest from server with base_prompt

        Returns:
            Dict with plan_items and raw_response

        Raises:
            ValueError: If request.base_prompt is None (server must provide base_prompt)
        """
        logger.info("Deriving plan for: %s...", request.objective[:50])
        print_info(f"Deriving plan for: {request.objective[:50]}...")

        # Detect and log input type
        input_type = detect_input_type(request.objective)
        logger.info("Detected input type: %s", input_type.value)

        # Generate and save intent if needed (S2.T1)
        intent_content = None
        intent_enrichment: EnrichmentLevel | None = None
        intent_model = None
        if not self._skip_intent and input_type in {InputType.VAGUE_NL, InputType.RICH_NL}:
            intent_content, intent_enrichment, intent_model = self._generate_and_save_intent(
                request.objective, input_type
            )

        # Load active intent for prompt injection (S2.T2)
        if intent_model is None:
            intent_model = self._load_active_intent()
        if intent_content is None and intent_model is not None:
            intent_content = self._format_intent_for_prompt(intent_model)

        scaffolded_run = False
        scaffolded_active = False
        planner = None
        if intent_model is not None:
            planner = ScaffoldedPlanner(
                self._working_dir,
                llm_config=self._llm_config,
                on_stream=self._on_stream,
                log_event=self._log_event,
                trace_id=self._trace_id,
                parent_span_id=self._parent_span_id,
            )
            scaffolded_active = planner.should_run(
                input_type,
                force=self._force_scaffolded,
                skip=self._skip_scaffolded,
            )
            if scaffolded_active:
                try:
                    intent_model, diff_path = planner.run(
                        request.objective,
                        intent_model,
                        interactive=sys.stdin.isatty(),
                    )
                    intent_content = self._format_intent_for_prompt(intent_model)
                    scaffolded_run = True
                    if diff_path and self._on_stream:
                        self._on_stream(
                            "scaffolded_intent",
                            f"diff_path={diff_path}",
                        )
                except Exception as exc:
                    logger.warning("Scaffolded intent enrichment failed: %s", exc)

        # FIX-DERIVE-HANG-001: Skip LLM derivation when intent enrichment failed completely.
        # When enrichment is NONE, the LLM returned garbage and we're using a minimal fallback.
        # Attempting LLM derivation with minimal context is likely to fail or produce poor results.
        # Return composite fallback directly to avoid cascading failures and potential hangs.
        if intent_enrichment == EnrichmentLevel.NONE and not scaffolded_run:
            logger.warning(
                "Skipping LLM derivation due to NONE intent enrichment - using composite fallback"
            )
            print_warning(
                "Intent enrichment failed. Using simplified single-task plan."
            )
            plan_items = self._build_composite_fallback(request.objective)
            plan_items = self._inject_closeout_story(
                plan_items,
                objective=request.objective,
                project_context=request.project_context,
            )
            return {
                "plan_items": plan_items,
                "raw_response": "",
            }

        # Validate base_prompt (server-side prompting required)
        if request.base_prompt is None:
            error_msg = (
                "DeriveRequest.base_prompt is None. Server must provide base prompt (ADR-027)."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        plan_items_reference = getattr(request, "plan_items_reference", [])
        if self._plan_context:
            merged_items = self._merge_plan_context(plan_items_reference, self._plan_context)
            if merged_items:
                merged_items = self._inject_closeout_story(
                    merged_items,
                    objective=request.objective,
                    project_context=request.project_context,
                )
                logger.info("Using local plan context for plan import workflow")
                print_info("Using local plan context from plan file")
                return {
                    "plan_items": merged_items,
                    "raw_response": "",
                }

        work_type = self._detect_work_type(request.objective)
        exploration_state = detect_recent_exploration(
            self._working_dir, lookback_minutes=EXPLORATION_LOOKBACK_MINUTES
        )
        self._maybe_nudge_exploration(work_type, exploration_state)

        # Enrich base prompt with local tactical context and intent (S2.T2)
        enricher = PromptEnricher(self._working_dir)
        enriched_prompt = enricher.enrich(request.base_prompt, intent=intent_content)

        stage_timeout_s = None
        max_passes = None
        if scaffolded_active and planner is not None:
            stage_config = planner.get_stage_config("derive")
            provider, model, thinking_level, auth_method, max_passes, stage_timeout_s = (
                self._resolve_scaffolded_stage_llm(stage_config, request.llm_provider)
            )
        else:
            provider, model, thinking_level, auth_method = self._resolve_llm_config(
                request.llm_provider
            )

        if max_passes is not None:
            max_garbage_retries = max(0, int(max_passes) - 1)
        else:
            max_garbage_retries = 2
        garbage_attempt = 0
        plan_items: list[dict[str, Any]] = []
        parse_info: dict[str, Any] = {}
        raw_response = ""

        while True:
            raw_response = self._invoke_llm(
                enriched_prompt,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                auth_method=auth_method,
                timeout_s=stage_timeout_s,
            )

            retry_on_garbage = garbage_attempt < max_garbage_retries
            plan_items, parse_info = self._parse_plan(
                raw_response,
                provider=provider,
                objective=request.objective,
                retry_on_garbage=retry_on_garbage,
            )
            plan_items = self._sanitize_plan_items(plan_items)
            parse_info["garbage_retry_attempt"] = garbage_attempt
            self._log_parse_event(
                action="derive",
                provider=provider,
                model=model,
                parse_info=parse_info,
            )

            if (
                parse_info.get("status") in {"garbage_response", "empty_response"}
                and retry_on_garbage
            ):
                self._log_retry_event(
                    action="derive",
                    provider=provider,
                    model=model,
                    attempt=garbage_attempt + 1,
                    reason=parse_info.get("status", "unknown"),
                )
                sleep(2**garbage_attempt)
                garbage_attempt += 1
                continue

            break

        if scaffolded_active and intent_content:
            reviewer = ScaffoldedPlanReviewer(
                self._working_dir,
                llm_config=self._llm_config,
                on_stream=self._on_stream,
                log_event=self._log_event,
                trace_id=self._trace_id,
                parent_span_id=self._parent_span_id,
            )
            try:
                review_result = reviewer.review(
                    request.objective,
                    intent_markdown=intent_content,
                    plan_items=plan_items,
                    intent_id=intent_model.id if intent_model else None,
                )
                if review_result and review_result.changes_required:
                    if review_result.plan_items:
                        plan_items = self._sanitize_plan_items(review_result.plan_items)
                    else:
                        logger.warning(
                            "Scaffolded review requested changes but returned no plan items"
                        )
            except Exception as exc:
                logger.warning("Scaffolded review failed: %s", exc)

        plan_items = self._inject_closeout_story(
            plan_items,
            objective=request.objective,
            project_context=request.project_context,
        )

        logger.info("Derived %s plan items", len(plan_items))
        print_info(f"Derived {len(plan_items)} plan items")

        return {
            "plan_items": plan_items,
            "raw_response": raw_response,
        }

    def _generate_and_save_intent(
        self,
        objective: str,
        input_type: InputType,
    ) -> tuple[str | None, EnrichmentLevel | None, IntentModel | None]:
        """Generate and save intent for the objective.

        Args:
            objective: User objective
            input_type: Detected input type

        Returns:
            Tuple of (intent_content, enrichment_level, intent_model):
            - intent_content: Intent content as string, or None if generation failed
            - enrichment_level: EnrichmentLevel indicating intent quality
            - intent_model: IntentModel instance if generated
        """
        from obra.hybrid.handlers.intent import IntentHandler  # noqa: PLC0415
        from obra.intent.storage import IntentStorage  # noqa: PLC0415

        try:
            # Get project identifier
            storage = IntentStorage()
            project = storage.get_project_id(self._working_dir)

            # Generate intent
            intent_handler = IntentHandler(
                working_dir=self._working_dir,
                project=project,
                on_stream=self._on_stream,
                llm_config=self._llm_config,
                log_event=self._log_event,
                trace_id=self._trace_id,
                parent_span_id=self._parent_span_id,
            )

            logger.info("Generating intent for objective (type: %s)", input_type.value)
            print_info("Generating intent for objective...")

            intent = intent_handler.generate(objective, input_type=input_type)

            # Save intent
            intent_path = storage.save(intent)
            logger.info("Saved intent to %s", intent_path)
            print_info(f"Intent saved: {intent.id}")

            # S3.T3: Stream enrichment level and intent path to operator
            enrichment_level = intent.enrichment_level
            if enrichment_level and self._on_stream:
                self._on_stream(
                    "intent_enrichment",
                    f"enrichment_level={enrichment_level.value}, path={intent_path}",
                )
            if self._log_event:
                self._log_event(
                    "intent_generated",
                    session_id=None,
                    trace_id=self._trace_id,
                    parent_span_id=self._parent_span_id,
                    intent_id=intent.id,
                    enrichment_level=enrichment_level.value if enrichment_level else "none",
                    intent_path=str(intent_path),
                )

            # S3.T4: Validate intent before derivation
            self._validate_intent_enrichment(intent)

            # S2.T4: Review intent if requested
            if self._review_intent:
                if not self._prompt_intent_approval(intent):
                    logger.info("Intent not approved, aborting derive")
                    raise ValueError("Intent review: User declined to proceed")

            # Return content for prompt injection with enrichment level
            return self._format_intent_for_prompt(intent), enrichment_level, intent

        except Exception as e:
            logger.warning("Failed to generate intent, continuing with derive: %s", e)
            return None, None, None

    def _load_active_intent(self) -> IntentModel | None:
        """Load the active intent model for the current project."""
        from obra.intent.storage import IntentStorage  # noqa: PLC0415

        try:
            storage = IntentStorage()
            project = storage.get_project_id(self._working_dir)
            intent = storage.load_active(project)
            if intent:
                logger.debug("Loaded active intent: %s", intent.id)
                return intent
        except Exception as e:
            logger.debug("Failed to load active intent: %s", e)
        return None

    def _load_active_intent_content(self) -> str | None:
        """Load the active intent content for prompt injection.

        Returns:
            Intent content as string, or None if no active intent
        """
        intent = self._load_active_intent()
        if not intent:
            return None
        return self._format_intent_for_prompt(intent)

    def _validate_intent_enrichment(self, intent: Any) -> None:
        """Validate intent enrichment level and warn if incomplete.

        S3.T4: Validates intent before derivation proceeds. Issues warnings
        for stub/incomplete intents (NONE enrichment) or partial intents
        (PROSE enrichment).

        Args:
            intent: IntentModel instance to validate
        """
        enrichment_level = intent.enrichment_level

        if enrichment_level == EnrichmentLevel.NONE:
            # Stub/fallback intent - minimal enrichment
            logger.warning(
                "Intent has minimal enrichment (NONE) - derivation may be incomplete. "
                "Consider providing a more detailed objective."
            )
            print_warning(
                "Intent enrichment: minimal (using fallback). "
                "Consider providing more details in your objective."
            )
        elif enrichment_level == EnrichmentLevel.PROSE:
            # Prose extraction - partial enrichment
            logger.info(
                "Intent extracted from prose response. "
                "Some structured fields may be incomplete."
            )
            print_info(
                "Intent enrichment: extracted from prose. "
                "Structured requirements may need manual refinement."
            )
        elif enrichment_level == EnrichmentLevel.FULL:
            # Full structured JSON - complete enrichment
            logger.debug("Intent has full enrichment from structured response")
        elif enrichment_level is None:
            # Legacy intent without enrichment level
            logger.debug("Intent has no enrichment level metadata (pre-S3 intent)")

    def _format_intent_for_prompt(self, intent: Any) -> str:
        """Format intent model for prompt injection.

        Args:
            intent: IntentModel instance

        Returns:
            Formatted intent content
        """
        sections = []

        sections.append(f"# Intent: {intent.problem_statement}")
        sections.append("")

        if intent.assumptions:
            sections.append("## Assumptions")
            for assumption in intent.assumptions:
                sections.append(f"- {assumption}")
            sections.append("")

        if intent.requirements:
            sections.append("## Requirements")
            for req in intent.requirements:
                sections.append(f"- {req}")
            sections.append("")

        if intent.constraints:
            sections.append("## Constraints")
            for constraint in intent.constraints:
                sections.append(f"- {constraint}")
            sections.append("")

        if intent.acceptance_criteria:
            sections.append("## Acceptance Criteria")
            for criterion in intent.acceptance_criteria:
                sections.append(f"- {criterion}")
            sections.append("")

        if intent.non_goals:
            sections.append("## Non-Goals")
            for non_goal in intent.non_goals:
                sections.append(f"- {non_goal}")
            sections.append("")

        if intent.risks:
            sections.append("## Risks")
            for risk in intent.risks:
                sections.append(f"- {risk}")
            sections.append("")

        if intent.context_amendments:
            sections.append("## Context Amendments")
            for amendment in intent.context_amendments:
                sections.append(f"- {amendment}")
            sections.append("")

        return "\n".join(sections)

    def _prompt_intent_approval(self, intent: Any) -> bool:
        """Display intent and prompt user for approval (S2.T4).

        Args:
            intent: IntentModel instance

        Returns:
            True if user approves, False otherwise
        """
        from obra.display import print_info  # noqa: PLC0415

        # Display intent
        print_info("\n=== Generated Intent ===\n")
        content = self._format_intent_for_prompt(intent)
        print_info(content)
        print_info("\n" + "="*50 + "\n")

        # Prompt for approval
        print_info("Proceed with this intent? [Y/n]: ", end="")
        try:
            response = input().strip().lower()
            return response in {"", "y", "yes"}
        except (EOFError, KeyboardInterrupt):
            return False

    def _detect_work_type(self, objective: str) -> str:
        """Classify the objective into a coarse work type."""
        lowered = objective.lower()
        for work_type, keywords in WORK_TYPE_KEYWORDS.items():
            if any(keyword in lowered for keyword in keywords):
                return str(work_type)
        return "general"

    def _maybe_nudge_exploration(self, work_type: str, exploration_state: dict[str, Any]) -> None:
        """Emit a nudge to explore first when appropriate."""
        if work_type not in WORK_TYPES_NEEDING_EXPLORATION:
            return

        if exploration_state.get("recent_exploration"):
            return

        message = (
            "Consider exploring the codebase first for better results "
            "(Plan Mode or Explore agent)."
        )
        print_warning(message)
        if self._log_event:
            try:
                self._log_event(
                    "exploration_nudge",
                    work_type=work_type,
                    recent_exploration=False,
                    signals=exploration_state.get("signals", []),
                    trace_id=self._trace_id,
                    parent_span_id=self._parent_span_id,
                )
            except TypeError:
                # Be defensive against legacy loggers with narrower signatures
                logger.debug("Exploration nudge logging skipped: incompatible log_event signature")

    def _merge_plan_context(
        self,
        plan_items_reference: list[dict[str, Any]],
        plan_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Merge server plan metadata with local plan context.

        Local context takes precedence, ensuring YAML tasks stay client-side.
        """
        stories = plan_context.get("stories")
        if not isinstance(stories, list) or not stories:
            return []

        story_map: dict[str, dict[str, Any]] = {}
        ordered_story_ids: list[str] = []
        for story in stories:
            if not isinstance(story, dict):
                continue
            story_id = story.get("id")
            if not isinstance(story_id, str):
                continue
            story_map[story_id] = story
            ordered_story_ids.append(story_id)

        base_items = plan_items_reference or []
        if not base_items:
            base_items = []
            for story_id in ordered_story_ids:
                story = story_map[story_id]
                base_items.append(
                    {
                        "id": story_id,
                        "item_type": story.get("item_type", "story"),
                        "title": story.get("title", story.get("desc", "Untitled")),
                        "description": (
                            story.get("description")
                            or story.get("title")
                            or story.get("desc", "Untitled")
                        ),
                        "acceptance_criteria": story.get("verify", []),
                        "dependencies": story.get("depends_on", []),
                        "context": {},
                    }
                )

        merged_items: list[dict[str, Any]] = []
        for item in base_items:
            merged_item = dict(item)
            base_context = item.get("context") or {}
            story = story_map.get(item.get("id"))
            if story:
                story_context: dict[str, Any] = {}
                if isinstance(story.get("context"), dict):
                    story_context.update(story["context"])
                if "tasks" in story:
                    story_context["tasks"] = story.get("tasks", [])
                if story.get("guidance"):
                    story_context["guidance"] = story["guidance"]
                if story.get("constraints"):
                    story_context["constraints"] = story["constraints"]
                if story.get("status"):
                    story_context["status"] = story["status"]
                merged_item["context"] = {**base_context, **story_context}
            else:
                merged_item["context"] = base_context

            merged_items.append(merged_item)

        return self._sanitize_plan_items(merged_items)

    def _sanitize_plan_items(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Ensure plan items conform to server schema.

        Coerces item_type to allowed enum, drops unknown keys, and fills required fields
        with safe defaults to avoid server-side validation failures.
        """
        allowed_item_types = {"task", "subtask", "milestone"}
        sanitized: list[dict[str, Any]] = []

        for idx, item in enumerate(items):
            item_type = item.get("item_type", "task")
            if item_type not in allowed_item_types:
                item_type = "task"

            title = item.get("title", "Untitled")
            description = item.get("description") or title
            context = item.get("context") or {}
            dependencies = item.get("dependencies", [])
            if not isinstance(dependencies, list):
                dependencies = [dependencies]

            sanitized.append(
                {
                    "id": item.get("id", f"T{idx + 1}"),
                    "item_type": item_type,
                    "title": title,
                    "description": description,
                    "acceptance_criteria": item.get("acceptance_criteria", []),
                    "dependencies": dependencies,
                    "context": context,
                }
            )

        return sanitized

    def _inject_closeout_story(
        self,
        plan_items: list[dict[str, Any]],
        *,
        objective: str,
        project_context: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Append close-out story tasks resolved from tiered templates."""
        if "no_closeout" in self._bypass_modes:
            logger.info("Skipping close-out injection due to no_closeout bypass mode")
            return plan_items

        resolution = self._resolve_closeout_template(project_context)
        if not resolution:
            return plan_items

        closeout_context = self._build_closeout_context(objective, project_context)
        story_id = self._next_story_id(plan_items)
        injected: list[dict[str, Any]] = []
        task_index = 0

        for task in resolution.template.tasks:
            if task.conditional and not self._evaluate_closeout_condition(
                task.conditional, closeout_context
            ):
                continue

            injected.append(
                {
                    "id": f"{story_id}.T{task_index}",
                    "item_type": "task",
                    "title": task.desc,
                    "description": task.desc,
                    "acceptance_criteria": [task.verify],
                    "dependencies": [],
                    "context": {
                        "closeout_domain": resolution.template.domain,
                        "template_source_tiers": resolution.source_tiers,
                        "conditional": task.conditional,
                    },
                }
            )
            task_index += 1

        if not injected:
            logger.info("No close-out tasks added after conditional evaluation")
            return plan_items

        logger.info(
            "Injected %d close-out tasks from %s template (tiers: %s)",
            len(injected),
            resolution.template.domain,
            ", ".join(resolution.source_tiers),
        )
        return plan_items + injected

    def _resolve_closeout_template(self, project_context: dict[str, Any]) -> Any | None:
        """Resolve close-out template using TieredResolver."""
        try:
            project_path = Path(project_context.get("repo_root", self._working_dir))
        except TypeError:
            project_path = self._working_dir

        domain = project_context.get("domain")
        if not domain:
            planning_config = get_project_planning_config(project_path)
            domain = planning_config.get("domain")
        if not domain:
            domain = "software-dev"

        obra_root = self._get_obra_root()
        resolver = TieredResolver(project_path=project_path, obra_path=obra_root)
        return resolver.resolve_closeout(domain)

    def _build_closeout_context(
        self, objective: str, project_context: dict[str, Any]
    ) -> dict[str, Any]:
        """Build context for evaluating close-out conditionals."""
        work_type = self._detect_work_type(objective)

        has_user_facing_changes = project_context.get("has_user_facing_changes")
        if has_user_facing_changes is None:
            has_user_facing_changes = work_type not in ("refactoring",)

        type_checks_enabled = project_context.get("type_checks_enabled")
        if type_checks_enabled is None:
            type_checks_enabled = self._is_type_checks_enabled()

        planning_config = get_project_planning_config(self._working_dir)
        domain = (
            project_context.get("domain")
            or planning_config.get("domain")
            or "software-dev"
        )

        return {
            "work_type": work_type,
            "has_user_facing_changes": bool(has_user_facing_changes),
            "type_checks_enabled": bool(type_checks_enabled),
            "domain": domain,
        }

    def _evaluate_closeout_condition(self, condition: str, context: dict[str, Any]) -> bool:
        """Evaluate conditional flags for close-out tasks."""
        condition_map = {
            "type_checks_enabled": bool(context.get("type_checks_enabled")),
            "has_user_facing_changes": bool(context.get("has_user_facing_changes")),
        }
        if condition not in condition_map:
            logger.debug("Unknown close-out condition '%s' - defaulting to include", condition)
            return True
        return condition_map[condition]

    def _is_type_checks_enabled(self) -> bool:
        """Detect whether type checks are configured for the project."""
        candidates = [
            self._working_dir / "mypy.ini",
            self._working_dir / "setup.cfg",
            self._working_dir / "pyproject.toml",
        ]

        for path in candidates:
            if not path.exists():
                continue
            if path.name in {"pyproject.toml", "setup.cfg"}:
                try:
                    content = path.read_text(encoding="utf-8")
                    if "tool.mypy" in content or "[mypy]" in content:
                        return True
                except OSError:
                    continue
            else:
                return True

        return False

    def _next_story_id(self, plan_items: list[dict[str, Any]]) -> str:
        """Compute the next sequential story ID based on existing items."""
        max_story = 0
        pattern = re.compile(r"^S(?P<story>\d+)")

        for item in plan_items:
            item_id = str(item.get("id", ""))
            match = pattern.match(item_id)
            if match:
                try:
                    story_num = int(match.group("story"))
                except ValueError:
                    continue
                max_story = max(max_story, story_num)

        return f"S{max_story + 1}"

    def _get_obra_root(self) -> Path:
        """Resolve repository root for bundled templates."""
        return Path(__file__).resolve().parents[3]

    def _invoke_llm(
        self,
        prompt: str,
        *,
        provider: str,
        model: str,
        thinking_level: str,
        auth_method: str = "oauth",
        timeout_s: int | None = None,
    ) -> str:
        """Invoke LLM to generate plan.

        Args:
            prompt: Derivation prompt
            provider: LLM provider name
            model: LLM model name
            thinking_level: LLM thinking level
            auth_method: Authentication method ("oauth" or "api_key")

        Returns:
            Raw LLM response
        """
        logger.debug(
            "Invoking LLM via CLI: provider=%s model=%s thinking=%s auth=%s",
            provider,
            model,
            thinking_level,
            auth_method,
        )

        def _stream(chunk: str) -> None:
            if self._on_stream:
                self._on_stream("llm_streaming", chunk)

        try:
            schema_path = None
            if provider == "openai":
                schema = {
                    "type": "object",
                    "properties": {
                        "plan_items": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "item_type": {"type": "string"},
                                    "title": {"type": "string"},
                                    "description": {"type": "string"},
                                    "acceptance_criteria": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "dependencies": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                                "required": [
                                    "id",
                                    "item_type",
                                    "title",
                                    "description",
                                    "acceptance_criteria",
                                    "dependencies",
                                ],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["plan_items"],
                    "additionalProperties": False,
                }
                with tempfile.NamedTemporaryFile(
                    mode="w+",
                    delete=False,
                    encoding="utf-8",
                ) as schema_file:
                    json.dump(schema, schema_file)
                    schema_path = Path(schema_file.name)
            try:
                return str(
                    invoke_llm_via_cli(
                        prompt=prompt,
                        cwd=self._working_dir,
                        provider=provider,
                        model=model,
                        thinking_level=thinking_level,
                        auth_method=auth_method,
                        on_stream=_stream if self._on_stream else None,
                        timeout_s=timeout_s,
                        output_schema=schema_path,
                        log_event=self._log_event,
                        trace_id=self._trace_id,
                        parent_span_id=self._parent_span_id,
                        call_site="derive",
                        monitoring_context=self._monitoring_context,  # ISSUE-CLI-016/017 fix
                        skip_git_check=self._llm_config.get("git", {}).get("skip_check", False),  # GIT-HARD-001
                    )
                )
            finally:
                if schema_path:
                    schema_path.unlink(missing_ok=True)
        except Exception as e:
            logger.exception("LLM invocation failed")
            return json.dumps(
                {
                    "plan_items": [
                        {
                            "id": "ERROR",
                            "item_type": "task",
                            "title": "LLM Error",
                            "description": f"LLM invocation failed: {e!s}",
                            "acceptance_criteria": [],
                            "dependencies": [],
                        }
                    ]
                }
            )

    def _parse_plan(  # noqa: PLR0912,PLR0915
        self,
        raw_response: str,
        *,
        provider: str | None = None,
        objective: str | None = None,
        retry_on_garbage: bool = False,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Parse LLM response into plan items.

        Args:
            raw_response: Raw LLM response
            provider: Optional provider name for debugging (FIX-GEMINI-UNWRAP-001)
            objective: Current objective for composite fallback construction
            retry_on_garbage: Skip extraction and allow caller to retry on garbage/empty

        Returns:
            List of plan item dictionaries

        Note:
            ISSUE-SAAS-018 fix: Now tries multiple key names that LLMs commonly use
            (plan_items, tasks, items, plan, stories) before falling back to
            wrapping as single item.
        """
        parse_info: dict[str, Any] = {
            "status": "strict_json",
            "response_length": len(raw_response),
            "used_extraction": False,
            "extraction_attempted": False,
            "extraction_succeeded": False,
        }
        normalized: list[dict[str, Any]] = []
        # FIX-GEMINI-UNWRAP-001: Add provider to parse_info for debugging
        if provider:
            parse_info["provider"] = provider

        # FIX-GEMINI-UNWRAP-001: Debug logging for raw LLM response
        # Helps diagnose parsing issues with different providers
        if raw_response:
            truncated = (
                raw_response[:RAW_RESPONSE_LOG_PREVIEW] + "..."
                if len(raw_response) > RAW_RESPONSE_LOG_PREVIEW
                else raw_response
            )
            logger.debug(
                "Raw LLM response (first %s chars): %s", RAW_RESPONSE_LOG_PREVIEW, truncated
            )

        trimmed_response = raw_response.strip()
        if not trimmed_response:
            parse_info["status"] = "empty_response"
            if retry_on_garbage:
                return [], parse_info
            return self._fallback_with_extraction(raw_response, parse_info, objective)

        is_garbage, garbage_reason = is_garbage_response(trimmed_response, return_reason=True)
        if is_garbage:
            parse_info["status"] = "garbage_response"
            parse_info["garbage_reason"] = garbage_reason
            logger.warning(
                "Detected garbage response in derivation (reason=%s). Preview: %s",
                garbage_reason,
                trimmed_response[:200],
            )
            if retry_on_garbage:
                return [], parse_info
            return self._fallback_with_extraction(raw_response, parse_info, objective)

        try:
            # Try to extract JSON from response
            # Handle case where response might have markdown code blocks
            response = trimmed_response

            if response.startswith("```"):
                # Extract from code block
                lines = response.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1] == "```" else len(lines)
                response = "\n".join(lines[start:end])

            # Parse JSON
            try:
                data = json.loads(response)
            except json.JSONDecodeError as e:
                candidate = extract_json_payload(raw_response)
                if candidate and candidate != response:
                    parse_info["status"] = "tolerant_json"
                    parse_info["used_extraction"] = True
                    data = json.loads(candidate)
                else:
                    parse_info["status"] = "parse_error"
                    parse_info["error"] = str(e)
                    return self._fallback_with_extraction(raw_response, parse_info, objective)

            # ISSUE-SAAS-030 FIX: Handle Claude CLI JSON wrapper format
            # When --output-format json is used, Claude CLI wraps the response
            data, was_unwrapped = unwrap_claude_cli_json(data)
            if was_unwrapped:
                logger.debug("Detected Claude CLI JSON wrapper, extracted result field")
                parse_info["unwrapped_cli_json"] = True
                # If unwrap returned a string (not JSON), coerce to single task
                if isinstance(data, str):
                    logger.warning(
                        "Claude CLI result is not valid JSON; attempting extraction fallback."
                    )
                    parse_info["status"] = "parse_error"
                    return self._fallback_with_extraction(data, parse_info, objective)

            # FIX-GEMINI-UNWRAP-001: Handle Gemini CLI JSON wrapper format
            # When Gemini CLI is used, it wraps the response as {"response": "...", "stats": {...}}
            data, was_gemini_unwrapped = unwrap_gemini_cli_json(data)
            if was_gemini_unwrapped:
                logger.debug("Detected Gemini CLI JSON wrapper, extracted response field")
                parse_info["unwrapped_gemini_json"] = True
                # If unwrap returned a string (not JSON), coerce to single task
                if isinstance(data, str):
                    logger.warning(
                        "Gemini CLI response is not valid JSON; coercing to single task."
                    )
                    parse_info["status"] = "parse_error"
                    return self._fallback_with_extraction(data, parse_info, objective)

            # ISSUE-SAAS-018: Try multiple common key names LLMs might use
            items = None
            if isinstance(data, dict):
                # Try common key names in order of preference
                for key in ["plan_items", "tasks", "items", "plan", "stories"]:
                    if key in data and isinstance(data[key], list):
                        items = data[key]
                        if key != "plan_items":
                            logger.info(
                                "Found plan items under '%s' key instead of 'plan_items'",
                                key,
                            )
                        break

                if items is None:
                    logger.info("Unexpected response format, wrapping as single item")
                    items = [data]
            elif isinstance(data, list):
                items = data
            else:
                logger.warning(
                    "Unexpected response format (not dict or list), wrapping as single item"
                )
                items = [{"description": str(data)}]

            # Validate and normalize items
            for i, item in enumerate(items):
                title = item.get("title", "Untitled")
                # ISSUE-SAAS-047 FIX: Use title as fallback when description is
                # empty or missing. Gemini and other LLMs sometimes return empty
                # descriptions, causing server-side validation to fail
                # (min_length=1 for description field).
                description = item.get("description", "")
                if not description:  # Empty string or missing
                    description = title
                normalized_item = {
                    "id": item.get("id", f"T{i + 1}"),
                    "item_type": item.get("item_type", "task"),
                    "title": title,
                    "description": description,
                    "acceptance_criteria": item.get("acceptance_criteria", []),
                    "dependencies": item.get("dependencies", []),
                }
                normalized.append(normalized_item)

        except json.JSONDecodeError as e:
            parse_info["status"] = "parse_error"
            parse_info["error"] = str(e)
            return self._fallback_with_extraction(raw_response, parse_info, objective)
        return normalized, parse_info

    def _fallback_with_extraction(
        self,
        raw_response: str,  # noqa: ARG002 - kept for signature compatibility
        parse_info: dict[str, Any],
        objective: str | None,
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Return composite fallback task when JSON parsing fails.

        FIX-DERIVE-HANG-001: Removed LLM extraction fallback.

        Previously this method attempted LLM-based structure extraction using a
        "fast" tier model, which could hang for up to 600s (default timeout).
        The extraction had low success probability since it used a weaker model
        to extract structure from a response that a better model failed to produce.

        Now returns composite fallback directly - deterministic, instant, no network call.
        The composite fallback (single task with objective) works well for LLM agents
        who can decompose during execution.
        """
        # Log that we're using composite fallback (for observability)
        parse_info["extraction_attempted"] = False
        parse_info["extraction_succeeded"] = False
        parse_info["status"] = "composite_fallback"

        logger.info("JSON parsing failed - using composite fallback (extraction disabled)")
        return self._build_composite_fallback(objective), parse_info

    def _build_composite_fallback(self, objective: str | None) -> list[dict[str, Any]]:
        """Return a single composite task when structure recovery fails."""
        objective_text = (objective or "").strip() or "Implement the requested objective"
        return [
            {
                "id": "T1",
                "item_type": "task",
                "title": "Implement objective",
                "description": objective_text,
                "acceptance_criteria": [
                    "Objective is implemented end-to-end",
                    "Quality gates (tests, lint, type checks) updated as needed",
                ],
                "dependencies": [],
            }
        ]

    def _resolve_llm_config(self, provider: str) -> tuple[str, str, str, str]:
        """Resolve LLM configuration from stored config.

        Returns:
            Tuple of (provider, model, thinking_level, auth_method)
        """
        resolved_provider = self._llm_config.get("provider", provider)
        model = self._llm_config.get("model", "default")
        thinking_level = self._llm_config.get("thinking_level", "medium")
        auth_method = self._llm_config.get("auth_method", "oauth")
        return resolved_provider, model, thinking_level, auth_method

    def _resolve_scaffolded_stage_llm(
        self,
        stage_config: dict[str, Any],
        provider: str,
    ) -> tuple[str, str, str, str, int, int]:
        model_tier = stage_config.get("model_tier")
        if not model_tier:
            raise ConfigurationError(
                "planning.scaffolded.stages.derive.model_tier is required",
                "Set model_tier for the derive stage in config.",
            )
        if "reasoning_level" not in stage_config:
            raise ConfigurationError(
                "planning.scaffolded.stages.derive.reasoning_level is required",
                "Set reasoning_level for the derive stage in config.",
            )
        if "max_passes" not in stage_config:
            raise ConfigurationError(
                "planning.scaffolded.stages.derive.max_passes is required",
                "Set max_passes for the derive stage in config.",
            )
        if "timeout_s" not in stage_config:
            raise ConfigurationError(
                "planning.scaffolded.stages.derive.timeout_s is required",
                "Set timeout_s for the derive stage in config.",
            )
        resolved = resolve_tier_config(
            model_tier,
            role="implementation",
            override_thinking_level=stage_config.get("reasoning_level"),
        )
        max_passes = int(stage_config.get("max_passes"))
        timeout_s = int(stage_config.get("timeout_s"))
        return (
            resolved.get("provider", provider),
            resolved["model"],
            resolved["thinking_level"],
            resolved["auth_method"],
            max_passes,
            timeout_s,
        )

    def _log_parse_event(
        self,
        *,
        action: str,
        provider: str,
        model: str,
        parse_info: dict[str, Any],
    ) -> None:
        if not self._log_event:
            return
        try:
            self._log_event(
                "hybrid_parse_result",
                action=action,
                provider=provider,
                model=model,
                status=parse_info.get("status"),
                used_extraction=parse_info.get("used_extraction", False),
                extraction_attempted=parse_info.get("extraction_attempted", False),
                extraction_succeeded=parse_info.get("extraction_succeeded", False),
                retried=parse_info.get("retried", False),
                response_length=parse_info.get("response_length", 0),
            )
        except Exception as e:
            logger.debug("Failed to log hybrid parse event: %s", e)

    def _log_retry_event(
        self,
        *,
        action: str,
        provider: str,
        model: str,
        attempt: int,
        reason: str,
    ) -> None:
        if not self._log_event:
            return
        try:
            self._log_event(
                "hybrid_parse_retry",
                action=action,
                provider=provider,
                model=model,
                attempt=attempt,
                reason=reason,
            )
        except Exception as e:
            logger.debug("Failed to log hybrid retry event: %s", e)


__all__ = ["DeriveHandler"]
