"""CLI-backed LLM invocation helpers for Obra.

Hybrid handlers (derive/examine/revise/execute) should be able to run using
provider CLIs (claude/codex/gemini) without requiring API keys.
"""

from __future__ import annotations

import contextlib
import logging
import subprocess
import tempfile
import threading
import time
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# ISSUE-CLI-016/CLI-017 FIX: Import MonitoringThread for liveness monitoring
# Now available directly from obra.monitoring (SaaS-spec)
from obra.monitoring.agent_monitor import MonitoringThread
from obra.hybrid.prompt_file import PromptFileManager

MONITORING_AVAILABLE = True


def _is_git_repository(path: Path) -> bool:
    """Check if path is within a git repository.

    FEAT-CLI-GIT-TRUST-001: Smart git detection for Codex CLI.
    """
    path = path.resolve()
    if (path / ".git").exists():
        return True
    return any((parent / ".git").exists() for parent in path.parents)


def _prepare_prompt(prompt: str, provider: str, thinking_level: str) -> str:
    if provider == "anthropic" and thinking_level == "maximum":
        return f"ultrathink: {prompt}"
    return prompt


def invoke_llm_via_cli(
    *,
    prompt: str,
    cwd: Path,
    provider: str,
    model: str,
    thinking_level: str,
    auth_method: str = "oauth",
    on_stream: Callable[[str], None] | None = None,
    output_schema: Path | None = None,
    timeout_s: int | None = None,
    log_event: Callable[..., None] | None = None,
    trace_id: str | None = None,
    parent_span_id: str | None = None,
    call_site: str | None = None,
    monitoring_context: dict[str, Any] | None = None,
    skip_git_check: bool = False,
) -> str:
    """Invoke an LLM via its provider CLI and return stdout as the model response.

    Args:
        prompt: The prompt to send to the LLM
        cwd: Working directory for the subprocess
        provider: LLM provider (anthropic, openai, google)
        model: Model identifier
        thinking_level: Thinking level (off, low, medium, high, maximum)
        auth_method: Authentication method ("oauth" or "api_key"). When "oauth",
            API key environment variables are stripped to ensure CLI uses OAuth.
            Default is "oauth" to prevent unexpected API billing.
        on_stream: Optional callback for streaming output
        output_schema: Optional JSON schema file for structured output (OpenAI)
        timeout_s: Timeout in seconds (default 600)
        log_event: Optional callback for logging events
        trace_id: Optional trace ID for observability
        parent_span_id: Optional parent span ID for observability
        call_site: Optional call site identifier for logging
        monitoring_context: Optional dict with keys: config, workspace_path,
            production_logger, session_id. If provided and monitoring is enabled,
            starts MonitoringThread for liveness checks and hang detection.
            Pattern from src/agents/claude_code_local.py:609-636 (ISSUE-CLI-016/017 fix).
        skip_git_check: Whether to add --skip-git-repo-check flag for OpenAI Codex
            (GIT-HARD-001). Default False. When True, bypasses git repository validation.
    """
    from obra.config import (
        build_llm_args,
        build_subprocess_env,
        get_agent_execution_timeout,
        get_llm_cli,
        get_prompt_retention,
    )

    timeout_s = timeout_s or get_agent_execution_timeout()
    prepared_prompt = _prepare_prompt(prompt, provider, thinking_level)
    cli_command = get_llm_cli(provider)
    start_time = time.time()
    span_id = uuid.uuid4().hex
    response_text = ""
    status = "success"
    error_message: str | None = None
    prompt_manager = PromptFileManager(cwd, retain=get_prompt_retention())
    removed_orphans = prompt_manager.cleanup_stale_prompt_artifacts()
    if removed_orphans:
        logger.debug("Removed %d orphaned prompt files", removed_orphans)
    prompt_path, prompt_instruction = prompt_manager.write_prompt(prepared_prompt)

    # build_llm_args expects a resolved config dict
    cli_args = build_llm_args(
        {"provider": provider, "model": model, "thinking_level": thinking_level}
    )

    # Build subprocess environment with auth-aware API key handling
    # When auth_method is "oauth", API keys are stripped to prevent unexpected billing
    subprocess_env = build_subprocess_env(auth_method)

    # Special-case Codex: for "text-only" orchestration prompts, keep it read-only and capture the
    # final message cleanly via --output-last-message.
    if provider == "openai":
        # Avoid the "workspace-write" behavior of --full-auto for orchestration prompts.
        with tempfile.NamedTemporaryFile(mode="w+", delete=False, encoding="utf-8") as f:
            output_path = f.name

        cmd = [
            cli_command,
            "exec",
            "-C",
            str(cwd),
            "--sandbox",
            "read-only",
            "--output-last-message",
            output_path,
        ]
        logger.debug("Codex workspace root set via -C: %s", cwd)

        # GIT-HARD-001: Add --skip-git-repo-check only when configured
        # Check skip_git_check parameter to determine if git validation should be bypassed
        # This replaces the hardcoded behavior from FEAT-CLI-GIT-TRUST-001
        if skip_git_check:
            cmd.append("--skip-git-repo-check")
            logger.debug(f"Codex: Adding --skip-git-repo-check (skip_git_check=True)")
        if output_schema:
            cmd.extend(["--output-schema", str(output_schema)])
        if model and model not in ("default", "auto"):
            cmd.extend(["--model", model])

        try:
            subprocess.run(
                [*cmd, prompt_instruction],
                cwd=cwd,
                text=True,
                encoding="utf-8",
                capture_output=True,
                timeout=timeout_s,
                check=False,
                env=subprocess_env,  # Auth-aware environment
            )
            response_text = Path(output_path).read_text(encoding="utf-8")
        except Exception as exc:
            status = "error"
            error_message = str(exc)
            raise
        finally:
            with contextlib.suppress(Exception):
                Path(output_path).unlink(missing_ok=True)
            prompt_manager.cleanup(prompt_path)
            _log_llm_call(
                log_event=log_event,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                prompt=prepared_prompt,
                response=response_text,
                start_time=start_time,
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id,
                call_site=call_site,
                status=status,
                error_message=error_message,
            )
        return response_text

    cmd = [cli_command, *cli_args, prompt_instruction]

    if not on_stream:
        # ADR-043: Use Popen + MonitoringThread for hang detection (not blocking subprocess.run)
        # This enables liveness checks even without streaming callbacks
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",  # Explicit UTF-8 to avoid Windows cp1252 issues
            env=subprocess_env,  # Auth-aware environment
        )

        # ADR-043: Initialize MonitoringThread if context provided
        # Same pattern as streaming path - enables hang detection for non-streaming calls
        monitor: Any | None = None
        if monitoring_context and MONITORING_AVAILABLE:
            try:
                config = monitoring_context.get("config")
                workspace_path = monitoring_context.get("workspace_path")
                production_logger = monitoring_context.get("production_logger")
                session_id = monitoring_context.get("session_id")

                # Support both dict configs (hybrid orchestrator) and object configs (legacy)
                if isinstance(config, dict):
                    monitoring_enabled = (
                        config
                        and "orchestration" in config
                        and "monitoring" in config["orchestration"]
                        and config["orchestration"]["monitoring"].get("enabled", False)
                    )
                else:
                    monitoring_enabled = (
                        config
                        and hasattr(config, "orchestration")
                        and hasattr(config.orchestration, "monitoring")
                        and config.orchestration.monitoring.enabled
                    )

                if monitoring_enabled and workspace_path and production_logger and session_id:
                    monitor = MonitoringThread(
                        process=proc,
                        config=config,
                        workspace_path=Path(workspace_path),
                        production_logger=production_logger,
                        session_id=session_id,
                        state_manager=None,  # Handlers don't have state_manager
                        task_id=None,  # Handlers don't have task_id
                        base_timeout=timeout_s,
                    )
                    monitor.start()
                    logger.info(
                        f"Monitoring thread started for non-streaming LLM call: PID={proc.pid}, "
                        f"provider={provider}, timeout={timeout_s}s"
                    )
            except Exception as e:
                logger.error(f"Failed to start monitoring thread: {e}", exc_info=True)
                monitor = None

        try:
            # Use communicate() for clean I/O handling with timeout
            stdout, stderr = proc.communicate(
                timeout=timeout_s,
            )
            if proc.returncode != 0:
                raise RuntimeError((stderr or stdout or "Unknown CLI error")[:500])
            response_text = stdout
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.communicate()  # Clean up zombie process
            status = "error"
            error_message = f"LLM CLI timed out after {timeout_s}s"
            raise RuntimeError(error_message)
        except Exception as exc:
            status = "error"
            error_message = str(exc)
            raise
        finally:
            # ADR-043: Stop monitoring thread if started
            if monitor:
                try:
                    monitor.stop(timeout=2.0)
                except Exception as e:
                    logger.warning(f"Error stopping monitoring thread: {e}")

            # Calculate token usage and display to user (SIM-FIX-001 continuation)
            if response_text and status == "success":
                from obra.display import print_info
                from obra.hybrid.json_utils import extract_usage_from_cli_response

                # Try to extract actual token counts from CLI response
                usage = extract_usage_from_cli_response(response_text)
                if usage["input_tokens"] > 0 or usage["output_tokens"] > 0:
                    # Use actual token counts from CLI
                    input_tokens = usage["input_tokens"]
                    output_tokens = usage["output_tokens"]
                    total_tokens = input_tokens + output_tokens
                    source = "CLI"
                else:
                    # Fall back to character-based estimation
                    input_tokens = len(prepared_prompt) // 4
                    output_tokens = len(response_text) // 4
                    total_tokens = input_tokens + output_tokens
                    source = "estimated"

                # Display token usage to stdout (always visible, even in non-verbose mode)
                print_info(f"Tokens: {total_tokens:,} (in: {input_tokens:,}, out: {output_tokens:,}) [{source}]")

            _log_llm_call(
                log_event=log_event,
                provider=provider,
                model=model,
                thinking_level=thinking_level,
                prompt=prepared_prompt,
                response=response_text,
                start_time=start_time,
                trace_id=trace_id,
                span_id=span_id,
                parent_span_id=parent_span_id,
                call_site=call_site,
                status=status,
                error_message=error_message,
            )

            # Cleanup Claude Code CLI temp files
            # - tmpclaude-*-cwd: Created to track cwd but not cleaned up
            # - nul: Windows NUL device written as literal file (Claude Code bug)
            if provider == "anthropic":
                for tmp_file in cwd.glob("tmpclaude-*-cwd"):
                    try:
                        tmp_file.unlink()
                    except OSError:
                        pass
                nul_file = cwd / "nul"
                if nul_file.exists() and nul_file.is_file():
                    try:
                        nul_file.unlink()
                    except OSError:
                        pass
            prompt_manager.cleanup(prompt_path)

        return response_text

    # Streaming path
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",  # Explicit UTF-8 to avoid Windows cp1252 issues
        env=subprocess_env,  # Auth-aware environment
    )

    # ISSUE-CLI-016/CLI-017 FIX: Initialize MonitoringThread if context provided
    # Pattern from src/agents/claude_code_local.py:608-636
    monitor: Any | None = None
    if monitoring_context and MONITORING_AVAILABLE:
        try:
            config = monitoring_context.get("config")
            workspace_path = monitoring_context.get("workspace_path")
            production_logger = monitoring_context.get("production_logger")
            session_id = monitoring_context.get("session_id")

            # Support both dict configs (hybrid orchestrator) and object configs (legacy)
            if isinstance(config, dict):
                monitoring_enabled = (
                    config
                    and "orchestration" in config
                    and "monitoring" in config["orchestration"]
                    and config["orchestration"]["monitoring"].get("enabled", False)
                )
                logger.debug(
                    f"Monitoring config (dict): enabled={monitoring_enabled}, "
                    f"has_context={bool(workspace_path and production_logger and session_id)}"
                )
            else:
                monitoring_enabled = (
                    config
                    and hasattr(config, "orchestration")
                    and hasattr(config.orchestration, "monitoring")
                    and config.orchestration.monitoring.enabled
                )
                logger.debug(
                    f"Monitoring config (object): enabled={monitoring_enabled}, "
                    f"has_context={bool(workspace_path and production_logger and session_id)}"
                )

            if monitoring_enabled and workspace_path and production_logger and session_id:
                monitor = MonitoringThread(
                    process=proc,
                    config=config,
                    workspace_path=Path(workspace_path),
                    production_logger=production_logger,
                    session_id=session_id,
                    state_manager=None,  # Handlers don't have state_manager
                    task_id=None,  # Handlers don't have task_id
                    base_timeout=timeout_s,
                )
                monitor.start()
                logger.info(
                    f"Monitoring thread started for LLM call: PID={proc.pid}, "
                    f"provider={provider}, timeout={timeout_s}s"
                )
            elif monitoring_enabled:
                logger.warning(
                    "Monitoring context incomplete: missing workspace_path, "
                    "production_logger, or session_id"
                )
        except Exception as e:
            logger.error(f"Failed to start monitoring thread: {e}", exc_info=True)
            monitor = None  # Ensure monitor is None if start failed

    # ISSUE-DOBRA-009: Start stderr reader thread to prevent pipe buffer deadlock
    # stderr must be consumed during execution, not after proc.wait()
    stderr_chunks: list[str] = []

    def stderr_reader() -> None:
        """Read stderr in background thread to prevent buffer deadlock."""
        try:
            if proc.stderr:
                for line in proc.stderr:
                    stderr_chunks.append(line)
        except (ValueError, OSError):
            pass  # Stream closed, process terminated

    stderr_thread = threading.Thread(target=stderr_reader, daemon=True)
    stderr_thread.start()

    assert proc.stdout is not None
    chunks: list[str] = []
    try:
        for line in proc.stdout:
            chunks.append(line)
            on_stream(line)
        proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        proc.kill()
        status = "error"
        error_message = str(exc)
        msg = f"LLM CLI timed out after {timeout_s}s"
        raise RuntimeError(msg)
    finally:
        # ADR-043: Stop monitoring thread if started
        if monitor:
            try:
                monitor.stop(timeout=2.0)
            except Exception as e:
                logger.warning(f"Error stopping monitoring thread: {e}")
        # ISSUE-DOBRA-009: Wait for stderr reader thread to finish
        stderr_thread.join(timeout=5)
        stderr = "".join(stderr_chunks)
        if proc.returncode not in (0, None) and status == "success":
            status = "error"
            error_message = (stderr or "Unknown CLI error")[:500]
        response_text = "".join(chunks)

        # Calculate token usage and display to user (SIM-FIX-001 continuation)
        if response_text and status == "success":
            from obra.display import print_info
            from obra.hybrid.json_utils import extract_usage_from_cli_response

            # Try to extract actual token counts from CLI response
            usage = extract_usage_from_cli_response(response_text)
            if usage["input_tokens"] > 0 or usage["output_tokens"] > 0:
                # Use actual token counts from CLI
                input_tokens = usage["input_tokens"]
                output_tokens = usage["output_tokens"]
                total_tokens = input_tokens + output_tokens
                source = "CLI"
            else:
                # Fall back to character-based estimation
                input_tokens = len(prepared_prompt) // 4
                output_tokens = len(response_text) // 4
                total_tokens = input_tokens + output_tokens
                source = "estimated"

            # Display token usage to stdout (always visible, even in non-verbose mode)
            print_info(f"Tokens: {total_tokens:,} (in: {input_tokens:,}, out: {output_tokens:,}) [{source}]")

        _log_llm_call(
            log_event=log_event,
            provider=provider,
            model=model,
            thinking_level=thinking_level,
            prompt=prepared_prompt,
            response=response_text,
            start_time=start_time,
            trace_id=trace_id,
            span_id=span_id,
            parent_span_id=parent_span_id,
            call_site=call_site,
            status=status,
            error_message=error_message,
        )

        # Cleanup Claude Code CLI temp files
        # - tmpclaude-*-cwd: Created to track cwd but not cleaned up
        # - nul: Windows NUL device written as literal file (Claude Code bug)
        if provider == "anthropic":
            for tmp_file in cwd.glob("tmpclaude-*-cwd"):
                try:
                    tmp_file.unlink()
                except OSError:
                    pass
            nul_file = cwd / "nul"
            if nul_file.exists() and nul_file.is_file():
                try:
                    nul_file.unlink()
                except OSError:
                    pass
        prompt_manager.cleanup(prompt_path)

    if proc.returncode != 0:
        # Use stderr collected by reader thread instead of blocking read
        status = "error"
        error_message = (stderr or "Unknown CLI error")[:500]
        raise RuntimeError(error_message)

    return "".join(chunks)


def _log_llm_call(
    *,
    log_event: Callable[..., None] | None,
    provider: str,
    model: str,
    thinking_level: str,
    prompt: str,
    response: str,
    start_time: float,
    trace_id: str | None,
    span_id: str,
    parent_span_id: str | None,
    call_site: str | None,
    status: str,
    error_message: str | None,
) -> None:
    """Emit a best-effort LLM call timing event."""
    if not log_event:
        return

    duration_ms = int((time.time() - start_time) * 1000)
    prompt_chars = len(prompt)
    response_chars = len(response)
    prompt_bytes = len(prompt.encode("utf-8"))
    response_bytes = len(response.encode("utf-8"))
    prompt_tokens = prompt_chars // 4
    response_tokens = response_chars // 4
    tokens_per_second = None
    if duration_ms > 0:
        tokens_per_second = (prompt_tokens + response_tokens) / (duration_ms / 1000)

    log_event(
        "llm_call",
        provider=provider,
        model=model,
        thinking_level=thinking_level,
        duration_ms=duration_ms,
        prompt_chars=prompt_chars,
        response_chars=response_chars,
        prompt_bytes=prompt_bytes,
        response_bytes=response_bytes,
        prompt_tokens=prompt_tokens,
        response_tokens=response_tokens,
        total_tokens=prompt_tokens + response_tokens,
        tokens_per_second=tokens_per_second,
        status=status,
        error_message=error_message,
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        call_site=call_site,
        token_estimate_source="chars_per_token",
    )
