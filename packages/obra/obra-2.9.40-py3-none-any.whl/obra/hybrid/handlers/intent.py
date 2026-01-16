"""Intent generation handler for Hybrid Orchestrator.

This module handles intent generation from user objectives using LLM.
It classifies the input type and generates a structured intent with
problem statement, assumptions, requirements, acceptance criteria, and non-goals.

The intent generation process:
    1. Classify input type (vague_nl, rich_nl, prd, prose_plan, structured_plan)
    2. For vague inputs: invoke LLM to expand into structured intent
    3. For rich inputs: parse directly or use LLM for extraction
    4. Return IntentModel with all required fields

Architecture (ADR-027):
    - Client-side LLM invocation (privacy-preserving)
    - Two-tier prompting: strategic prompts can come from server or local templates
    - Intent stored locally in ~/.obra/intents/{project}/

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - docs/decisions/ADR-027-two-tier-prompting-architecture.md
    - obra/intent/models.py
    - obra/intent/storage.py
"""

import json
import logging
import re
import time
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from obra.hybrid.json_utils import extract_json_payload, is_garbage_response
from obra.intent.detection import detect_input_type
from obra.intent.models import EnrichmentLevel, InputType, IntentModel
from obra.llm.cli_runner import invoke_llm_via_cli

# Threshold for classifying a response as predominantly interrogative (questions vs statements)
# If ratio of questions to total sentences exceeds this, response is likely non-compliant
INTERROGATIVE_RATIO_THRESHOLD = 0.5

# Rate limit retry configuration (SIM-FIX-001 S1.T0)
RATE_LIMIT_MAX_RETRIES = 3
RATE_LIMIT_BACKOFF_DELAYS = [2.0, 4.0, 8.0]  # Exponential backoff in seconds

logger = logging.getLogger(__name__)


class IntentHandler:
    """Handler for intent generation from user objectives.

    Takes a user objective (vague or detailed) and generates a structured
    intent using LLM. The intent captures problem statement, assumptions,
    requirements, acceptance criteria, and explicit non-goals.

    ## Client-Side LLM (ADR-027)

    Intent generation happens client-side to preserve privacy. User objectives
    and project context never leave the local machine during intent generation.

    ## Input Classification

    The handler classifies inputs into:
    - vague_nl: Short, underspecified ("add auth")
    - rich_nl: Detailed description with requirements
    - prd: Product requirements document (file)
    - prose_plan: Unstructured plan document (file)
    - structured_plan: MACHINE_PLAN JSON/YAML (file)

    Example:
        >>> handler = IntentHandler(Path("/path/to/project"))
        >>> intent = handler.generate("add user authentication")
        >>> print(intent.problem_statement)
    """

    def __init__(
        self,
        working_dir: Path,
        project: str | None = None,
        on_stream: Callable[[str, str], None] | None = None,
        llm_config: dict[str, Any] | None = None,
        log_event: Callable[..., None] | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
    ) -> None:
        """Initialize IntentHandler.

        Args:
            working_dir: Working directory for file access
            project: Optional project identifier (defaults to working_dir name)
            on_stream: Optional callback for LLM streaming chunks
            llm_config: Optional LLM configuration
            log_event: Optional logger for hybrid events
            trace_id: Optional trace ID for monitoring
            parent_span_id: Optional parent span ID for monitoring
        """
        self._working_dir = working_dir
        self._project = project or working_dir.name
        self._on_stream = on_stream
        self._llm_config = llm_config or {}
        self._log_event = log_event
        self._trace_id = trace_id
        self._parent_span_id = parent_span_id

    def generate(
        self,
        objective: str,
        *,
        input_type: InputType | None = None,
        base_prompt: str | None = None,
        force_empty: bool = False,
        force_existing: bool = False,
        detect_project_state_flag: bool = False,
    ) -> IntentModel:
        """Generate a structured intent from user objective.

        Args:
            objective: User objective (natural language)
            input_type: Optional pre-classified input type (auto-detects if None)
            base_prompt: Optional base prompt from server (two-tier prompting)
            force_empty: Force EMPTY project state (new/minimal project)
            force_existing: Force EXISTING project state (established codebase)
            detect_project_state_flag: Enable detection for PRD/plan inputs (skipped by default)

        Returns:
            IntentModel with structured intent data

        Raises:
            ValueError: If objective is empty or invalid

        Example:
            >>> handler = IntentHandler(Path.cwd())
            >>> intent = handler.generate("add authentication system")
            >>> print(intent.requirements)
            ['User can register', 'User can login', ...]
        """
        if not objective or not objective.strip():
            msg = "Objective cannot be empty"
            raise ValueError(msg)

        objective = objective.strip()
        logger.info("Generating intent for objective: %s...", objective[:50])

        # Classify input type
        detected_type = input_type or detect_input_type(objective)
        logger.debug("Detected input type: %s", detected_type)

        # Emit input_type_classified event (S4.T2)
        if self._log_event:
            self._log_event(
                "input_type_classified",
                session_id=None,
                trace_id=self._trace_id,
                parent_span_id=self._parent_span_id,
                detected_type=detected_type.value,
                objective_length=len(objective),
            )

        # Detect project state (FEAT-AUTO-INTENT-002 S1)
        from obra.config import (  # noqa: PLC0415
            get_project_detection_empty_threshold,
            get_project_detection_enabled,
            get_project_detection_existing_threshold,
        )
        from obra.intent.detection import ProjectState, detect_project_state  # noqa: PLC0415

        project_state_result = None

        # Determine if detection should run
        should_detect = False
        if detected_type in {InputType.VAGUE_NL, InputType.RICH_NL}:
            # Always detect for natural language inputs
            should_detect = True
        elif detected_type in {InputType.PRD, InputType.PROSE_PLAN}:
            # For PRD/plan, only detect if flag is set
            should_detect = detect_project_state_flag
        # STRUCTURED_PLAN: never detect (not applicable)

        # Run detection if enabled and applicable
        if should_detect and get_project_detection_enabled():
            # Determine force state
            force_state = None
            if force_empty:
                force_state = ProjectState.EMPTY
            elif force_existing:
                force_state = ProjectState.EXISTING

            # Get thresholds from config
            empty_threshold = get_project_detection_empty_threshold()
            existing_threshold = get_project_detection_existing_threshold()

            # Run detection
            project_state_result = detect_project_state(
                project_dir=self._working_dir,
                empty_threshold=empty_threshold,
                existing_threshold=existing_threshold,
                llm_config=self._llm_config,
                force_state=force_state,
            )

            logger.info(
                "Project state detected: %s (via %s)",
                project_state_result.state.value,
                project_state_result.method,
            )

            # Emit project_state_detected event (S4.T1)
            if self._log_event:
                self._log_event(
                    "project_state_detected",
                    session_id=None,
                    trace_id=self._trace_id,
                    parent_span_id=self._parent_span_id,
                    state=project_state_result.state.value,
                    method=project_state_result.method,
                    file_count=project_state_result.file_count,
                    empty_threshold=empty_threshold,
                    existing_threshold=existing_threshold,
                )

        # Generate intent based on input type
        # All generation methods return (intent_data, enrichment_level) tuple
        if detected_type == InputType.VAGUE_NL:
            intent_data, enrichment_level = self._generate_from_vague_nl(
                objective, base_prompt
            )
        elif detected_type == InputType.RICH_NL:
            intent_data, enrichment_level = self._generate_from_rich_nl(
                objective, base_prompt
            )
        elif detected_type == InputType.PRD:
            intent_data, enrichment_level = self._generate_from_prd(
                objective, base_prompt
            )
        elif detected_type == InputType.PROSE_PLAN:
            intent_data, enrichment_level = self._generate_from_prose_plan(
                objective, base_prompt
            )
        elif detected_type == InputType.STRUCTURED_PLAN:
            intent_data, enrichment_level = self._generate_from_structured_plan(
                objective
            )
        else:
            # Fallback to vague_nl handling
            intent_data, enrichment_level = self._generate_from_vague_nl(
                objective, base_prompt
            )

        # Create IntentModel
        slug = IntentModel.slugify(intent_data.get("problem_statement", objective))
        intent_id = IntentModel.generate_id(slug)

        intent = IntentModel(
            id=intent_id,
            project=self._project,
            slug=slug,
            created=datetime.now(UTC).isoformat(),
            input_type=detected_type,
            problem_statement=intent_data["problem_statement"],
            assumptions=intent_data.get("assumptions", []),
            requirements=intent_data.get("requirements", []),
            constraints=intent_data.get("constraints", []),
            acceptance_criteria=intent_data.get("acceptance_criteria", []),
            non_goals=intent_data.get("non_goals", []),
            risks=intent_data.get("risks", []),
            raw_objective=objective,
            enrichment_level=enrichment_level,
        )

        logger.info("Generated intent: %s", intent.id)
        return intent

    def _generate_from_vague_nl(
        self,
        objective: str,
        base_prompt: str | None,
    ) -> tuple[dict[str, Any], EnrichmentLevel]:
        """Generate intent from vague natural language input using LLM.

        Args:
            objective: Vague user objective
            base_prompt: Optional base prompt from server

        Returns:
            Tuple of (intent_data_dict, enrichment_level)
        """
        # Import prompt template here to avoid circular import
        from obra.intent.prompts import build_intent_generation_prompt  # noqa: PLC0415

        prompt = base_prompt or build_intent_generation_prompt(
            objective,
            input_type=InputType.VAGUE_NL,
        )

        provider, model, thinking_level, auth_method = self._resolve_llm_config()
        raw_response = self._invoke_llm(
            prompt,
            provider=provider,
            model=model,
            thinking_level=thinking_level,
            auth_method=auth_method,
        )

        # Create retry callback for rate limit handling (SIM-FIX-001 S1.T1)
        def retry_callback() -> str:
            return self._invoke_llm(
                prompt,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                auth_method=auth_method,
            )

        return self._parse_intent_response(raw_response, objective, llm_retry_callback=retry_callback)

    def _generate_from_rich_nl(
        self,
        objective: str,
        base_prompt: str | None,
    ) -> tuple[dict[str, Any], EnrichmentLevel]:
        """Generate intent from rich natural language input.

        For rich NL, we use LLM to extract structure from the detailed input.

        Args:
            objective: Rich user objective with details
            base_prompt: Optional base prompt from server

        Returns:
            Tuple of (intent_data_dict, enrichment_level)
        """
        # Import prompt template here
        from obra.intent.prompts import build_intent_generation_prompt  # noqa: PLC0415

        prompt = base_prompt or build_intent_generation_prompt(
            objective,
            input_type=InputType.RICH_NL,
        )

        provider, model, thinking_level, auth_method = self._resolve_llm_config()
        raw_response = self._invoke_llm(
            prompt,
            provider=provider,
            model=model,
            thinking_level=thinking_level,
            auth_method=auth_method,
        )

        # Create retry callback for rate limit handling (SIM-FIX-001 S1.T1)
        def retry_callback() -> str:
            return self._invoke_llm(
                prompt,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                auth_method=auth_method,
            )

        return self._parse_intent_response(raw_response, objective, llm_retry_callback=retry_callback)

    def _generate_from_prd(
        self,
        prd_path: str,
        base_prompt: str | None,
    ) -> tuple[dict[str, Any], EnrichmentLevel]:
        """Generate intent from PRD file.

        Args:
            prd_path: Path to PRD file
            base_prompt: Optional base prompt from server

        Returns:
            Tuple of (intent_data_dict, enrichment_level)

        Raises:
            FileNotFoundError: If PRD file doesn't exist
            ValueError: If PRD file is empty or unreadable
        """
        # Resolve path relative to working directory
        file_path = Path(prd_path)
        if not file_path.is_absolute():
            file_path = self._working_dir / file_path

        if not file_path.exists():
            msg = f"PRD file not found: {file_path}"
            raise FileNotFoundError(msg)

        # Read PRD content
        try:
            prd_content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            msg = f"Failed to read PRD file: {e}"
            raise ValueError(msg) from e

        if not prd_content.strip():
            msg = f"PRD file is empty: {file_path}"
            raise ValueError(msg)

        logger.info("Extracting intent from PRD: %s (%d chars)", file_path.name, len(prd_content))

        # Import prompt template
        from obra.intent.prompts import build_intent_generation_prompt  # noqa: PLC0415

        prompt = base_prompt or build_intent_generation_prompt(
            prd_content,
            input_type=InputType.PRD,
        )

        provider, model, thinking_level, auth_method = self._resolve_llm_config()
        raw_response = self._invoke_llm(
            prompt,
            provider=provider,
            model=model,
            thinking_level=thinking_level,
            auth_method=auth_method,
        )

        # Create retry callback for rate limit handling (SIM-FIX-001 S1.T1)
        def retry_callback() -> str:
            return self._invoke_llm(
                prompt,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                auth_method=auth_method,
            )

        return self._parse_intent_response(raw_response, prd_content[:100], llm_retry_callback=retry_callback)

    def _generate_from_prose_plan(
        self,
        plan_path: str,
        base_prompt: str | None,
    ) -> tuple[dict[str, Any], EnrichmentLevel]:
        """Generate intent from prose plan file.

        Args:
            plan_path: Path to prose plan file
            base_prompt: Optional base prompt from server

        Returns:
            Tuple of (intent_data_dict, enrichment_level)

        Raises:
            FileNotFoundError: If plan file doesn't exist
            ValueError: If plan file is empty or unreadable
        """
        # Resolve path relative to working directory
        file_path = Path(plan_path)
        if not file_path.is_absolute():
            file_path = self._working_dir / file_path

        if not file_path.exists():
            msg = f"Plan file not found: {file_path}"
            raise FileNotFoundError(msg)

        # Read plan content
        try:
            plan_content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            msg = f"Failed to read plan file: {e}"
            raise ValueError(msg) from e

        if not plan_content.strip():
            msg = f"Plan file is empty: {file_path}"
            raise ValueError(msg)

        logger.info("Extracting intent from prose plan: %s (%d chars)", file_path.name, len(plan_content))

        # Import prompt template
        from obra.intent.prompts import build_intent_generation_prompt  # noqa: PLC0415

        prompt = base_prompt or build_intent_generation_prompt(
            plan_content,
            input_type=InputType.PROSE_PLAN,
        )

        provider, model, thinking_level, auth_method = self._resolve_llm_config()
        raw_response = self._invoke_llm(
            prompt,
            provider=provider,
            model=model,
            thinking_level=thinking_level,
            auth_method=auth_method,
        )

        # Create retry callback for rate limit handling (SIM-FIX-001 S1.T1)
        def retry_callback() -> str:
            return self._invoke_llm(
                prompt,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                auth_method=auth_method,
            )

        return self._parse_intent_response(raw_response, plan_content[:100], llm_retry_callback=retry_callback)

    def _generate_from_structured_plan(
        self, plan_path: str
    ) -> tuple[dict[str, Any], EnrichmentLevel]:
        """Generate intent from structured plan file (mechanical extraction).

        This is a fast (~0ms) mechanical extraction that doesn't use LLM.
        Extracts intent from MACHINE_PLAN JSON/YAML structure.

        Args:
            plan_path: Path to structured MACHINE_PLAN file

        Returns:
            Tuple of (intent_data_dict, enrichment_level)
            Always returns FULL since this is deterministic extraction.

        Raises:
            FileNotFoundError: If plan file doesn't exist
            ValueError: If file is not a valid MACHINE_PLAN
        """
        # Resolve path relative to working directory
        file_path = Path(plan_path)
        if not file_path.is_absolute():
            file_path = self._working_dir / file_path

        if not file_path.exists():
            msg = f"Plan file not found: {file_path}"
            raise FileNotFoundError(msg)

        # Read and parse plan file
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            msg = f"Failed to read plan file: {e}"
            raise ValueError(msg) from e

        # Parse JSON or YAML
        import yaml  # noqa: PLC0415

        try:
            if file_path.suffix == ".json":
                data = json.loads(content)
            else:  # YAML
                data = yaml.safe_load(content)
        except Exception as e:
            msg = f"Failed to parse plan file: {e}"
            raise ValueError(msg) from e

        # Validate structure
        from obra.intent.detection import is_valid_machine_plan  # noqa: PLC0415

        if not is_valid_machine_plan(data):
            msg = f"Invalid MACHINE_PLAN structure in: {file_path}"
            raise ValueError(msg)

        logger.info(
            "Mechanically extracting intent from structured plan: %s",
            file_path.name,
        )

        # Extract intent fields mechanically
        work_id = data.get("work_id", "Unknown")
        context = data.get("context", {})
        stories = data.get("stories", [])
        completion_checklist = data.get("completion_checklist", [])

        # Problem statement: from work_id and context
        if isinstance(context, dict) and "objective" in context:
            problem_statement = str(context["objective"])
        elif stories:
            first_story = stories[0]
            story_title = first_story.get("title", first_story.get("desc", ""))
            problem_statement = f"{work_id}: {story_title}"
        else:
            problem_statement = work_id

        # Assumptions: from context.assumptions
        assumptions = []
        if isinstance(context, dict) and "assumptions" in context:
            context_assumptions = context["assumptions"]
            if isinstance(context_assumptions, list):
                assumptions = [str(a) for a in context_assumptions]

        # Requirements: from stories
        requirements = []
        for story in stories:
            if isinstance(story, dict):
                story_title = story.get("title", story.get("desc", ""))
                if story_title:
                    requirements.append(story_title)

        # Acceptance criteria: from completion_checklist
        acceptance_criteria = []
        if isinstance(completion_checklist, list):
            acceptance_criteria = [str(c) for c in completion_checklist]

        # Non-goals: from context or flags
        non_goals = []
        if isinstance(context, dict) and "non_goals" in context:
            context_non_goals = context["non_goals"]
            if isinstance(context_non_goals, list):
                non_goals = [str(ng) for ng in context_non_goals]

        # Structured plan extraction is deterministic, always FULL enrichment
        return (
            {
                "problem_statement": problem_statement,
                "assumptions": assumptions,
                "requirements": requirements if requirements else ["Complete all stories in plan"],
                "acceptance_criteria": acceptance_criteria
                if acceptance_criteria
                else ["All tasks completed"],
                "non_goals": non_goals,
            },
            EnrichmentLevel.FULL,
        )

    def _is_cli_error_response(self, response: str) -> tuple[bool, str | None]:
        """Detect error responses from CLI tools that don't raise exceptions.

        CLI tools sometimes return error messages as stdout instead of raising
        exceptions. This detects common patterns.

        Args:
            response: CLI response text

        Returns:
            Tuple of (is_error, error_type) for observability
        """
        if not response:
            return False, None

        lowered = response.lower().strip()
        first_line = lowered.split("\n")[0] if lowered else ""

        # CLI-specific error patterns that appear at start of output
        cli_error_starts = (
            "error:",
            "error -",
            "failed:",
            "exception:",
            "traceback (most recent call last)",
            "fatal:",
            "panic:",
        )
        for pattern in cli_error_starts:
            if first_line.startswith(pattern) or lowered.startswith(pattern):
                return True, f"cli_error_start:{pattern.rstrip(':')}"

        # Check for Python/shell error patterns anywhere in short responses
        if len(response) < 500:
            error_patterns = (
                "command not found",
                "no such file or directory",
                "permission denied",
                "connection refused",
                "timeout expired",
                "modulenotfounderror",
                "importerror",
            )
            for pattern in error_patterns:
                if pattern in lowered:
                    return True, f"cli_error_pattern:{pattern}"

        return False, None

    def _invoke_llm(
        self,
        prompt: str,
        *,
        provider: str,
        model: str,
        thinking_level: str,
        auth_method: str = "oauth",
    ) -> str:
        """Invoke LLM to generate intent.

        Args:
            prompt: Intent generation prompt
            provider: LLM provider name
            model: LLM model name
            thinking_level: LLM thinking level
            auth_method: Authentication method

        Returns:
            Raw LLM response

        Raises:
            RuntimeError: If CLI returns error response
        """
        logger.debug(
            "Invoking LLM for intent: provider=%s model=%s thinking=%s",
            provider,
            model,
            thinking_level,
        )

        def _stream(chunk: str) -> None:
            if self._on_stream:
                self._on_stream("llm_streaming", chunk)

        try:
            response = str(
                invoke_llm_via_cli(
                    prompt=prompt,
                    cwd=self._working_dir,
                    provider=provider,
                    model=model,
                    thinking_level=thinking_level,
                    auth_method=auth_method,
                    on_stream=_stream if self._on_stream else None,
                    log_event=self._log_event,
                    trace_id=self._trace_id,
                    parent_span_id=self._parent_span_id,
                    call_site="intent_generation",
                    skip_git_check=self._llm_config.get("git", {}).get("skip_check", False),  # GIT-HARD-001
                )
            )

            # Check for CLI-level errors returned as strings
            is_cli_error, error_type = self._is_cli_error_response(response)
            if is_cli_error:
                logger.warning(
                    "LLM CLI returned error response (type=%s): %s",
                    error_type,
                    response[:300],
                )
                # Return error indicator that will trigger Tier 4 fallback
                # Don't mask as valid JSON - let garbage detection catch it
                return f"CLI_ERROR: {error_type} - {response[:200]}"

            return response

        except Exception:
            logger.exception("LLM invocation failed for intent generation")
            # Return minimal fallback structure
            return json.dumps(
                {
                    "problem_statement": "Error generating intent",
                    "assumptions": [],
                    "requirements": [],
                    "acceptance_criteria": [],
                    "non_goals": [],
                }
            )

    def _parse_intent_response(
        self,
        raw_response: str,
        objective: str,
        llm_retry_callback: Callable[[], str] | None = None,
    ) -> tuple[dict[str, Any], EnrichmentLevel]:
        """Parse LLM response into intent data structure using 6-tier graceful degradation.

        Implements a 6-tier parsing strategy for resilient intent extraction:
        - Tier 1: YAML frontmatter parsing (primary format)
        - Tier 2: Markdown sections parsing (natural LLM format)
        - Tier 3: Direct JSON parsing (legacy, structured LLM response)
        - Tier 4: JSON payload extraction (legacy, JSON embedded in prose)
        - Tier 5: Prose extraction (natural language with recognizable structure)
        - Tier 6: Fallback (minimal intent from original objective)

        Rate limit retry (SIM-FIX-001 S1.T0):
        If rate limit error detected and llm_retry_callback provided, retries up to 3 times
        with exponential backoff (2s, 4s, 8s).

        Args:
            raw_response: Raw LLM response
            objective: Original user objective
            llm_retry_callback: Optional callback to retry LLM invocation on rate limit

        Returns:
            Tuple of (intent_data_dict, enrichment_level) where:
            - intent_data_dict has problem_statement, assumptions, requirements, etc.
            - enrichment_level indicates parsing success (YAML, FULL, PROSE, or NONE)

        FIX-GARBAGE-WRAPPER-001: Unwraps CLI JSON wrapper before parsing to ensure
        the actual LLM content is processed, not the CLI metadata.
        """
        # Unwrap CLI JSON wrapper (Claude, Gemini) before any processing
        # This extracts the actual LLM response from {"type":"result","result":"..."}
        response_to_parse = raw_response
        if raw_response.strip().startswith("{"):
            try:
                data = json.loads(raw_response)
                if isinstance(data, dict):
                    # Claude CLI wrapper: {"type": "result", "is_error": bool, "result": "..."}
                    if data.get("type") == "result" and "result" in data:
                        if data.get("is_error"):
                            logger.warning("CLI wrapper indicates error, using fallback")
                            return self._tier4_fallback(objective), EnrichmentLevel.NONE
                        result = data.get("result", "")
                        if isinstance(result, str) and result.strip():
                            response_to_parse = result.strip()
                            logger.debug("Unwrapped Claude CLI JSON wrapper for parsing")
                    # Gemini CLI wrapper: {"response": "...", "stats": {...}}
                    elif "response" in data and "stats" in data:
                        stats = data.get("stats", {})
                        if isinstance(stats, dict) and stats.get("error"):
                            logger.warning("Gemini CLI wrapper indicates error, using fallback")
                            return self._tier4_fallback(objective), EnrichmentLevel.NONE
                        response = data.get("response", "")
                        if isinstance(response, str) and response.strip():
                            response_to_parse = response.strip()
                            logger.debug("Unwrapped Gemini CLI JSON wrapper for parsing")
            except json.JSONDecodeError:
                pass  # Not valid JSON, continue with original response

        # Early exit for garbage/error responses with retry logic for rate limits
        is_garbage, garbage_reason = is_garbage_response(response_to_parse, return_reason=True)
        if is_garbage:
            # Check if this is a rate limit error
            is_rate_limit = (
                isinstance(garbage_reason, str)
                and "error_marker:" in garbage_reason
                and any(
                    marker in garbage_reason
                    for marker in ["rate limit", "ratelimit", "too many requests"]
                )
            )

            # Retry logic for rate limit errors
            if is_rate_limit and llm_retry_callback:
                for attempt in range(RATE_LIMIT_MAX_RETRIES):
                    delay = RATE_LIMIT_BACKOFF_DELAYS[attempt]
                    logger.info(
                        "Rate limit detected, retrying in %.1fs (attempt %d/%d)",
                        delay,
                        attempt + 1,
                        RATE_LIMIT_MAX_RETRIES,
                    )
                    time.sleep(delay)

                    # Retry LLM invocation
                    try:
                        raw_response = llm_retry_callback()
                        # Re-run unwrapping on new response
                        response_to_parse = raw_response
                        if raw_response.strip().startswith("{"):
                            try:
                                retry_data = json.loads(raw_response)
                                if isinstance(retry_data, dict):
                                    if retry_data.get("type") == "result" and "result" in retry_data:
                                        if not retry_data.get("is_error"):
                                            result = retry_data.get("result", "")
                                            if isinstance(result, str) and result.strip():
                                                response_to_parse = result.strip()
                                    elif "response" in retry_data and "stats" in retry_data:
                                        stats = retry_data.get("stats", {})
                                        if not (isinstance(stats, dict) and stats.get("error")):
                                            response = retry_data.get("response", "")
                                            if isinstance(response, str) and response.strip():
                                                response_to_parse = response.strip()
                            except json.JSONDecodeError:
                                pass
                        # Check if retry succeeded
                        is_garbage, garbage_reason = is_garbage_response(
                            response_to_parse, return_reason=True
                        )
                        if not is_garbage:
                            logger.info("Rate limit retry succeeded on attempt %d", attempt + 1)
                            break
                        # Check if still rate limited
                        is_rate_limit = (
                            isinstance(garbage_reason, str)
                            and "error_marker:" in garbage_reason
                            and any(
                                marker in garbage_reason
                                for marker in ["rate limit", "ratelimit", "too many requests"]
                            )
                        )
                        if not is_rate_limit:
                            # Different error type, stop retrying
                            break
                    except Exception:
                        logger.exception("Rate limit retry failed on attempt %d", attempt + 1)
                        break

            # If still garbage after retries (or no retry callback), use fallback
            if is_garbage:
                logger.warning(
                    "Detected garbage response (reason=%s), using Tier 6 fallback. "
                    "Response preview: %s",
                    garbage_reason,
                    response_to_parse[:200] if response_to_parse else "<empty>",
                )
                return self._tier4_fallback(objective), EnrichmentLevel.NONE

        # Tier 1: YAML frontmatter parsing
        tier1_result = self._tier1_yaml_frontmatter(response_to_parse, objective)
        if tier1_result is not None:
            logger.debug("Tier 1 (YAML frontmatter) succeeded")
            return tier1_result, EnrichmentLevel.YAML

        # Tier 2: Markdown sections parsing
        tier2_result = self._tier2_markdown_sections(response_to_parse, objective)
        if tier2_result is not None:
            logger.debug("Tier 2 (markdown sections) succeeded")
            return tier2_result, EnrichmentLevel.YAML

        # Tier 3: Direct JSON parsing (legacy)
        tier3_result = self._tier1_direct_json(response_to_parse, objective)
        if tier3_result is not None:
            logger.debug("Tier 3 (direct JSON - legacy) succeeded")
            return tier3_result, EnrichmentLevel.FULL

        # Tier 4: JSON payload extraction (legacy)
        tier4_result = self._tier2_extract_json(response_to_parse, objective)
        if tier4_result is not None:
            logger.debug("Tier 4 (extract JSON payload - legacy) succeeded")
            return tier4_result, EnrichmentLevel.FULL

        # Tier 5: Prose extraction
        tier5_result = self._tier3_prose_extraction(response_to_parse, objective)
        if tier5_result is not None:
            logger.debug("Tier 5 (prose extraction) succeeded")
            return tier5_result, EnrichmentLevel.PROSE

        # Tier 6: Fallback
        logger.warning("All parsing tiers failed, using Tier 6 fallback")
        return self._tier4_fallback(objective), EnrichmentLevel.NONE

    def _tier1_yaml_frontmatter(
        self, raw_response: str, objective: str
    ) -> dict[str, Any] | None:
        """Tier 1: Parse YAML frontmatter format.

        Extracts structured intent from YAML frontmatter delimited by --- markers.
        Format:
            ---
            problem_statement: |
              Text here
            assumptions:
              - Item 1
              - Item 2
            ---

        Args:
            raw_response: Raw LLM response
            objective: Original user objective

        Returns:
            Parsed intent dict or None if parsing fails
        """
        try:
            response = raw_response.strip()

            # Handle markdown code blocks (```yaml or ```)
            if response.startswith("```"):
                lines = response.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1].strip() == "```" else len(lines)
                response = "\n".join(lines[start:end])

            # Look for YAML frontmatter (--- delimited)
            frontmatter_pattern = r"^---\s*\n(.*?)\n---"
            match = re.match(frontmatter_pattern, response, re.DOTALL)

            if not match:
                return None

            yaml_content = match.group(1)
            data = yaml.safe_load(yaml_content)

            if not isinstance(data, dict):
                return None

            return self._extract_intent_fields(data, objective)

        except (yaml.YAMLError, AttributeError, KeyError):
            return None

    def _tier2_markdown_sections(
        self, raw_response: str, objective: str
    ) -> dict[str, Any] | None:
        """Tier 2: Parse markdown sections format.

        Extracts structured intent from markdown sections using ## headers.
        Recognizes common section headers like:
        - ## Problem Statement
        - ## Assumptions
        - ## Requirements
        - ## Acceptance Criteria
        - ## Non-Goals

        Args:
            raw_response: Raw LLM response
            objective: Original user objective

        Returns:
            Parsed intent dict or None if parsing fails
        """
        try:
            response = raw_response.strip()

            # Look for markdown sections with ## headers
            if "##" not in response:
                return None

            # Define section patterns (case-insensitive)
            sections = {
                "problem_statement": r"##\s*(?:Problem\s*Statement|Problem|Overview)",
                "assumptions": r"##\s*Assumptions?",
                "requirements": r"##\s*Requirements?",
                "acceptance_criteria": r"##\s*(?:Acceptance\s*Criteria|Success\s*Criteria)",
                "non_goals": r"##\s*(?:Non[- ]?Goals|Out[- ]of[- ]Scope)",
            }

            data = {}
            found_any = False

            for field, pattern in sections.items():
                # Find section header
                match = re.search(pattern, response, re.IGNORECASE)
                if not match:
                    continue

                found_any = True
                start = match.end()

                # Find next section or end of text
                next_section = re.search(r"\n##\s", response[start:])
                end = start + next_section.start() if next_section else len(response)

                content = response[start:end].strip()

                # Extract list items or use paragraph
                if field in ("assumptions", "requirements", "acceptance_criteria", "non_goals"):
                    items = []
                    for line in content.split("\n"):
                        stripped_line = line.strip()
                        # Match bullets or numbered items
                        if stripped_line.startswith(("-", "*", "•")):
                            item = stripped_line.lstrip("-*• ").strip()
                            if item:
                                items.append(item)
                        elif stripped_line and stripped_line[0].isdigit() and (". " in stripped_line or ") " in stripped_line):
                            item = re.sub(r"^\d+[.)]\s*", "", stripped_line).strip()
                            if item:
                                items.append(item)
                    data[field] = items
                else:
                    # problem_statement is text, not list
                    data[field] = content

            # Only succeed if we found at least problem_statement or 2+ sections
            if not found_any or (
                "problem_statement" not in data and len(data) < 2
            ):
                return None

            return self._extract_intent_fields(data, objective)

        except (AttributeError, KeyError):
            return None

    def _tier1_direct_json(
        self, raw_response: str, objective: str
    ) -> dict[str, Any] | None:
        """Tier 1: Direct JSON parsing with markdown handling.

        Args:
            raw_response: Raw LLM response
            objective: Original user objective

        Returns:
            Parsed intent dict or None if parsing fails
        """
        try:
            response = raw_response.strip()

            # Handle markdown code blocks
            if response.startswith("```"):
                lines = response.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1] == "```" else len(lines)
                response = "\n".join(lines[start:end])

            data = json.loads(response)
            return self._extract_intent_fields(data, objective)

        except json.JSONDecodeError:
            return None

    def _tier2_extract_json(
        self, raw_response: str, objective: str
    ) -> dict[str, Any] | None:
        """Tier 2: Extract JSON payload from mixed response.

        Uses extract_json_payload() utility to find embedded JSON.

        Args:
            raw_response: Raw LLM response
            objective: Original user objective

        Returns:
            Parsed intent dict or None if extraction fails
        """
        payload = extract_json_payload(raw_response)
        if payload is None:
            return None

        try:
            data = json.loads(payload)
            return self._extract_intent_fields(data, objective)
        except json.JSONDecodeError:
            return None

    def _tier3_prose_extraction(
        self, raw_response: str, _objective: str  # objective unused - Tier 4 handles fallback
    ) -> dict[str, Any] | None:
        """Tier 3: Extract intent from declarative natural language prose.

        Attempts to extract structured data from a prose response by
        looking for common patterns like numbered lists, bullet points,
        and labeled sections.

        Rejects interrogative responses (predominantly questions) since
        those indicate non-compliance rather than valid intent content.

        Args:
            raw_response: Raw LLM response (natural language)
            _objective: Original user objective (unused, Tier 4 handles fallback)

        Returns:
            Partial intent dict or None if no meaningful extraction
        """
        text = raw_response.strip()
        if not text:
            return None

        # Reject predominantly interrogative responses
        if self._is_interrogative(text):
            logger.debug("Tier 3 rejected: response is predominantly interrogative")
            return None

        # Try to extract problem statement from first paragraph/sentence
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        if not lines:
            return None

        # Use first meaningful line as problem statement
        problem_statement = lines[0]

        # Remove markdown headers
        if problem_statement.startswith("#"):
            problem_statement = problem_statement.lstrip("#").strip()

        # Reject if problem statement is a question
        if problem_statement.endswith("?"):
            logger.debug("Tier 3 rejected: problem statement is a question")
            return None

        # Look for bullet points or numbered items for requirements
        requirements = []
        for line in lines[1:]:
            # Match bullet points: -, *, •
            if line.startswith(("-", "*", "•")):
                item = line.lstrip("-*• ").strip()
                if item and len(item) > 3:  # Skip very short items
                    requirements.append(item)
            # Match numbered items: 1., 1), (1)
            elif len(line) > 2 and line[0].isdigit():
                # Strip number prefix like "1.", "1)", "(1)"
                item = line.lstrip("0123456789.)(").strip()
                if item and len(item) > 3:
                    requirements.append(item)

        # Only return if we extracted something meaningful
        if problem_statement and (requirements or len(problem_statement) > 20):
            return {
                "problem_statement": problem_statement[:500],  # Cap length
                "assumptions": [],
                "requirements": requirements[:10],  # Cap count
                "acceptance_criteria": ["Implementation complete and verified"],
                "non_goals": [],
            }

        return None

    def _is_interrogative(self, text: str) -> bool:
        """Check if text is predominantly questions rather than statements.

        Uses punctuation-based heuristics to detect interrogative responses.
        This is more robust than phrase matching and language-agnostic.

        Args:
            text: Text to analyze

        Returns:
            True if response is predominantly questions
        """
        question_count = text.count("?")
        sentence_count = text.count(".") + text.count("!") + question_count
        if sentence_count == 0:
            return question_count > 0
        return question_count / sentence_count > INTERROGATIVE_RATIO_THRESHOLD

    def _tier4_fallback(self, objective: str) -> dict[str, Any]:
        """Tier 4: Minimal fallback intent from objective.

        Args:
            objective: Original user objective

        Returns:
            Minimal intent dict using objective as problem statement
        """
        return {
            "problem_statement": objective,
            "assumptions": [],
            "requirements": [],
            "acceptance_criteria": ["Implementation complete and verified"],
            "non_goals": [],
        }

    def _extract_intent_fields(
        self, data: dict[str, Any], objective: str
    ) -> dict[str, Any]:
        """Extract intent fields from parsed JSON data.

        Args:
            data: Parsed JSON dict
            objective: Fallback objective

        Returns:
            Dict with intent fields
        """
        return {
            "problem_statement": data.get("problem_statement", objective),
            "assumptions": data.get("assumptions", []),
            "requirements": data.get("requirements", []),
            "acceptance_criteria": data.get("acceptance_criteria", []),
            "non_goals": data.get("non_goals", []),
        }

    def _resolve_llm_config(self) -> tuple[str, str, str, str]:
        """Resolve LLM configuration from stored config.

        Returns:
            Tuple of (provider, model, thinking_level, auth_method)
        """
        provider = self._llm_config.get("provider", "claude")
        model = self._llm_config.get("model", "default")
        thinking_level = self._llm_config.get("thinking_level", "medium")
        auth_method = self._llm_config.get("auth_method", "oauth")
        return provider, model, thinking_level, auth_method


__all__ = ["IntentHandler"]
