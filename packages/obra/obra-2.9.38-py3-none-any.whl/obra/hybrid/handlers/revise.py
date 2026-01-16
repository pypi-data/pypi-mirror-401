"""Revise handler for Hybrid Orchestrator.

This module handles the REVISE action from the server. It revises the current
plan based on issues identified during examination.

The revision process:
    1. Receive RevisionRequest with issues to address
    2. Build revision prompt with issues and guidance
    3. Invoke LLM to generate revised plan
    4. Parse revised plan items
    5. Return RevisedPlan to report to server

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 1
    - obra/api/protocol.py
    - obra/hybrid/orchestrator.py
"""
# pylint: disable=duplicate-code

import json
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

from obra.api.protocol import RevisionRequest
from obra.display import print_info
from obra.hybrid.json_utils import (
    extract_json_payload,
    is_garbage_response,
    unwrap_claude_cli_json,
    unwrap_gemini_cli_json,
)
from obra.hybrid.prompt_enricher import PromptEnricher
from obra.llm.cli_runner import invoke_llm_via_cli

logger = logging.getLogger(__name__)


class ReviseHandler:  # pylint: disable=too-few-public-methods
    """Handler for REVISE action.

    Revises the current plan based on issues from examination.
    Returns updated plan items with changes summary.

    ## Architecture Context (ADR-027)

    This handler implements the two-tier prompting architecture where:
    - **Server (Tier 1)**: Generates strategic base prompts with revision guidance
    - **Client (Tier 2)**: Enriches base prompts with local tactical context

    **Implementation Flow**:
    1. Server sends RevisionRequest with base_prompt containing revision instructions
    2. Client enriches base_prompt via PromptEnricher (adds file structure, git log)
    3. Client invokes LLM with enriched prompt locally
    4. Client reports revised plan items and changes summary back to server

    ## IP Protection

    Strategic revision guidance (issue patterns, quality standards) stay on server.
    This protects Obra's proprietary quality assessment IP from client-side inspection.

    ## Privacy Protection

    Tactical context (file contents, git messages, errors) never sent to server.
    Only LLM revision results (revised plan and changes summary) is transmitted.

    See: docs/decisions/ADR-027-two-tier-prompting-architecture.md

    Example:
        >>> handler = ReviseHandler(Path("/path/to/project"))
        >>> request = RevisionRequest(
        ...     issues=[{"id": "I1", "description": "Missing error handling"}],
        ...     blocking_issues=[{"id": "I1", ...}]
        ... )
        >>> result = handler.handle(request)
        >>> print(result["plan_items"])
    """

    def __init__(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        self,
        working_dir: Path,
        on_stream: Callable[[str, str], None] | None = None,
        llm_config: dict[str, str] | None = None,
        log_event: Callable[..., None] | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
        monitoring_context: dict[str, Any] | None = None,
    ) -> None:
        """Initialize ReviseHandler.

        Args:
            working_dir: Working directory for file access
            on_stream: Optional callback for LLM streaming chunks (S3.T6)
            llm_config: Optional LLM configuration (S4.T4)
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

    def handle(self, request: RevisionRequest) -> dict[str, Any]:
        """Handle REVISE action.

        Args:
            request: RevisionRequest from server with base_prompt

        Returns:
            Dict with plan_items, changes_summary, and raw_response

        Raises:
            ValueError: If request.base_prompt is None (server must provide base_prompt)
        """
        logger.info("Revising plan to address %s issues", len(request.issues))
        print_info(
            f"Revising plan ({len(request.blocking_issues)} blocking issues)..."
        )

        # Validate base_prompt (server-side prompting required)
        if request.base_prompt is None:
            error_msg = (
                "RevisionRequest.base_prompt is None. Server must provide base prompt (ADR-027)."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Enrich base prompt with local tactical context
        enricher = PromptEnricher(self._working_dir)
        enriched_prompt = enricher.enrich(request.base_prompt)

        provider, model, thinking_level, auth_method = self._resolve_llm_config("anthropic")

        # Invoke LLM with enriched prompt
        raw_response = self._invoke_llm(
            enriched_prompt,
            provider=provider,
            model=model,
            thinking_level=thinking_level,
            auth_method=auth_method,
        )

        # Parse revised plan
        plan_items, changes_summary, parse_info = self._parse_revision(raw_response)
        if not plan_items:
            fallback_items, fallback_reason = self._extract_plan_from_prompt(enriched_prompt)
            if fallback_items:
                plan_items = fallback_items
                if not changes_summary:
                    changes_summary = "No valid revision produced; reusing previous plan items."
                parse_info["status"] = "fallback_previous_plan"
                parse_info["fallback_reason"] = fallback_reason

        self._log_parse_event(
            action="revise",
            provider=provider,
            model=model,
            parse_info=parse_info,
        )

        if self._should_retry_on_parse_failure(provider, model, parse_info):
            retry_prompt = self._build_retry_prompt(enriched_prompt)
            self._log_retry_event(
                action="revise",
                provider=provider,
                model=model,
                attempt=1,
                reason=parse_info.get("status", "unknown"),
            )
            raw_response = self._invoke_llm(
                retry_prompt,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                auth_method=auth_method,
            )
            plan_items, changes_summary, parse_info = self._parse_revision(raw_response)
            parse_info["retried"] = True
            self._log_parse_event(
                action="revise",
                provider=provider,
                model=model,
                parse_info=parse_info,
            )

        logger.info("Revised plan has %s items", len(plan_items))
        print_info(f"Revised plan: {len(plan_items)} items")

        return {
            "plan_items": plan_items,
            "changes_summary": changes_summary,
            "raw_response": raw_response,
        }

    def _invoke_llm(  # pylint: disable=too-many-arguments
        self,
        prompt: str,
        *,
        provider: str,
        model: str,
        thinking_level: str,
        auth_method: str = "oauth",
    ) -> str:
        """Invoke LLM for revision.

        Args:
            prompt: Revision prompt
            provider: LLM provider name
            model: LLM model name
            thinking_level: LLM thinking level
            auth_method: Authentication method ("oauth" or "api_key")

        Returns:
            Raw LLM response
        """
        logger.debug(
            "Invoking LLM via CLI for revision: provider=%s model=%s auth=%s",
            provider,
            model,
            auth_method,
        )

        def _stream(chunk: str) -> None:
            if self._on_stream:
                self._on_stream("llm_streaming", chunk)

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
                    log_event=self._log_event,
                    trace_id=self._trace_id,
                    parent_span_id=self._parent_span_id,
                    call_site="revise",
                    monitoring_context=self._monitoring_context,  # ISSUE-CLI-016/017 fix
                    skip_git_check=self._llm_config.get("git", {}).get("skip_check", False),  # GIT-HARD-001
                )
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.error("LLM invocation failed: %s", e)
            return json.dumps(
                {
                    "plan_items": [],
                    "changes_summary": f"LLM error: {e!s}",
                }
            )

    def _parse_revision(  # pylint: disable=too-many-locals,too-many-return-statements,too-many-branches,too-many-statements
        self,
        raw_response: str,
    ) -> tuple[list[dict[str, Any]], str, dict[str, Any]]:
        """Parse LLM response into revised plan.

        Args:
            raw_response: Raw LLM response

        Returns:
            Tuple of (plan_items, changes_summary, parse_info)
        """
        parse_info = {
            "status": "strict_json",
            "used_extraction": False,
            "response_length": len(raw_response or ""),
            "extraction_attempted": False,
            "extraction_succeeded": False,
        }

        response = (raw_response or "").strip()
        if not response:
            parse_info["status"] = "empty_response"
            return [], "", parse_info

        looks_like_json = (
            response.startswith("{")
            or response.startswith("[")
            or response.startswith("```")
        )
        if not looks_like_json:
            is_garbage, garbage_reason = is_garbage_response(response, return_reason=True)
            if is_garbage:
                parse_info["status"] = "garbage_response"
                parse_info["garbage_reason"] = garbage_reason
                logger.warning(
                    "Detected garbage response in revision (reason=%s). Preview: %s",
                    garbage_reason,
                    response[:200],
                )
                return [], "", parse_info

        try:
            normalized_response = response
            if normalized_response.startswith("```"):
                lines = normalized_response.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1] == "```" else len(lines)
                normalized_response = "\n".join(lines[start:end])

            data = json.loads(normalized_response)
        except json.JSONDecodeError as e:
            candidate = extract_json_payload(raw_response)
            if candidate and candidate != response:
                parse_info["status"] = "tolerant_json"
                parse_info["used_extraction"] = True
                data = json.loads(candidate)
            else:
                parse_info["status"] = "parse_error"
                parse_info["error"] = str(e)
                return self._fallback_with_extraction(raw_response, parse_info)

        # ISSUE-SAAS-030 FIX: Handle Claude CLI JSON wrapper format
        data, was_unwrapped = unwrap_claude_cli_json(data)
        if was_unwrapped:
            logger.debug("Detected Claude CLI JSON wrapper, extracted result field")
            parse_info["unwrapped_cli_json"] = True
            if isinstance(data, str):
                logger.warning(
                    "Claude CLI result is text, not JSON; attempting extraction fallback."
                )
                parse_info["status"] = "parse_error"
                return self._fallback_with_extraction(data, parse_info)
            # Otherwise data is dict/list, continue processing below

        data, was_gemini_unwrapped = unwrap_gemini_cli_json(data)
        if was_gemini_unwrapped:
            logger.debug("Detected Gemini CLI JSON wrapper, extracted response field")
            parse_info["unwrapped_gemini_json"] = True
            if isinstance(data, str):
                logger.warning(
                    "Gemini CLI result is text, not JSON; attempting extraction fallback."
                )
                parse_info["status"] = "parse_error"
                return self._fallback_with_extraction(data, parse_info)

        if isinstance(data, dict):
            items = data.get("plan_items", [])
            summary = data.get("changes_summary", "")
        elif isinstance(data, list):
            items = data
            summary = ""
        else:
            logger.warning("Unexpected response format")
            parse_info["status"] = "unexpected_format"
            return self._fallback_with_extraction(raw_response, parse_info)

        if not items:
            parse_info["status"] = "empty_items"
            return self._fallback_with_extraction(raw_response, parse_info)

        normalized = self._normalize_plan_items(items)
        return normalized, summary, parse_info

    def _normalize_plan_items(self, items: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Normalize plan items to expected structure with defaults."""
        normalized: list[dict[str, Any]] = []
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            title = item.get("title", "Untitled")
            description = item.get("description", "") or title
            normalized_item = {
                "id": item.get("id", f"T{i + 1}"),
                "item_type": item.get("item_type", "task"),
                "title": title,
                "description": description,
                "acceptance_criteria": item.get("acceptance_criteria", []),
                "dependencies": item.get("dependencies", []),
            }
            normalized.append(normalized_item)
        return normalized

    def _extract_plan_from_prompt(self, prompt: str) -> tuple[list[dict[str, Any]], str]:
        """Extract current plan items from the revision prompt if available."""
        start_marker = "BEGIN CURRENT PLAN JSON"
        end_marker = "END CURRENT PLAN JSON"
        start = prompt.find(start_marker)
        end = prompt.find(end_marker)
        if start == -1 or end == -1 or end <= start:
            return [], "missing_markers"

        json_block = prompt[start + len(start_marker):end].strip()
        try:
            data = json.loads(json_block)
        except json.JSONDecodeError:
            return [], "invalid_json"

        if isinstance(data, dict):
            items = data.get("plan_items", [])
        elif isinstance(data, list):
            items = data
        else:
            return [], "unexpected_format"

        normalized = self._normalize_plan_items(items)
        if not normalized:
            return [], "empty_items"
        return normalized, "parsed_current_plan"

    def _fallback_with_extraction(
        self,
        raw_response: str,  # noqa: ARG002 - kept for signature compatibility
        parse_info: dict[str, Any],
    ) -> tuple[list[dict[str, Any]], str, dict[str, Any]]:
        """Return no changes when JSON parsing fails.

        FIX-DERIVE-HANG-001: Removed LLM extraction fallback.

        Previously this method attempted LLM-based structure extraction using a
        "fast" tier model, which could hang for up to 600s (default timeout).
        For revise operations, returning "no changes" is a safe fallback - the
        existing plan remains unchanged.
        """
        parse_info["extraction_attempted"] = False
        parse_info["extraction_succeeded"] = False
        parse_info["status"] = "no_changes"

        logger.info("JSON parsing failed in revise - treating as no changes (extraction disabled)")
        return [], "", parse_info

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

    def _should_retry_on_parse_failure(  # pylint: disable=unused-argument
        self,
        provider: str,
        model: str,
        parse_info: dict[str, Any],
    ) -> bool:
        """REVISE parse failures should not retry; treat as no-op revisions."""
        return False

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
                extraction_attempted=parse_info.get("extraction_attempted", False),
                extraction_succeeded=parse_info.get("extraction_succeeded", False),
                retried=parse_info.get("retried", False),
                response_length=parse_info.get("response_length", 0),
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning("Failed to log parse event for %s: %s", action, e)

    def _log_retry_event(  # pylint: disable=too-many-arguments
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
        except Exception as e:  # pylint: disable=broad-exception-caught
            logger.warning("Failed to log parse retry event for %s: %s", action, e)


__all__ = ["ReviseHandler"]
