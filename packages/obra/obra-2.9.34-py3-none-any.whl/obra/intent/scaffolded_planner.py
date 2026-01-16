"""Scaffolded planning orchestrator for intent enrichment."""

from __future__ import annotations

import json
import logging
import sys
import time
from datetime import UTC, datetime
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from obra.config.llm import resolve_tier_config
from obra.exceptions import ConfigurationError
from obra.hybrid.json_utils import is_garbage_response
from obra.intent.analogue_cache import (
    append_analogue_cache_entry,
    load_analogue_cache_entries,
    render_analogue_cache,
)
from obra.intent.diff import build_intent_diff, render_intent_diff
from obra.intent.models import InputType, IntentModel
from obra.intent.prompts_scaffolded import (
    build_assumptions_prompt,
    build_brief_prompt,
    build_expert_alignment_prompt,
)
from obra.intent.retention import cleanup_retention
from obra.intent.scaffolded_config import load_scaffolded_config
from obra.intent.storage import IntentStorage
from obra.intent.telemetry import log_scaffolded_event
from obra.llm.cli_runner import invoke_llm_via_cli

logger = logging.getLogger(__name__)


def _unwrap_cli_response(raw_response: str) -> str:
    response = raw_response.strip()
    if not response.startswith("{"):
        return response
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        return response
    if isinstance(data, dict):
        if data.get("type") == "result" and "result" in data:
            result = data.get("result")
            if isinstance(result, str) and result.strip():
                return result.strip()
        if "response" in data and "stats" in data:
            response_value = data.get("response")
            if isinstance(response_value, str) and response_value.strip():
                return response_value.strip()
    return response


def _parse_yaml_frontmatter(raw_response: str) -> dict[str, Any]:
    response = _unwrap_cli_response(raw_response)
    if not response.startswith("---"):
        return {}
    parts = response.split("---", 2)
    if len(parts) < 3:
        return {}
    try:
        data = yaml.safe_load(parts[1]) or {}
        if isinstance(data, dict):
            return data
    except yaml.YAMLError:
        return {}
    return {}


@dataclass
class ScaffoldedStageResult:
    name: str
    raw_response: str
    parsed: dict[str, Any]
    duration_s: float


class ScaffoldedPlanner:
    """Run scaffolded intent enrichment stages A-C."""

    def __init__(
        self,
        working_dir: Path,
        *,
        llm_config: dict[str, Any],
        on_stream: Any | None = None,
        log_event: Any | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
    ) -> None:
        self._working_dir = working_dir
        self._llm_config = llm_config
        self._on_stream = on_stream
        self._log_event = log_event
        self._trace_id = trace_id
        self._parent_span_id = parent_span_id
        try:
            self._config = load_scaffolded_config(working_dir)
        except ConfigurationError as exc:
            logger.warning("Scaffolded planning disabled due to config error: %s", exc)
            self._config = {"enabled": False}

    def is_enabled(self) -> bool:
        return bool(self._config.get("enabled", False))

    def should_run(
        self,
        input_type: InputType,
        *,
        force: bool = False,
        skip: bool = False,
    ) -> bool:
        if skip:
            return False
        if not self.is_enabled():
            return False
        if force:
            return True
        always_on = bool(self._config.get("always_on", True))
        if always_on:
            return True
        return input_type in {InputType.VAGUE_NL, InputType.RICH_NL}

    def get_stage_config(self, stage: str) -> dict[str, Any]:
        """Expose stage configuration for external orchestration."""
        return self._get_stage_config(stage)

    def run(
        self,
        objective: str,
        intent: IntentModel,
        *,
        interactive: bool,
    ) -> tuple[IntentModel, Path | None]:
        if not self.is_enabled():
            return intent, None

        stage_results: list[ScaffoldedStageResult] = []
        intent_before = intent.model_copy(deep=True)

        stage_a_result = self._run_assumptions_stage(objective, intent, stage_results)
        self._apply_assumptions(intent, stage_a_result, interactive=interactive)

        stage_b_result = self._run_expert_stage(objective, intent, stage_results)
        self._apply_expert_updates(intent, stage_b_result)
        self._update_analogue_cache(objective, stage_b_result)

        stage_c_result = self._run_brief_stage(objective, intent, stage_results)
        self._apply_brief_update(intent, stage_c_result)

        storage = IntentStorage()
        storage.save(intent)

        diff_path = self._write_intent_diff(intent_before, intent, stage_c_result)

        self._write_stage_artifacts(intent.id, stage_results)
        self._log_telemetry(intent.id, stage_results)
        self._run_retention_cleanup()

        return intent, diff_path

    def _run_assumptions_stage(
        self,
        objective: str,
        intent: IntentModel,
        stage_results: list[ScaffoldedStageResult],
    ) -> ScaffoldedStageResult:
        stage_config = self._get_stage_config("assumptions")
        prompt = build_assumptions_prompt(
            objective,
            self._format_intent(intent),
            self._config.get("non_inferable_categories", []),
        )
        result = self._invoke_stage("assumptions", prompt, stage_config)
        stage_results.append(result)
        return result

    def _run_expert_stage(
        self,
        objective: str,
        intent: IntentModel,
        stage_results: list[ScaffoldedStageResult],
    ) -> ScaffoldedStageResult:
        stage_config = self._get_stage_config("analogues")
        cache_entries = self._load_analogue_cache_entries()
        cache_text = render_analogue_cache(cache_entries)
        prompt = build_expert_alignment_prompt(
            objective,
            self._format_intent(intent),
            analogue_cache=cache_text or None,
        )
        result = self._invoke_stage("analogues", prompt, stage_config)
        stage_results.append(result)
        return result

    def _run_brief_stage(
        self,
        objective: str,
        intent: IntentModel,
        stage_results: list[ScaffoldedStageResult],
    ) -> ScaffoldedStageResult:
        stage_config = self._get_stage_config("brief")
        prompt = build_brief_prompt(objective, self._format_intent(intent))
        result = self._invoke_stage("brief", prompt, stage_config)
        stage_results.append(result)
        return result

    def _invoke_stage(
        self, stage_name: str, prompt: str, stage_config: dict[str, Any]
    ) -> ScaffoldedStageResult:
        model_tier = stage_config.get("model_tier")
        if "reasoning_level" not in stage_config:
            raise ConfigurationError(
                f"planning.scaffolded.stages.{stage_name}.reasoning_level is required",
                "Set the reasoning_level in config/default_config.yaml or .obra/config.yaml",
            )
        if "max_passes" not in stage_config:
            raise ConfigurationError(
                f"planning.scaffolded.stages.{stage_name}.max_passes is required",
                "Set max_passes in config/default_config.yaml or .obra/config.yaml",
            )
        if "timeout_s" not in stage_config:
            raise ConfigurationError(
                f"planning.scaffolded.stages.{stage_name}.timeout_s is required",
                "Set timeout_s in config/default_config.yaml or .obra/config.yaml",
            )
        reasoning_level = stage_config.get("reasoning_level")
        max_passes = int(stage_config.get("max_passes"))
        timeout_s = int(stage_config.get("timeout_s"))

        if not model_tier:
            raise ConfigurationError(
                f"planning.scaffolded.stages.{stage_name}.model_tier is required",
                "Set the model_tier in config/default_config.yaml or .obra/config.yaml",
            )
        if max_passes < 1:
            return ScaffoldedStageResult(stage_name, "", {}, 0.0)

        resolved = resolve_tier_config(
            model_tier,
            role="implementation",
            override_thinking_level=reasoning_level,
        )

        start = time.time()
        raw_response = invoke_llm_via_cli(
            prompt=prompt,
            cwd=self._working_dir,
            provider=resolved["provider"],
            model=resolved["model"],
            thinking_level=resolved["thinking_level"],
            auth_method=resolved["auth_method"],
            on_stream=self._build_stream_handler(stage_name),
            timeout_s=timeout_s or None,
            log_event=self._log_event,
            trace_id=self._trace_id,
            parent_span_id=self._parent_span_id,
            call_site=f"scaffolded_{stage_name}",
            monitoring_context=None,
            skip_git_check=self._llm_config.get("git", {}).get("skip_check", False),
        )

        duration = time.time() - start
        response_text = _unwrap_cli_response(raw_response)
        parsed = _parse_yaml_frontmatter(response_text)
        if response_text:
            is_garbage = is_garbage_response(response_text)
            if is_garbage:
                logger.warning("Scaffolded %s stage returned garbage response", stage_name)
        return ScaffoldedStageResult(stage_name, response_text, parsed, duration)

    def _load_analogue_cache_entries(self) -> list[dict[str, Any]]:
        cache_config = self._config.get("analogue_cache", {})
        global_path = cache_config.get("global_path")
        project_path = cache_config.get("project_path")
        resolved_global = Path(global_path).expanduser() if global_path else None
        resolved_project = (
            (self._working_dir / project_path).resolve()
            if project_path
            else None
        )
        return load_analogue_cache_entries(
            global_path=resolved_global,
            project_path=resolved_project,
        )

    def _update_analogue_cache(
        self, objective: str, result: ScaffoldedStageResult
    ) -> None:
        if not result.parsed:
            return
        cache_config = self._config.get("analogue_cache", {})
        global_path = cache_config.get("global_path")
        project_path = cache_config.get("project_path")
        if not global_path and not project_path:
            return
        resolved_global = Path(global_path).expanduser() if global_path else None
        resolved_project = (
            (self._working_dir / project_path).resolve()
            if project_path
            else None
        )
        domain_inference = result.parsed.get("domain_inference") or []
        domains = [
            entry.get("domain")
            for entry in domain_inference
            if isinstance(entry, dict) and entry.get("domain")
        ]
        expert_roles = []
        for entry in domain_inference:
            if isinstance(entry, dict):
                expert_roles.extend(entry.get("expert_roles") or [])
        entry = {
            "created": datetime.now(UTC).isoformat(),
            "objective_preview": objective,
            "domains": domains,
            "expert_roles": expert_roles,
            "expert_approach": result.parsed.get("expert_approach") or [],
            "intent_gaps": result.parsed.get("intent_gaps") or [],
            "rationale": result.parsed.get("rationale") or "",
        }
        append_analogue_cache_entry(
            entry,
            global_path=resolved_global,
            project_path=resolved_project,
        )

    def _apply_assumptions(
        self, intent: IntentModel, result: ScaffoldedStageResult, *, interactive: bool
    ) -> None:
        data = result.parsed
        assumptions_add = data.get("assumptions_add", []) or []
        questions = data.get("questions", []) or []
        non_inferable = data.get("non_inferable_questions", []) or []

        intent.assumptions = _merge_unique(intent.assumptions, assumptions_add)

        if questions:
            intent.metadata.setdefault("unresolved_questions", [])
            intent.metadata["unresolved_questions"] = _merge_unique(
                intent.metadata["unresolved_questions"], questions
            )

        if non_inferable:
            intent.metadata.setdefault("non_inferable_questions", [])
            intent.metadata["non_inferable_questions"] = _merge_unique(
                intent.metadata["non_inferable_questions"], non_inferable
            )
            if interactive and sys.stdin.isatty():
                self._prompt_non_inferable(intent, non_inferable)

    def _prompt_non_inferable(self, intent: IntentModel, questions: list[str]) -> None:
        assumptions_stage = self._config.get("stages", {}).get("assumptions", {})
        if "max_questions" not in assumptions_stage:
            raise ConfigurationError(
                "planning.scaffolded.stages.assumptions.max_questions is required",
                "Set max_questions in config/default_config.yaml or .obra/config.yaml",
            )
        max_questions = int(assumptions_stage.get("max_questions"))
        if max_questions <= 0:
            return

        answers: list[str] = []
        for question in questions[:max_questions]:
            try:
                answer = input(f"[Scaffolded planning] {question} ")
            except (EOFError, KeyboardInterrupt):
                break
            answer = answer.strip()
            if answer:
                answers.append(f"{question} -> {answer}")
        if answers:
            intent.context_amendments.extend(answers)
            intent.metadata.setdefault("non_inferable_answers", [])
            intent.metadata["non_inferable_answers"] = _merge_unique(
                intent.metadata["non_inferable_answers"], answers
            )

    def _apply_expert_updates(self, intent: IntentModel, result: ScaffoldedStageResult) -> None:
        updates = result.parsed.get("proposed_intent_updates", {}) or {}
        intent.assumptions = _merge_unique(intent.assumptions, updates.get("assumptions_add", []))
        intent.requirements = _merge_unique(intent.requirements, updates.get("requirements_add", []))
        intent.constraints = _merge_unique(intent.constraints, updates.get("constraints_add", []))
        intent.non_goals = _merge_unique(intent.non_goals, updates.get("non_goals_add", []))
        intent.risks = _merge_unique(intent.risks, updates.get("risks_add", []))
        intent.acceptance_criteria = _merge_unique(
            intent.acceptance_criteria, updates.get("acceptance_criteria_add", [])
        )

        domain_inference = result.parsed.get("domain_inference")
        if domain_inference:
            intent.metadata["domain_inference"] = domain_inference

        expert_approach = result.parsed.get("expert_approach")
        if expert_approach:
            intent.metadata["expert_approach"] = expert_approach

        intent_gaps = result.parsed.get("intent_gaps")
        if intent_gaps:
            intent.metadata["intent_gaps"] = intent_gaps

    def _apply_brief_update(self, intent: IntentModel, result: ScaffoldedStageResult) -> None:
        data = result.parsed
        if not data:
            return
        intent.problem_statement = data.get("problem_statement", intent.problem_statement)
        intent.assumptions = data.get("assumptions", intent.assumptions) or intent.assumptions
        intent.requirements = data.get("requirements", intent.requirements) or intent.requirements
        intent.constraints = data.get("constraints", intent.constraints) or intent.constraints
        intent.acceptance_criteria = data.get(
            "acceptance_criteria", intent.acceptance_criteria
        ) or intent.acceptance_criteria
        intent.non_goals = data.get("non_goals", intent.non_goals) or intent.non_goals
        intent.risks = data.get("risks", intent.risks) or intent.risks

    def _write_intent_diff(
        self,
        before: IntentModel,
        after: IntentModel,
        stage_result: ScaffoldedStageResult,
    ) -> Path | None:
        diff_config = self._config.get("diff", {})
        path_template = diff_config.get("path_template")
        if not path_template:
            raise ConfigurationError(
                "planning.scaffolded.diff.path_template is required",
                "Set planning.scaffolded.diff.path_template in config.",
            )
        diff_path = Path(path_template.format(intent_id=after.id)).expanduser()
        diff_data = build_intent_diff(
            before,
            after,
            stage="scaffolded",
            rationale=stage_result.parsed.get("rationale"),
            metadata={
                "non_inferable_questions": after.metadata.get("non_inferable_questions", []),
                "non_inferable_answers": after.metadata.get("non_inferable_answers", []),
            },
        )
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        diff_path.write_text(render_intent_diff(diff_data), encoding="utf-8")
        return diff_path

    def _write_stage_artifacts(self, intent_id: str, stage_results: list[ScaffoldedStageResult]) -> None:
        artifacts_config = self._config.get("artifacts", {})
        artifacts_dir = artifacts_config.get("dir")
        if not artifacts_dir:
            raise ConfigurationError(
                "planning.scaffolded.artifacts.dir is required",
                "Set planning.scaffolded.artifacts.dir in config.",
            )
        root = Path(artifacts_dir).expanduser() / intent_id
        root.mkdir(parents=True, exist_ok=True)
        for result in stage_results:
            if not result.raw_response:
                continue
            path = root / f"{result.name}.md"
            path.write_text(result.raw_response, encoding="utf-8")

    def _log_telemetry(self, intent_id: str, stage_results: list[ScaffoldedStageResult]) -> None:
        telemetry_config = self._config.get("telemetry", {})
        if not telemetry_config.get("enabled", False):
            return
        output_path = telemetry_config.get("output_path")
        if not output_path:
            raise ConfigurationError(
                "planning.scaffolded.telemetry.output_path is required",
                "Set planning.scaffolded.telemetry.output_path in config.",
            )
        include_content = bool(telemetry_config.get("include_content", False))
        stages_payload = []
        for result in stage_results:
            entry = {
                "stage": result.name,
                "duration_s": result.duration_s,
                "parsed_keys": sorted(result.parsed.keys()),
            }
            if include_content:
                entry["raw_response"] = result.raw_response
            stages_payload.append(entry)
        log_scaffolded_event(
            Path(output_path),
            {
                "intent_id": intent_id,
                "stages": stages_payload,
            },
        )

    def _run_retention_cleanup(self) -> None:
        diff_retention = self._config.get("diff", {}).get("retention", {})
        artifacts_retention = self._config.get("artifacts", {}).get("retention", {})

        diff_path = self._config.get("diff", {}).get("path_template")
        if diff_path:
            if "max_age_days" not in diff_retention or "max_files" not in diff_retention:
                raise ConfigurationError(
                    "planning.scaffolded.diff.retention.max_age_days/max_files are required",
                    "Set diff retention values in config/default_config.yaml or .obra/config.yaml",
                )
            diff_root = Path(diff_path.format(intent_id="_placeholder")).expanduser().parent
            cleanup_retention(
                diff_root,
                max_age_days=int(diff_retention.get("max_age_days")),
                max_files=int(diff_retention.get("max_files")),
            )

        artifacts_dir = self._config.get("artifacts", {}).get("dir")
        if artifacts_dir:
            if "max_age_days" not in artifacts_retention or "max_files" not in artifacts_retention:
                raise ConfigurationError(
                    "planning.scaffolded.artifacts.retention.max_age_days/max_files are required",
                    "Set artifacts retention values in config/default_config.yaml or .obra/config.yaml",
                )
            cleanup_retention(
                Path(artifacts_dir),
                max_age_days=int(artifacts_retention.get("max_age_days")),
                max_files=int(artifacts_retention.get("max_files")),
            )

    def _get_stage_config(self, stage: str) -> dict[str, Any]:
        stages = self._config.get("stages")
        if not isinstance(stages, dict):
            raise ConfigurationError(
                "planning.scaffolded.stages must be a mapping",
                "Set planning.scaffolded.stages in config.",
            )
        stage_config = stages.get(stage)
        if not isinstance(stage_config, dict):
            raise ConfigurationError(
                f"planning.scaffolded.stages.{stage} must be a mapping",
                f"Set planning.scaffolded.stages.{stage} in config.",
            )
        return stage_config

    def _build_stream_handler(self, stage_name: str):
        if not self._on_stream:
            return None
        return lambda chunk: self._on_stream(stage_name, chunk)

    @staticmethod
    def _format_intent(intent: IntentModel) -> str:
        sections = [f"# Intent: {intent.problem_statement}", ""]
        sections.extend(_render_section("Assumptions", intent.assumptions))
        sections.extend(_render_section("Requirements", intent.requirements))
        sections.extend(_render_section("Constraints", intent.constraints))
        sections.extend(_render_section("Acceptance Criteria", intent.acceptance_criteria))
        sections.extend(_render_section("Non-Goals", intent.non_goals))
        sections.extend(_render_section("Risks", intent.risks))
        return "\n".join(sections)


def _render_section(title: str, items: list[str]) -> list[str]:
    if not items:
        return [f"## {title}", "", "- _None documented._", ""]
    return [f"## {title}", "", *(f"- {item}" for item in items), ""]


def _merge_unique(existing: list[str], additions: list[str] | None) -> list[str]:
    merged = list(existing)
    for item in additions or []:
        if item and item not in merged:
            merged.append(item)
    return merged
