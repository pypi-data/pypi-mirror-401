"""Examine handler for Hybrid Orchestrator.

This module handles the EXAMINE action from the server. It examines the current
plan using LLM to identify issues that need to be addressed.

The examination process:
    1. Receive ExamineRequest with plan to examine
    2. Build examination prompt with IP-protected criteria from server
    3. Invoke LLM with extended thinking if required
    4. Parse structured issues from response
    5. Return ExaminationReport to report to server

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 1
    - obra/api/protocol.py
    - obra/hybrid/orchestrator.py
"""

import json
import logging
import tempfile
from collections.abc import Callable
from pathlib import Path
from typing import Any, cast

from obra.api.protocol import ExamineRequest
from obra.display import print_info
from obra.hybrid.json_utils import (
    extract_json_payload,
    unwrap_claude_cli_json,
    unwrap_gemini_cli_json,
)
from obra.hybrid.prompt_enricher import PromptEnricher
from obra.llm.cli_runner import invoke_llm_via_cli
from obra.model_registry import get_default_model, validate_model

# Import enums from server schema for type-safe category and severity values
try:
    from functions.src.state.session_schema import ExaminationIssueCategory, Priority
except ImportError:
    # Fallback if server schema not available (shouldn't happen in normal operation)
    Priority = None
    ExaminationIssueCategory = None

logger = logging.getLogger(__name__)


class ExamineHandler:
    """Handler for EXAMINE action.

    Examines the current plan using LLM to identify issues.
    Issues are categorized and assigned severity levels.

    ## Architecture Context (ADR-027)

    This handler implements the two-tier prompting architecture where:
    - **Server (Tier 1)**: Generates strategic base prompts with examination criteria
    - **Client (Tier 2)**: Enriches base prompts with local tactical context

    **Implementation Flow**:
    1. Server sends ExamineRequest with base_prompt containing examination criteria
    2. Client enriches base_prompt via PromptEnricher (adds file structure, git log)
    3. Client invokes LLM with enriched prompt locally
    4. Client reports issues back to server for validation

    ## IP Protection

    Strategic examination criteria (quality standards, issue patterns) stay on server.
    This protects Obra's proprietary quality assessment IP from client-side inspection.

    ## Privacy Protection

    Tactical context (file contents, git messages, errors) never sent to server.
    Only LLM examination results (issues summary) is transmitted.

    See: docs/decisions/ADR-027-two-tier-prompting-architecture.md

    Example:
        >>> handler = ExamineHandler(Path("/path/to/project"))
        >>> request = ExamineRequest(
        ...     plan_version_id="v1",
        ...     plan_items=[{"id": "T1", "title": "Task 1", ...}]
        ... )
        >>> result = handler.handle(request)
        >>> print(result["issues"])
    """

    def __init__(
        self,
        working_dir: Path,
        on_stream: Callable[[str, str], None] | None = None,
        llm_config: dict[str, Any] | None = None,
        log_event: Callable[..., None] | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        monitoring_context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ExamineHandler.

        Args:
            working_dir: Working directory for file access
            on_stream: Optional callback for LLM streaming chunks (S3.T6)
            llm_config: Optional LLM configuration (S4.T3)
            log_event: Optional logger for hybrid events (ISSUE-OBS-002)
            monitoring_context: Optional monitoring context for liveness checks (ISSUE-CLI-016/017 fix)
        """
        self._working_dir = working_dir
        self._on_stream = on_stream
        self._llm_config = llm_config or {}
        self._log_event = log_event
        self._trace_id = trace_id
        self._parent_span_id = parent_span_id
        self._monitoring_context = monitoring_context

    def handle(self, request: ExamineRequest) -> dict[str, Any]:
        """Handle EXAMINE action.

        Args:
            request: ExamineRequest from server with base_prompt

        Returns:
            Dict with issues, thinking_budget_used, and raw_response

        Raises:
            ValueError: If request.base_prompt is None (server must provide base_prompt)
        """
        logger.info(f"Examining plan version: {request.plan_version_id}")
        print_info(f"Examining plan ({len(request.plan_items)} items)...")

        # Validate base_prompt (server-side prompting required)
        if request.base_prompt is None:
            error_msg = (
                "ExamineRequest.base_prompt is None. Server must provide base prompt (ADR-027)."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Enrich base prompt with local tactical context
        enricher = PromptEnricher(self._working_dir)
        enriched_prompt = enricher.enrich(request.base_prompt)

        provider, model, thinking_level, auth_method = self._resolve_llm_config("anthropic")
        resolved_thinking_level = thinking_level if request.thinking_required else "off"

        # Invoke LLM with thinking if required
        raw_response, thinking_used, thinking_fallback = self._invoke_llm(
            enriched_prompt,
            provider=provider,
            model=model,
            thinking_level=resolved_thinking_level,
            auth_method=auth_method,
        )

        # Parse issues from response
        issues, parse_info = self._parse_issues(raw_response, provider=provider)
        self._log_parse_event(
            action="examine",
            provider=provider,
            model=model,
            parse_info=parse_info,
        )

        if self._should_retry_on_parse_failure(provider, model, parse_info):
            retry_prompt = self._build_retry_prompt(enriched_prompt)
            self._log_retry_event(
                action="examine",
                provider=provider,
                model=model,
                attempt=1,
                reason=parse_info.get("status", "unknown"),
            )
            raw_response, thinking_used, thinking_fallback = self._invoke_llm(
                retry_prompt,
                provider=provider,
                model=model,
                thinking_level=resolved_thinking_level,
                auth_method=auth_method,
            )
            issues, parse_info = self._parse_issues(raw_response, provider=provider)
            parse_info["retried"] = True
            self._log_parse_event(
                action="examine",
                provider=provider,
                model=model,
                parse_info=parse_info,
            )

        logger.info(f"Found {len(issues)} issues")
        print_info(f"Found {len(issues)} issues")

        # Log blocking issues
        blocking = [i for i in issues if i.get("severity") in ("P0", "P1", "critical", "high")]
        if blocking:
            logger.info(f"  Blocking issues: {len(blocking)}")
            print_info(f"  Blocking issues: {len(blocking)}")

        return {
            "issues": issues,
            "thinking_budget_used": thinking_used,
            "thinking_fallback": thinking_fallback,
            "raw_response": raw_response,
            "iteration": 0,  # Server tracks iteration
        }

    def _invoke_llm(
        self,
        prompt: str,
        *,
        provider: str,
        model: str,
        thinking_level: str,
        auth_method: str = "oauth",
    ) -> tuple[str, int, bool]:
        """Invoke LLM for examination.

        Args:
            prompt: Examination prompt
            provider: LLM provider name
            model: LLM model name
            thinking_level: Thinking level (standard, high, max)
            auth_method: Authentication method ("oauth" or "api_key")

        Returns:
            Tuple of (raw_response, thinking_tokens_used, thinking_fallback)
        """
        logger.debug(
            f"Invoking LLM via CLI: provider={provider} model={model} "
            f"thinking_level={thinking_level} auth={auth_method}"
        )

        def _stream(chunk: str) -> None:
            if self._on_stream:
                self._on_stream("llm_streaming", chunk)

        try:
            schema_path = None
            if provider == "openai":
                valid_categories = self._valid_issue_categories()
                schema = {
                    "type": "object",
                    "properties": {
                        "issues": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "string"},
                                    "category": {"type": "string", "enum": valid_categories},
                                    "severity": {"type": "string"},
                                    "description": {"type": "string"},
                                    "affected_items": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                },
                                "required": [
                                    "id",
                                    "category",
                                    "severity",
                                    "description",
                                    "affected_items",
                                ],
                                "additionalProperties": False,
                            },
                        }
                    },
                    "required": ["issues"],
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
                response = invoke_llm_via_cli(
                    prompt=prompt,
                    cwd=self._working_dir,
                    provider=provider,
                    model=model,
                    thinking_level=thinking_level,
                    auth_method=auth_method,
                    on_stream=_stream if self._on_stream else None,
                    output_schema=schema_path,
                    log_event=self._log_event,
                    trace_id=self._trace_id,
                    parent_span_id=self._parent_span_id,
                    call_site="examine",
                    monitoring_context=self._monitoring_context,  # ISSUE-CLI-016/017 fix
                    skip_git_check=self._llm_config.get("git", {}).get("skip_check", False),  # GIT-HARD-001
                )
            finally:
                if schema_path:
                    schema_path.unlink(missing_ok=True)
            return response, 0, False
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}")
            return json.dumps({"issues": []}), 0, False

    def _parse_issues(
        self, raw_response: str, provider: str | None = None
    ) -> tuple[list[dict[str, Any]], dict[str, Any]]:
        """Parse LLM response into issues list.

        Args:
            raw_response: Raw LLM response
            provider: Optional provider name for debugging (FIX-GEMINI-UNWRAP-001)

        Returns:
            List of issue dictionaries
        """
        parse_info: dict[str, Any] = {
            "status": "strict_json",
            "response_length": len(raw_response),
            "used_extraction": False,
            "category_coercions": 0,
        }
        # FIX-GEMINI-UNWRAP-001: Add provider to parse_info for debugging
        if provider:
            parse_info["provider"] = provider

        # FIX-GEMINI-UNWRAP-001: Debug logging for raw LLM response
        # Helps diagnose parsing issues with different providers
        if raw_response:
            truncated = raw_response[:500] + "..." if len(raw_response) > 500 else raw_response
            logger.debug(f"Raw LLM response (first 500 chars): {truncated}")

        try:
            # Try to extract JSON from response
            response = raw_response.strip()

            if response.startswith("```"):
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
                    # ISSUE-CLI-015 FIX: Early return when JSON extraction fails
                    # Following pattern from derive.py:320-327
                    logger.warning(f"Failed to parse issues JSON: {e}")
                    parse_info["status"] = "parse_error_fallback"
                    parse_info["error"] = str(e)
                    return [], parse_info

            # ISSUE-SAAS-030 FIX: Handle Claude CLI JSON wrapper format
            data, was_unwrapped = unwrap_claude_cli_json(data)
            if was_unwrapped:
                logger.debug("Detected Claude CLI JSON wrapper, extracted result field")
                parse_info["unwrapped_cli_json"] = True
                if isinstance(data, str):
                    # Unwrapped result is text, not JSON - no issues to parse
                    logger.warning("Claude CLI result is text, not JSON; assuming no issues.")
                    parse_info["status"] = "coerced_text"
                    return [], parse_info
                # Otherwise data is dict/list, continue processing below

            # FIX-GEMINI-UNWRAP-001: Handle Gemini CLI JSON wrapper format
            # When Gemini CLI is used, it wraps the response as {"response": "...", "stats": {...}}
            data, was_gemini_unwrapped = unwrap_gemini_cli_json(data)
            if was_gemini_unwrapped:
                logger.debug("Detected Gemini CLI JSON wrapper, extracted response field")
                parse_info["unwrapped_gemini_json"] = True
                if isinstance(data, str):
                    # Unwrapped result is text, not JSON - no issues to parse
                    logger.warning(
                        "Gemini CLI response is text, not JSON; assuming no issues."
                    )
                    parse_info["status"] = "coerced_text"
                    return [], parse_info
                # Otherwise data is dict/list, continue processing below

            # Extract issues
            if isinstance(data, dict) and "issues" in data:
                issues = data["issues"]
            elif isinstance(data, list):
                issues = data
            else:
                logger.warning("Unexpected response format")
                parse_info["status"] = "empty_fallback"
                return [], parse_info

            # Validate and normalize issues
            normalized = []
            for i, issue in enumerate(issues):
                # ISSUE-CLI-014 FIX: Handle non-dict issue items (e.g., strings)
                # Some LLMs may return strings instead of dicts
                if isinstance(issue, str):
                    # Convert string to minimal issue dict
                    normalized_issue = {
                        "id": f"I{i + 1}",
                        "category": "other",
                        "severity": "low",
                        "description": issue,
                        "affected_items": [],
                    }
                elif isinstance(issue, dict):
                    # Normal dict case - extract fields with defaults
                    raw_category = issue.get("category", "")
                    normalized_category, coerced = self._normalize_category(raw_category)
                    if coerced:
                        parse_info["category_coercions"] += 1
                        examples = parse_info.setdefault(
                            "category_coercions_examples",
                            [],
                        )
                        if len(examples) < 3:
                            examples.append(raw_category or "<empty>")
                    normalized_issue = {
                        "id": issue.get("id", f"I{i + 1}"),
                        "category": normalized_category,
                        "severity": self._normalize_severity(issue.get("severity", "low")),
                        "description": issue.get("description", ""),
                        "affected_items": issue.get("affected_items", []),
                    }
                else:
                    # Unexpected type - convert to string description
                    logger.warning(f"Unexpected issue type: {type(issue)}, converting to string")
                    normalized_issue = {
                        "id": f"I{i + 1}",
                        "category": "other",
                        "severity": "low",
                        "description": str(issue),
                        "affected_items": [],
                    }
                normalized.append(normalized_issue)

            return normalized, parse_info

        except json.JSONDecodeError as e:
            logger.warning(f"Failed to parse issues JSON: {e}")
            parse_info["status"] = "parse_error_fallback"
            parse_info["error"] = str(e)
            return [], parse_info

    def _normalize_severity(self, severity: str) -> str:
        """Normalize severity string to Priority enum values.

        Maps common severity strings to server's Priority enum (P0-P3).
        This ensures type-safe communication with the server.

        Args:
            severity: Raw severity string from LLM

        Returns:
            Priority enum value (P0, P1, P2, P3)
        """
        severity_lower = severity.lower()

        # Map to Priority enum values (single source of truth)
        mapping = {
            # Critical severity
            "critical": Priority.P0.value if Priority else "P0",
            "p0": Priority.P0.value if Priority else "P0",
            "blocker": Priority.P0.value if Priority else "P0",
            # High severity
            "high": Priority.P1.value if Priority else "P1",
            "p1": Priority.P1.value if Priority else "P1",
            "major": Priority.P1.value if Priority else "P1",
            # Medium severity
            "medium": Priority.P2.value if Priority else "P2",
            "p2": Priority.P2.value if Priority else "P2",
            "minor": Priority.P2.value if Priority else "P2",
            # Low severity
            "low": Priority.P3.value if Priority else "P3",
            "p3": Priority.P3.value if Priority else "P3",
            "trivial": Priority.P3.value if Priority else "P3",
        }

        return mapping.get(severity_lower, Priority.P3.value if Priority else "P3")

    def _normalize_category(self, category: str) -> tuple[str, bool]:
        """Normalize category string to ExaminationIssueCategory enum values.

        Maps common category variations to server's ExaminationIssueCategory enum.
        This ensures type-safe communication with the server.

        Args:
            category: Raw category string from LLM

        Returns:
            Tuple of (normalized category, coerced)
        """
        if not isinstance(category, str):
            category = "" if category is None else str(category)
        category_lower = category.lower().strip()

        # Map to ExaminationIssueCategory enum values (single source of truth)
        if ExaminationIssueCategory:
            mapping = {
                # Scope variations
                "scope": ExaminationIssueCategory.SCOPE.value,
                "requirement": ExaminationIssueCategory.SCOPE.value,
                "requirements": ExaminationIssueCategory.SCOPE.value,
                # Completeness variations
                "completeness": ExaminationIssueCategory.COMPLETENESS.value,
                "complete": ExaminationIssueCategory.COMPLETENESS.value,
                "missing": ExaminationIssueCategory.COMPLETENESS.value,
                "incomplete": ExaminationIssueCategory.COMPLETENESS.value,
                # Clarity variations
                "clarity": ExaminationIssueCategory.CLARITY.value,
                "unclear": ExaminationIssueCategory.CLARITY.value,
                "ambiguous": ExaminationIssueCategory.CLARITY.value,
                "ambiguity": ExaminationIssueCategory.CLARITY.value,
                # Dependencies variations
                "dependencies": ExaminationIssueCategory.DEPENDENCIES.value,
                "dependency": ExaminationIssueCategory.DEPENDENCIES.value,
                "deps": ExaminationIssueCategory.DEPENDENCIES.value,
                # Feasibility variations
                "feasibility": ExaminationIssueCategory.FEASIBILITY.value,
                "feasible": ExaminationIssueCategory.FEASIBILITY.value,
                "complexity": ExaminationIssueCategory.FEASIBILITY.value,
                # Security variations
                "security": ExaminationIssueCategory.SECURITY.value,
                "sec": ExaminationIssueCategory.SECURITY.value,
                # Testing variations
                "testing": ExaminationIssueCategory.TESTING.value,
                "test": ExaminationIssueCategory.TESTING.value,
                "tests": ExaminationIssueCategory.TESTING.value,
                # Documentation variations
                "documentation": ExaminationIssueCategory.DOCUMENTATION.value,
                "doc": ExaminationIssueCategory.DOCUMENTATION.value,
                "docs": ExaminationIssueCategory.DOCUMENTATION.value,
                # Other/default
                "other": ExaminationIssueCategory.OTHER.value,
                "misc": ExaminationIssueCategory.OTHER.value,
                "miscellaneous": ExaminationIssueCategory.OTHER.value,
            }
            default_value = ExaminationIssueCategory.OTHER.value
            normalized = str(mapping.get(category_lower, default_value))
            coerced = category_lower not in mapping
            return normalized, coerced
        # Fallback if enum not available
        mapping = {
            "scope": "scope",
            "requirement": "scope",
            "requirements": "scope",
            "completeness": "completeness",
            "complete": "completeness",
            "missing": "completeness",
            "incomplete": "completeness",
            "clarity": "clarity",
            "unclear": "clarity",
            "ambiguous": "clarity",
            "ambiguity": "clarity",
            "dependencies": "dependencies",
            "dependency": "dependencies",
            "deps": "dependencies",
            "feasibility": "feasibility",
            "feasible": "feasibility",
            "complexity": "feasibility",
            "security": "security",
            "sec": "security",
            "testing": "testing",
            "test": "testing",
            "tests": "testing",
            "documentation": "documentation",
            "doc": "documentation",
            "docs": "documentation",
            "other": "other",
            "misc": "other",
            "miscellaneous": "other",
        }
        normalized = str(mapping.get(category_lower, "other"))
        coerced = category_lower not in mapping
        return normalized, coerced

    def _resolve_llm_config(self, default_provider: str) -> tuple[str, str, str, str]:
        """Resolve LLM configuration from stored config.

        Returns:
            Tuple of (provider, model, thinking_level, auth_method)
        """
        resolved_provider = self._llm_config.get("provider", default_provider)
        model = self._llm_config.get("model", "default")
        thinking_level = self._llm_config.get("thinking_level", "medium")
        auth_method = self._llm_config.get("auth_method", "oauth")
        return resolved_provider, model, thinking_level, auth_method

    def _normalize_model(self, provider: str, model: str) -> str | None:
        if not model or model in ("default", "auto"):
            return cast(str | None, get_default_model(provider))
        return model

    def _valid_issue_categories(self) -> list[str]:
        if ExaminationIssueCategory:
            return [category.value for category in ExaminationIssueCategory]
        return [
            "scope",
            "completeness",
            "clarity",
            "dependencies",
            "feasibility",
            "security",
            "testing",
            "documentation",
            "other",
        ]


    def _should_retry_on_parse_failure(
        self,
        provider: str,
        model: str,
        parse_info: dict[str, Any],
    ) -> bool:
        if parse_info.get("status") not in ("empty_fallback", "parse_error_fallback"):
            return False

        if not self._llm_config.get("parse_retry_enabled", True):
            return False

        parse_retry_providers = self._llm_config.get("parse_retry_providers")
        if parse_retry_providers is None:
            parse_retry_providers = ["openai"]
        if isinstance(parse_retry_providers, str):
            parse_retry_providers = [parse_retry_providers]
        if provider not in parse_retry_providers:
            return False

        parse_retry_models = self._llm_config.get("parse_retry_models")
        if parse_retry_models:
            if isinstance(parse_retry_models, str):
                parse_retry_models = [parse_retry_models]
            normalized_model = self._normalize_model(provider, model)
            if not normalized_model:
                return False
            if normalized_model not in parse_retry_models:
                return False

            validation = validate_model(provider, normalized_model)
            if not validation.valid:
                logger.warning("Parse retry model rejected by registry: %s", validation.error)
                return False

        return True

    def _build_retry_prompt(self, prompt: str) -> str:
        return (
            f"{prompt}\n\n"
            "Return only valid JSON for the response schema. "
            "Do not include prose, markdown, or code fences."
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


__all__ = ["ExamineHandler"]
