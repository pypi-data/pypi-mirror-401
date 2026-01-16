"""Scaffolded plan review using expert-aligned prompts."""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from obra.config.llm import resolve_tier_config
from obra.exceptions import ConfigurationError
from obra.hybrid.json_utils import extract_json_payload, is_garbage_response
from obra.intent.prompts_scaffolded import build_review_prompt
from obra.intent.scaffolded_config import load_scaffolded_config
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


@dataclass
class ScaffoldedReviewResult:
    changes_required: bool
    issues: list[str]
    plan_items: list[dict[str, Any]] | None
    raw_response: str
    duration_s: float


class ScaffoldedPlanReviewer:
    """Run expert-aligned review of derived plan items."""

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
            logger.warning("Scaffolded review disabled due to config error: %s", exc)
            self._config = {"enabled": False}

    def is_enabled(self) -> bool:
        return bool(self._config.get("enabled", False))

    def review(
        self,
        objective: str,
        *,
        intent_markdown: str,
        plan_items: list[dict[str, Any]],
        intent_id: str | None = None,
    ) -> ScaffoldedReviewResult | None:
        if not self.is_enabled():
            return None
        stage_config = self._get_stage_config("review")
        if "max_passes" not in stage_config:
            raise ConfigurationError(
                "planning.scaffolded.stages.review.max_passes is required",
                "Set max_passes for the review stage in config.",
            )
        max_passes = int(stage_config.get("max_passes", 0))
        if max_passes < 1:
            return None

        model_tier = stage_config.get("model_tier")
        if not model_tier:
            raise ConfigurationError(
                "planning.scaffolded.stages.review.model_tier is required",
                "Set model_tier for the review stage in config.",
            )
        if "reasoning_level" not in stage_config:
            raise ConfigurationError(
                "planning.scaffolded.stages.review.reasoning_level is required",
                "Set reasoning_level for the review stage in config.",
            )
        if "timeout_s" not in stage_config:
            raise ConfigurationError(
                "planning.scaffolded.stages.review.timeout_s is required",
                "Set timeout_s for the review stage in config.",
            )
        reasoning_level = stage_config.get("reasoning_level")
        timeout_s = int(stage_config.get("timeout_s"))

        resolved = resolve_tier_config(
            model_tier,
            role="implementation",
            override_thinking_level=reasoning_level,
        )

        prompt = build_review_prompt(
            objective,
            intent_markdown,
            json.dumps(plan_items, indent=2),
        )

        attempt = 0
        last_response = ""
        start = time.time()
        while attempt < max_passes:
            raw_response = invoke_llm_via_cli(
                prompt=prompt,
                cwd=self._working_dir,
                provider=resolved["provider"],
                model=resolved["model"],
                thinking_level=resolved["thinking_level"],
                auth_method=resolved["auth_method"],
                on_stream=self._build_stream_handler(),
                timeout_s=timeout_s or None,
                log_event=self._log_event,
                trace_id=self._trace_id,
                parent_span_id=self._parent_span_id,
                call_site="scaffolded_review",
                monitoring_context=None,
                skip_git_check=self._llm_config.get("git", {}).get("skip_check", False),
            )
            response_text = _unwrap_cli_response(raw_response)
            last_response = response_text
            if response_text:
                is_garbage = is_garbage_response(response_text)
                if is_garbage:
                    logger.warning("Scaffolded review returned garbage response")
                    attempt += 1
                    continue

            payload = _parse_review_payload(response_text)
            if payload is None:
                attempt += 1
                continue
            duration = time.time() - start
            result = ScaffoldedReviewResult(
                changes_required=bool(payload.get("changes_required", False)),
                issues=_normalize_list(payload.get("issues")),
                plan_items=_normalize_plan_items(payload.get("plan_items")),
                raw_response=response_text,
                duration_s=duration,
            )
            self._write_artifact(intent_id, response_text)
            self._log_telemetry(result, intent_id=intent_id)
            return result

        duration = time.time() - start
        if last_response:
            self._write_artifact(intent_id, last_response)
            self._log_telemetry(
                ScaffoldedReviewResult(False, [], None, last_response, duration),
                intent_id=intent_id,
            )
        return ScaffoldedReviewResult(False, [], None, last_response, duration)

    def _write_artifact(self, intent_id: str | None, response_text: str) -> None:
        if not intent_id or not response_text:
            return
        artifacts_config = self._config.get("artifacts", {})
        artifacts_dir = artifacts_config.get("dir")
        if not artifacts_dir:
            return
        root = Path(artifacts_dir).expanduser() / intent_id
        root.mkdir(parents=True, exist_ok=True)
        path = root / "review.md"
        path.write_text(response_text, encoding="utf-8")

    def _log_telemetry(self, result: ScaffoldedReviewResult, *, intent_id: str | None) -> None:
        telemetry_config = self._config.get("telemetry", {})
        if not telemetry_config.get("enabled", False):
            return
        if not intent_id:
            return
        output_path = telemetry_config.get("output_path")
        if not output_path:
            raise ConfigurationError(
                "planning.scaffolded.telemetry.output_path is required",
                "Set planning.scaffolded.telemetry.output_path in config.",
            )
        include_content = bool(telemetry_config.get("include_content", False))
        payload = {
            "intent_id": intent_id,
            "stages": [
                {
                    "stage": "review",
                    "duration_s": result.duration_s,
                    "parsed_keys": ["changes_required", "issues", "plan_items"],
                    **({"raw_response": result.raw_response} if include_content else {}),
                }
            ],
        }
        log_scaffolded_event(Path(output_path), payload)

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

    def _build_stream_handler(self):
        if not self._on_stream:
            return None
        return lambda chunk: self._on_stream("scaffolded_review", chunk)


def _parse_review_payload(response_text: str) -> dict[str, Any] | None:
    if not response_text:
        return None
    payload_text = extract_json_payload(response_text)
    if not payload_text:
        return None
    try:
        parsed = json.loads(payload_text)
    except json.JSONDecodeError:
        return None
    if not isinstance(parsed, dict):
        return None
    if "changes_required" not in parsed:
        return None
    return parsed


def _normalize_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value]
    if value:
        return [str(value)]
    return []


def _normalize_plan_items(value: Any) -> list[dict[str, Any]] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        return None
    return [item for item in value if isinstance(item, dict)]
