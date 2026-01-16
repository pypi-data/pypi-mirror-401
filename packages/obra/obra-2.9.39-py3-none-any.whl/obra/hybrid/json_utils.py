"""Utilities for extracting JSON payloads from LLM responses."""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from obra.config.llm import resolve_tier_config
from obra.llm.cli_runner import invoke_llm_via_cli

EXTRACTION_PROMPT_TEMPLATE = """Extract plan items from this text as a JSON array.
Each item needs: id, title, description, acceptance_criteria (array), dependencies (array).
If the text contains no clear plan items, return an empty array [].
If items are numbered (1, 2, 3), use T1, T2, T3 as IDs.
Return ONLY valid JSON, no explanation or markdown.

Text to extract from:
---
{raw_response}
---

JSON array:
"""

logger = logging.getLogger(__name__)


def unwrap_claude_cli_json(data: dict[str, Any]) -> tuple[Any, bool]:
    """Unwrap Claude CLI JSON wrapper format.

    When Claude CLI is invoked with --output-format json, it returns a wrapper:
    {"type": "result", "result": "...", ...}

    This function extracts the actual LLM response from the "result" field.

    Args:
        data: Parsed JSON data that may be a Claude CLI wrapper

    Returns:
        Tuple of (unwrapped_data, was_wrapped) where:
        - unwrapped_data: The actual LLM response (parsed if JSON, or string)
        - was_wrapped: True if data was a Claude CLI wrapper

    ISSUE-SAAS-030: Fixes derivation returning empty plan items because
    the wrapper JSON was being treated as the plan instead of its result field.
    """
    if not isinstance(data, dict):
        return data, False

    # Check for Claude CLI wrapper signature
    if data.get("type") == "result" and "result" in data:
        result_content = data["result"]

        if isinstance(result_content, str):
            result_content = result_content.strip()
            # Remove markdown code blocks if present
            if result_content.startswith("```"):
                lines = result_content.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1] == "```" else len(lines)
                result_content = "\n".join(lines[start:end])
            # Try to parse as JSON
            try:
                return json.loads(result_content), True
            except json.JSONDecodeError:
                # Return as-is if not valid JSON
                return result_content, True

        elif isinstance(result_content, (dict, list)):
            return result_content, True

    return data, False


def extract_usage_from_cli_response(data: str | dict[str, Any]) -> dict[str, int]:
    """Extract token usage from Claude CLI JSON wrapper.

    When Claude CLI is invoked with --output-format json, it may include usage:
    {"type": "result", "result": "...", "usage": {"input_tokens": 123, "output_tokens": 456}}

    This function extracts the token counts from the usage field if present.

    Args:
        data: Either raw string output or parsed JSON data from CLI

    Returns:
        Dictionary with "input_tokens" and "output_tokens" keys.
        Returns 0 for both if usage data is not found.

    Related:
        - unwrap_claude_cli_json: Extracts result content from wrapper
        - obra/agents/base.py:_invoke_cli: Uses this for token reporting
    """
    # Parse string to dict if needed
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            # Not valid JSON, no usage data available
            return {"input_tokens": 0, "output_tokens": 0}

    if not isinstance(data, dict):
        return {"input_tokens": 0, "output_tokens": 0}

    # Extract usage field if present
    usage = data.get("usage", {})
    if not isinstance(usage, dict):
        return {"input_tokens": 0, "output_tokens": 0}

    return {
        "input_tokens": usage.get("input_tokens", 0),
        "output_tokens": usage.get("output_tokens", 0),
    }


def unwrap_gemini_cli_json(data: dict[str, Any]) -> tuple[Any, bool]:
    """Unwrap Gemini CLI JSON wrapper format.

    When Gemini CLI is invoked with --output-format json, it returns a wrapper:
    {"response": "...", "stats": {...}}

    This function extracts the actual LLM response from the "response" field.

    Args:
        data: Parsed JSON data that may be a Gemini CLI wrapper

    Returns:
        Tuple of (unwrapped_data, was_wrapped) where:
        - unwrapped_data: The actual LLM response (parsed if JSON, or string)
        - was_wrapped: True if data was a Gemini CLI wrapper

    FIX-GEMINI-UNWRAP-001: Adds Gemini-specific unwrapper to fix "Untitled"
    metadata in plan items when using Gemini CLI provider.
    """
    if not isinstance(data, dict):
        return data, False

    # Check for Gemini CLI wrapper signature: has "response" and "stats" keys
    if "response" in data and "stats" in data:
        response_content = data["response"]

        if isinstance(response_content, str):
            response_content = response_content.strip()
            # Remove markdown code blocks if present
            if response_content.startswith("```"):
                lines = response_content.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1] == "```" else len(lines)
                response_content = "\n".join(lines[start:end])
            # Try to parse as JSON (for structured prompts)
            try:
                return json.loads(response_content), True
            except json.JSONDecodeError:
                # Return as-is if not valid JSON
                return response_content, True

        elif isinstance(response_content, (dict, list)):
            return response_content, True

    return data, False


def extract_json_payload(text: str) -> str | None:
    """Extract a JSON object/array from a mixed response.

    Returns the first plausible JSON payload as a string, or None if not found.
    """
    trimmed = text.strip()
    if not trimmed:
        return None

    code_block = re.search(r"```(?:json)?\s*(.*?)```", trimmed, re.DOTALL)
    if code_block:
        candidate = code_block.group(1).strip()
        if candidate:
            return candidate

    for opener, closer in (("{", "}"), ("[", "]")):
        start = trimmed.find(opener)
        end = trimmed.rfind(closer)
        if start != -1 and end != -1 and end > start:
            return trimmed[start : end + 1].strip()

    return None


def _build_extraction_prompt(raw_response: str) -> str:
    """Build extraction prompt for LLM-based plan structure recovery."""
    return EXTRACTION_PROMPT_TEMPLATE.format(raw_response=raw_response.strip())


def is_garbage_response(text: str, return_reason: bool = False) -> bool | tuple[bool, str | None]:
    """Detect clearly unusable responses (errors, rate limits, gibberish).

    Handles CLI JSON wrappers (Claude, Gemini) by:
    1. Detecting wrapper format and checking is_error/error fields
    2. Extracting actual content from result/response field
    3. Running garbage detection on unwrapped content

    This prevents false positives when LLM-generated content contains
    error-like strings (e.g., "implement rate limiting for the API").

    Args:
        text: Response text to check
        return_reason: If True, returns tuple (is_garbage, reason) for observability

    Returns:
        If return_reason=False: bool indicating if response is garbage
        If return_reason=True: tuple of (is_garbage, reason_string_or_none)

    FIX-GARBAGE-WRAPPER-001: Unwrap CLI JSON before error marker detection
    to prevent false positives from content containing error-like strings.
    """
    cleaned = text.strip()
    if not cleaned:
        return (True, "empty_response") if return_reason else True

    # Handle CLI JSON wrappers (Claude, Gemini) - unwrap before checking content
    # This prevents false positives when LLM content contains error-like strings
    if cleaned.startswith("{"):
        try:
            data = json.loads(cleaned)
            if isinstance(data, dict):
                # Claude CLI wrapper: {"type": "result", "is_error": bool, "result": "..."}
                if data.get("type") == "result" and "result" in data:
                    if data.get("is_error"):
                        return (True, "cli_wrapper_error") if return_reason else True
                    # Successful response - extract content for checking
                    result = data.get("result", "")
                    if isinstance(result, str) and result.strip():
                        cleaned = result.strip()
                # Gemini CLI wrapper: {"response": "...", "stats": {...}}
                elif "response" in data and "stats" in data:
                    # Check for error in stats if present
                    stats = data.get("stats", {})
                    if isinstance(stats, dict) and stats.get("error"):
                        return (True, "cli_wrapper_error") if return_reason else True
                    # Extract response content
                    response = data.get("response", "")
                    if isinstance(response, str) and response.strip():
                        cleaned = response.strip()
        except json.JSONDecodeError:
            pass  # Not valid JSON, continue with original text

    # Exempt valid markdown/YAML patterns
    # YAML frontmatter: starts with ---
    if cleaned.startswith("---"):
        return (False, None) if return_reason else False

    # Markdown headers: starts with #
    if cleaned.startswith("#"):
        return (False, None) if return_reason else False

    lowered = cleaned.lower()
    error_markers = (
        "rate limit",
        "ratelimit",
        "too many requests",
        "exceeded your current quota",
        "quota exceeded",
        "please try again later",
        "invalid api key",
        "missing api key",
        "unauthorized",
        "forbidden",
        "temporarily unavailable",
        "error code",
        "http 429",
        "http 500",
    )
    for marker in error_markers:
        if marker in lowered:
            reason = f"error_marker:{marker}"
            return (True, reason) if return_reason else True

    compact = "".join(ch for ch in cleaned if not ch.isspace())
    if compact and " " not in cleaned and len(compact) > 48:
        reason = f"no_spaces_long_string:len={len(compact)}"
        return (True, reason) if return_reason else True

    non_word_ratio = sum(1 for ch in compact if not ch.isalnum()) / max(len(compact), 1)
    if non_word_ratio > 0.45 and len(compact) >= 12:
        reason = f"high_non_word_ratio:{non_word_ratio:.2f}"
        return (True, reason) if return_reason else True

    alpha_ratio = sum(1 for ch in compact if ch.isalpha()) / max(len(compact), 1)
    if alpha_ratio < 0.2 and len(compact) >= 12:
        reason = f"low_alpha_ratio:{alpha_ratio:.2f}"
        return (True, reason) if return_reason else True

    return (False, None) if return_reason else False


def _parse_extraction_response(response_text: str) -> list[dict[str, Any]] | None:
    """Parse extraction LLM response into plan item dictionaries."""
    try:
        parsed: Any = json.loads(response_text)
    except json.JSONDecodeError:
        payload = extract_json_payload(response_text)
        if not payload:
            return None
        try:
            parsed = json.loads(payload)
        except json.JSONDecodeError:
            return None

    if isinstance(parsed, dict):
        parsed, _ = unwrap_claude_cli_json(parsed)
        parsed, _ = unwrap_gemini_cli_json(parsed)

    if isinstance(parsed, str):
        try:
            parsed = json.loads(parsed)
        except json.JSONDecodeError:
            return None

    if not isinstance(parsed, list):
        return None

    items: list[dict[str, Any]] = []
    for item in parsed:
        if isinstance(item, dict):
            items.append(item)
        else:
            return None
    return items


def llm_extract_structure(
    raw_response: str,
    *,
    working_dir: Path,
    log_event: Callable[..., None] | None = None,
    trace_id: str | None = None,
    parent_span_id: str | None = None,
) -> tuple[list[dict[str, Any]] | None, bool]:
    """Extract structured plan items from a natural language response using an LLM."""
    is_garbage, garbage_reason = is_garbage_response(raw_response, return_reason=True)
    if is_garbage:
        logger.debug("Skipping LLM extraction for garbage response (reason=%s)", garbage_reason)
        return None, False

    normalized = raw_response.strip()
    prompt = _build_extraction_prompt(normalized)
    tier_config = resolve_tier_config("fast")

    try:
        response_text = invoke_llm_via_cli(
            prompt=prompt,
            cwd=working_dir,
            provider=tier_config["provider"],
            model=tier_config["model"],
            thinking_level=tier_config["thinking_level"],
            auth_method=tier_config["auth_method"],
            log_event=log_event,
            trace_id=trace_id,
            parent_span_id=parent_span_id,
            call_site="llm_extract_structure",
            skip_git_check=False,  # GIT-HARD-001: Utility function uses strict validation
        )
    except Exception as exc:
        logger.warning("LLM extraction failed: %s", exc)
        return None, False

    extracted_items = _parse_extraction_response(response_text)
    return extracted_items, extracted_items is not None
