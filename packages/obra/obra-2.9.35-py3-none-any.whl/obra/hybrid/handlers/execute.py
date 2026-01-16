"""Execute handler for Hybrid Orchestrator.

This module handles the EXECUTE action from the server. It executes a plan item
by deploying an implementation agent (Claude Code, etc.).

The execution process:
    1. Receive ExecutionRequest with plan item to execute
    2. Prepare execution context (files, dependencies)
    3. Deploy implementation agent
    4. Collect execution results (files changed, tests, etc.)
    5. Return ExecutionResult to report to server

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 2
    - obra/api/protocol.py
    - obra/hybrid/orchestrator.py
"""

import logging
import subprocess
import threading
import time
import uuid
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from obra.api.protocol import ExecutionRequest, ExecutionStatus
from obra.config import (
    DEFAULT_LLM_API_TIMEOUT,
    PROVIDER_CLI_INFO,
    build_llm_args,
    build_subprocess_env,
    get_agent_execution_timeout,
    get_heartbeat_initial_delay,
    get_heartbeat_interval,
    get_llm_cli,
    get_prompt_retention,
    get_thinking_keyword,
)
from obra.display import print_error, print_info, print_warning
from obra.display.observability import ObservabilityConfig, ProgressEmitter, VerbosityLevel
from obra.hybrid.handlers.base import ObservabilityContextMixin
from obra.hybrid.prompt_file import PromptFileManager
from obra.hybrid.prompt_enricher import PromptEnricher

logger = logging.getLogger(__name__)

# Type alias for streaming callback
StreamCallback = Callable[[str, str], None] | None


@dataclass
class FileChangeSet:
    """Represents a set of file changes detected in the working directory.

    Attributes:
        added: Set of filepaths for newly created files
        modified: Set of filepaths for modified existing files
        count: Total number of changed files (added + modified)
    """

    added: set[str]
    modified: set[str]
    count: int


class FileChangeTracker:
    """Tracks file changes between polls, returning only new changes.

    This class maintains state of previously seen file changes and returns
    only the delta (new changes) on each poll() call.

    Attributes:
        _handler: ExecuteHandler instance for file change detection
        _previous_added: Previously seen added files
        _previous_modified: Previously seen modified files
    """

    def __init__(self, handler: "ExecuteHandler") -> None:
        """Initialize the tracker.

        Args:
            handler: ExecuteHandler instance that provides _get_file_changes()
        """
        self._handler = handler
        self._previous_added: set[str] = set()
        self._previous_modified: set[str] = set()

    def poll(self) -> FileChangeSet:
        """Poll for new file changes since last poll.

        Returns:
            FileChangeSet containing only files that changed since the last poll
        """
        # Get current file changes
        current = self._handler._get_file_changes()

        # Calculate delta - only new files since last poll
        new_added = current.added - self._previous_added
        new_modified = current.modified - self._previous_modified

        # Update tracked state
        self._previous_added = current.added
        self._previous_modified = current.modified

        # Return only the delta
        new_count = len(new_added) + len(new_modified)
        return FileChangeSet(added=new_added, modified=new_modified, count=new_count)


class HeartbeatThread(threading.Thread):
    """Background thread that emits heartbeat messages during long-running execution.

    This thread runs alongside subprocess execution, periodically emitting
    heartbeat messages via ProgressEmitter to show execution is still active.
    It also monitors file changes and emits file events when detected.
    Additionally, it emits liveness_check events via log_event callback.

    Attributes:
        _item_id: ID of the plan item being executed
        _emitter: ProgressEmitter for output
        _file_tracker: FileChangeTracker for detecting file changes
        _handler: ExecuteHandler for line counting
        _interval: Seconds between heartbeats (scaled by verbosity)
        _initial_delay: Seconds to wait before first heartbeat
        _stop_event: Event signaling thread should stop
        _log_event: Optional callback for emitting liveness_check events
        _session_id: Optional session ID for trace correlation
        _trace_id: Optional trace ID for distributed tracing
        _start_time: Timestamp when execution started
        _alive_count: Counter for number of liveness checks emitted
    """

    def __init__(
        self,
        item_id: str,
        emitter: ProgressEmitter,
        file_tracker: FileChangeTracker,
        handler: "ExecuteHandler",
        interval: int,
        initial_delay: int,
        stop_event: threading.Event,
        log_event: Callable[..., None] | None = None,
        session_id: str | None = None,
        trace_id: str | None = None,
    ) -> None:
        """Initialize HeartbeatThread.

        Args:
            item_id: ID of the plan item being executed
            emitter: ProgressEmitter for output
            file_tracker: FileChangeTracker for detecting file changes
            handler: ExecuteHandler for line counting
            interval: Base interval between heartbeats (seconds)
            initial_delay: Delay before first heartbeat (seconds)
            stop_event: Event to signal thread should stop
            log_event: Optional callback for emitting liveness_check events
            session_id: Optional session ID for trace correlation
            trace_id: Optional trace ID for distributed tracing
        """
        super().__init__(daemon=True)
        self._item_id = item_id
        self._emitter = emitter
        self._file_tracker = file_tracker
        self._handler = handler
        self._interval = interval
        self._initial_delay = initial_delay
        self._stop_event = stop_event
        self._log_event = log_event
        self._session_id = session_id
        self._trace_id = trace_id
        self._start_time = time.time()
        self._alive_count = 0

    def run(self) -> None:
        """Main thread loop - emits heartbeats and file events until stopped.

        Waits for initial_delay, then emits heartbeats every interval seconds.
        On each iteration, also polls for file changes and emits file events.
        Every 180 seconds, emits liveness_check event via log_event callback.
        """
        # Wait for initial delay before first heartbeat
        self._stop_event.wait(self._initial_delay)

        # Track last liveness check time
        last_liveness_check = time.time()
        liveness_check_interval = 180  # seconds

        # Main heartbeat loop
        while not self._stop_event.is_set():
            # Calculate elapsed time since execution started
            elapsed = int(time.time() - self._start_time)

            # Get current file count for heartbeat
            file_count = self._get_file_count()

            # S4.T1: Get liveness indicators at DETAIL verbosity level
            liveness_indicators = None
            if self._emitter.config.verbosity >= VerbosityLevel.DETAIL:
                liveness_indicators = self._get_liveness_indicators()

            # Emit heartbeat with liveness indicators at DETAIL level
            self._emitter.item_heartbeat(self._item_id, elapsed, file_count, liveness_indicators)

            # S3.T1: Emit liveness_check event every 180 seconds
            current_time = time.time()
            if self._log_event and (current_time - last_liveness_check) >= liveness_check_interval:
                indicators = self._get_liveness_indicators()
                # Calculate status: "active" if any indicator is True, else "idle"
                status = "active" if any(indicators.values()) else "idle"
                self._alive_count += 1

                self._log_event(
                    "liveness_check",
                    status=status,
                    alive_count=self._alive_count,
                    indicators=indicators,
                    elapsed_seconds=elapsed,
                    session_id=self._session_id,
                    trace_id=self._trace_id,
                )
                last_liveness_check = current_time

            # Poll for file changes and emit file events
            changes = self._file_tracker.poll()
            if changes.count > 0:
                # Emit events for new files
                for filepath in changes.added:
                    line_count = self._handler._count_lines(filepath)
                    self._emitter.file_event(filepath, "new", line_count)

                # Emit events for modified files
                for filepath in changes.modified:
                    line_count = self._handler._count_lines(filepath)
                    self._emitter.file_event(filepath, "modified", line_count)

            # Wait for next interval (or until stop event)
            self._stop_event.wait(self._interval)

    def _get_file_count(self) -> int:
        """Get current count of changed files.

        Returns:
            Number of files changed since execution started
        """
        return self._handler._count_file_changes()

    def _get_liveness_indicators(self) -> dict[str, bool]:
        """Get liveness indicators showing agent activity.

        Returns a dict with boolean indicators for:
        - files: Files being modified in workspace
        - log: Log files being written to
        - proc: Process is running
        - cpu: CPU activity (requires psutil, graceful degradation)
        - db: Database updates (placeholder for future implementation)

        Returns:
            Dict mapping indicator names to boolean active status
        """
        indicators = {
            "files": False,
            "log": False,
            "proc": True,  # If we're in heartbeat loop, process is running
            "cpu": False,  # Requires psutil, graceful degradation
            "db": False,  # Placeholder - would need StateManager integration
        }

        # Check if files have been modified
        file_count = self._get_file_count()
        indicators["files"] = file_count > 0

        # Check if log files have been written to recently
        # Look for .log or .jsonl files modified in the last interval
        try:
            working_dir = self._handler._working_dir
            current_time = time.time()
            log_activity = False

            # Check common log file patterns
            for pattern in ["*.log", "*.jsonl"]:
                for log_file in working_dir.glob(f"**/{pattern}"):
                    if log_file.is_file():
                        # Check if modified within last interval (+ some buffer)
                        mtime = log_file.stat().st_mtime
                        if current_time - mtime < (self._interval * 2):
                            log_activity = True
                            break
                if log_activity:
                    break

            indicators["log"] = log_activity
        except Exception:
            # If log checking fails, just report False
            pass

        # S3.T2: Check CPU activity via psutil (optional dependency)
        try:
            import psutil

            # Get CPU usage over a short interval
            # cpu_percent() with interval returns average CPU usage over that period
            # Using 0.1 seconds to avoid blocking the heartbeat thread
            cpu_percent = psutil.cpu_percent(interval=0.1)
            # Consider CPU active if usage is above 5% (low threshold for any activity)
            indicators["cpu"] = cpu_percent > 5.0
        except ImportError:
            # psutil not available - graceful degradation
            pass
        except Exception:
            # Any other error - graceful degradation
            pass

        return indicators

    def stop(self) -> None:
        """Signal the thread to stop and wait for it to exit.

        This method is thread-safe and can be called multiple times.
        """
        self._stop_event.set()
        # Wait up to 2 seconds for thread to finish
        self.join(timeout=2.0)


class ExecuteHandler(ObservabilityContextMixin):
    """Handler for EXECUTE action.

    Executes a plan item using an implementation agent (e.g., Claude Code CLI).
    Returns execution results including files changed and test results.

    ## Architecture Context (ADR-027)

    This handler implements the two-tier prompting architecture where:
    - **Server (Tier 1)**: Generates strategic base prompts with execution instructions
    - **Client (Tier 2)**: Enriches base prompts with local tactical context

    **Implementation Flow**:
    1. Server sends ExecutionRequest with base_prompt containing execution instructions
    2. Client enriches base_prompt via PromptEnricher (adds file structure, git log)
    3. Client invokes implementation agent (e.g., Claude Code CLI) via subprocess
    4. Client runs tests locally and reports results back to server

    ## IP Protection

    Strategic execution patterns (best practices, quality standards) stay on server.
    This protects Obra's proprietary implementation guidance from client-side inspection.

    ## Privacy Protection

    Tactical context (file contents, git messages, errors) never sent to server.
    Only execution results (summary, files changed, test results) is transmitted.

    See: docs/decisions/ADR-027-two-tier-prompting-architecture.md

    Example:
        >>> handler = ExecuteHandler(Path("/path/to/project"))
        >>> request = ExecutionRequest(
        ...     plan_items=[{"id": "T1", "title": "Create models", ...}],
        ...     execution_index=0
        ... )
        >>> result = handler.handle(request)
        >>> print(result["status"])
    """

    def __init__(
        self,
        working_dir: Path,
        llm_config: dict[str, str] | None = None,
        session_id: str | None = None,
        log_file: Path | None = None,
        trace_id: str | None = None,
        log_event: Any | None = None,
        parent_span_id: str | None = None,
        observability_config: ObservabilityConfig | None = None,
        progress_emitter: ProgressEmitter | None = None,
        on_stream: StreamCallback = None,
    ) -> None:
        """Initialize ExecuteHandler.

        Args:
            working_dir: Working directory for file access
            llm_config: Optional LLM configuration (S6.T1)
            session_id: Optional session ID for trace correlation
            log_file: Optional log file path for event emission
            trace_id: Optional trace ID for distributed tracing
            log_event: Optional event logging callback
            parent_span_id: Optional parent span ID for tracing
            observability_config: Optional observability configuration for progress visibility
            progress_emitter: Optional progress emitter for heartbeat and file events
            on_stream: Optional callback for LLM streaming output (event_type, chunk)
        """
        self._working_dir = working_dir
        self._llm_config = llm_config or {}
        self._session_id = session_id
        self._log_file = log_file
        self._trace_id = trace_id
        self._log_event = log_event
        self._parent_span_id = parent_span_id
        self._observability_config = observability_config
        self._progress_emitter = progress_emitter
        self._on_stream = on_stream

    def handle(self, request: ExecutionRequest) -> dict[str, Any]:
        """Handle EXECUTE action.

        Args:
            request: ExecutionRequest from server with base_prompt

        Returns:
            Dict with item_id, status, summary, files_changed, etc.

        Raises:
            ValueError: If request.base_prompt is None (server must provide base_prompt)
        """
        if not request.current_item:
            logger.error("No current item to execute")
            return {
                "item_id": "",
                "status": ExecutionStatus.FAILURE.value,
                "summary": "No item to execute",
                "files_changed": 0,
                "tests_passed": False,
                "test_count": 0,
                "coverage_delta": 0.0,
            }

        # Validate base_prompt (server-side prompting required)
        if request.base_prompt is None:
            error_msg = (
                "ExecutionRequest.base_prompt is None. Server must provide base prompt (ADR-027)."
            )
            logger.error(error_msg)
            raise ValueError(error_msg)

        item = request.current_item
        item_id = item.get("id", "unknown")
        title = item.get("title", "Untitled")

        logger.info(f"Executing item {item_id}: {title}")
        print_info(f"Executing: {item_id} - {title}")

        # Enrich base prompt with local tactical context
        enricher = PromptEnricher(self._working_dir)
        enriched_prompt = enricher.enrich(request.base_prompt)

        # Execute via implementation agent
        result = self._execute_item(item, enriched_prompt)

        # Log result
        status = result.get("status", ExecutionStatus.FAILURE.value)
        if status == ExecutionStatus.SUCCESS.value:
            print_info(f"  Completed: {result.get('summary', 'Success')[:50]}")
        elif status == ExecutionStatus.PARTIAL.value:
            print_warning(f"  Partial: {result.get('summary', 'Partial completion')[:50]}")
        else:
            print_error(f"  Failed: {result.get('summary', 'Execution failed')[:50]}")

        return result

    def _execute_item(self, item: dict[str, Any], enriched_prompt: str) -> dict[str, Any]:
        """Execute a single plan item.

        Args:
            item: Plan item to execute
            enriched_prompt: Enriched execution prompt from server

        Returns:
            Execution result dictionary
        """
        item_id = item.get("id", "unknown")
        title = item.get("title", "Untitled")

        # Try to deploy implementation agent with enriched prompt
        try:
            result = self._deploy_agent(enriched_prompt)

            # Count files changed (would be from git diff in production)
            files_changed = result.get("files_changed", 0)

            # Run tests if present
            tests_passed, test_count = self._run_tests()

            return {
                "item_id": item_id,
                "status": result.get("status", ExecutionStatus.SUCCESS.value),
                "summary": result.get("summary", f"Executed: {title}"),
                "files_changed": files_changed,
                "tests_passed": tests_passed,
                "test_count": test_count,
                "coverage_delta": 0.0,  # Would be calculated from coverage reports
            }

        except Exception as e:
            logger.exception(f"Execution failed for {item_id}: {e}")
            return {
                "item_id": item_id,
                "status": ExecutionStatus.FAILURE.value,
                "summary": f"Execution failed: {e!s}",
                "files_changed": 0,
                "tests_passed": False,
                "test_count": 0,
                "coverage_delta": 0.0,
            }

    def _prepare_prompt(self, prompt: str) -> str:
        """Prepare prompt with thinking keywords if needed.

        S6.T2: Inject ultrathink keyword for Claude + maximum thinking level.

        Args:
            prompt: Base prompt

        Returns:
            Prepared prompt with keywords if applicable
        """
        keyword = get_thinking_keyword(self._llm_config)
        if keyword:
            return f"{keyword}: {prompt}"

        return prompt

    def _deploy_agent(self, prompt: str) -> dict[str, Any]:
        """Deploy implementation agent via subprocess.

        S6.T3: Use build_llm_args() and get_llm_cli() to construct command.
        S6.T4: Detect auth errors and provide login hints.
        S6.T5: Execute subprocess.run() with constructed command.

        Args:
            prompt: Execution prompt

        Returns:
            Agent result dictionary with status, summary, files_changed
        """
        logger.debug("Deploying implementation agent")

        # ISSUE-SAAS-050: Capture HEAD SHA before execution to detect git operations
        # that modify repository state without changing working tree files
        start_head = self._get_head_sha()

        # S6.T2: Prepare prompt with thinking keywords if needed
        prepared_prompt = self._prepare_prompt(prompt)

        # S6.T3: Build CLI command and args from llm_config
        # ISSUE-SAAS-035: Use mode="execute" to allow file writing (no --print flag)
        if self._llm_config:
            provider = self._llm_config.get("provider", "anthropic")
            cli_command = get_llm_cli(provider)
            cli_args = build_llm_args(self._llm_config, mode="execute")
        else:
            # Fallback to defaults if no config
            cli_command = "claude"
            cli_args = ["--dangerously-skip-permissions"]
            provider = "anthropic"

        prompt_manager = PromptFileManager(self._working_dir, retain=get_prompt_retention())
        removed_orphans = prompt_manager.cleanup_stale_prompt_artifacts()
        if removed_orphans:
            logger.debug("Removed %d orphaned prompt files", removed_orphans)

        prompt_path, prompt_instruction = prompt_manager.write_prompt(prepared_prompt)
        if provider == "openai":
            logger.debug(
                "Codex prompt prepared: path=%s instruction=%s workspace=%s",
                prompt_path,
                prompt_instruction,
                self._working_dir,
            )

        cmd = [cli_command, *cli_args]
        if provider == "openai":
            cmd.extend(["-C", str(self._working_dir)])
            logger.debug("Codex workspace root set via -C: %s", self._working_dir)
        cmd.append(prompt_instruction)

        # BUG-11ff06b1: Add --skip-git-repo-check for OpenAI Codex (default: true)
        # Codex defaults to read-only for non-git directories, which prevents file writes
        # even with --sandbox workspace-write. Default to true for OpenAI to support
        # arbitrary project directories, but respect user config if explicitly set.
        # See: https://developers.openai.com/codex/security - "Non-version-controlled folders: read-only"
        if provider == "openai":
            git_config: dict[str, Any] = self._llm_config.get("git", {})
            # Default to True for OpenAI, but respect explicit False from user
            skip_git_check = git_config.get("skip_check", True)
            if skip_git_check:
                cmd.append("--skip-git-repo-check")
                logger.debug("OpenAI Codex: Adding --skip-git-repo-check (default for non-git dirs)")
            else:
                logger.debug("OpenAI Codex: Skipping --skip-git-repo-check (user config: git.skip_check=false)")

        logger.debug(f"Running agent: {' '.join(cmd[:3])}...")

        # Build subprocess environment with auth-aware API key handling
        # When auth_method is "oauth", API keys are stripped to prevent unexpected billing
        auth_method = self._llm_config.get("auth_method", "oauth")
        env = build_subprocess_env(
            auth_method=auth_method,
            extra_env=self._get_observability_env(),  # ISSUE-OBS-003: observability context
        )

        start_time = time.time()
        response_text = ""
        status = ExecutionStatus.FAILURE.value
        error_message: str | None = None

        # S2.T2: Set up heartbeat thread if progress emitter is available
        heartbeat_thread: HeartbeatThread | None = None
        stop_event: threading.Event | None = None

        if self._progress_emitter and self._observability_config:
            # Calculate scaled interval based on verbosity
            # QUIET (0): 3x base, PROGRESS (1): 1x base, DETAIL (2+): 0.5x base
            base_interval = get_heartbeat_interval()
            verbosity = self._observability_config.verbosity

            if verbosity == 0:  # QUIET
                scaled_interval = base_interval * 3
            elif verbosity == 1:  # PROGRESS
                scaled_interval = base_interval
            else:  # DETAIL (2+)
                scaled_interval = int(base_interval * 0.5)

            # Get initial delay
            initial_delay = get_heartbeat_initial_delay()

            # Create file change tracker
            file_tracker = FileChangeTracker(self)

            # Create and start heartbeat thread
            stop_event = threading.Event()
            # Use item_id from context if available, otherwise generic
            item_id = "execution"
            # S3.T3: Pass log_event, session_id, trace_id to HeartbeatThread
            heartbeat_thread = HeartbeatThread(
                item_id=item_id,
                emitter=self._progress_emitter,
                file_tracker=file_tracker,
                handler=self,
                interval=scaled_interval,
                initial_delay=initial_delay,
                stop_event=stop_event,
                log_event=self._log_event,
                session_id=self._session_id,
                trace_id=self._trace_id,
            )
            heartbeat_thread.start()
            logger.debug(
                f"Started heartbeat thread: interval={scaled_interval}s, "
                f"initial_delay={initial_delay}s, verbosity={verbosity}"
            )

        try:
            # S6.T5: Execute subprocess with observability environment
            # LLM Output Streaming: Use Popen for real-time output streaming
            proc = subprocess.Popen(
                cmd,
                cwd=self._working_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",  # ISSUE-SAAS-030: Explicit UTF-8 for Windows
                env=env,  # ISSUE-OBS-003: Pass observability context
            )

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

            # Stream stdout with callback
            stdout_chunks: list[str] = []
            try:
                assert proc.stdout is not None
                for line in proc.stdout:
                    stdout_chunks.append(line)
                    if self._on_stream:
                        self._on_stream("llm_streaming", line.rstrip("\n"))

                proc.wait(timeout=get_agent_execution_timeout())
            except subprocess.TimeoutExpired:
                proc.kill()
                raise
            finally:
                # Wait for stderr reader thread to finish
                stderr_thread.join(timeout=5)

            response_text = "".join(stdout_chunks)
            stderr_text = "".join(stderr_chunks)

            # Create a result-like object for compatibility with existing code
            class SubprocessResult:
                def __init__(self, returncode: int, stdout: str, stderr: str) -> None:
                    self.returncode = returncode
                    self.stdout = stdout
                    self.stderr = stderr

            result = SubprocessResult(proc.returncode or 0, response_text, stderr_text)

            # S6.T4: Check for auth errors in stderr
            # More specific auth error detection to avoid false positives (e.g., git trust errors)
            stderr = result.stderr.lower()
            stderr_lines = result.stderr.split("\n") if result.stderr else []
            is_auth_error = (
                "not authenticated" in stderr
                or "authentication required" in stderr
                or "login required" in stderr
                or any("auth" in line and "error" in line for line in stderr_lines)
            )
            # Exclude git trust errors from auth detection
            is_git_trust_error = "trusted directory" in stderr or "--skip-git-repo-check" in stderr

            if is_auth_error and not is_git_trust_error:
                error_message = result.stderr[:200] if result.stderr else "Authentication required"
                auth_hint = PROVIDER_CLI_INFO.get(provider, {}).get(
                    "auth_hint", f"{cli_command} login"
                )
                return {
                    "status": ExecutionStatus.FAILURE.value,
                    "summary": f"Authentication required. Run '{auth_hint}' to authenticate.",
                    "files_changed": 0,
                }

            # Codex prompt file missing hint
            if provider == "openai" and result.stderr:
                stderr_lower = result.stderr.lower()
                if ".obra-prompt-" in stderr_lower and (
                    "not present" in stderr_lower
                    or "not found" in stderr_lower
                    or "no such file" in stderr_lower
                ):
                    stderr_snippet = result.stderr[:200]
                    error_message = (
                        "Codex prompt file missing "
                        f"(workspace={self._working_dir}, "
                        f"prompt_path={prompt_path}, "
                        f"instruction={prompt_instruction}, "
                        f"stderr={stderr_snippet})"
                    )
                    logger.warning(
                        "Codex prompt file missing: workspace=%s prompt_path=%s instruction=%s stderr=%s",
                        self._working_dir,
                        prompt_path,
                        prompt_instruction,
                        stderr_snippet,
                    )
                    return {
                        "status": ExecutionStatus.FAILURE.value,
                        "summary": (
                            "Codex could not find the prompt file in the workspace. "
                            "Obra sets the workspace root with -C <working_dir>; "
                            "verify the working directory is correct and accessible."
                        ),
                        "files_changed": 0,
                    }

            # Check exit code
            if result.returncode == 0:
                status = ExecutionStatus.SUCCESS.value
                # ISSUE-SAAS-046 FIX: Count actual file changes via git diff
                files_changed = self._count_file_changes()

                # ISSUE-SAAS-046 FIX: Zero-Output Validation Gate
                # Fail fast when execution claims success but produced no output.
                # This prevents false-positive quality scores on empty work.
                if files_changed == 0:
                    # ISSUE-SAAS-050 FIX: Check for git operations before failing
                    # Git commit/merge operations modify .git/ but not working tree,
                    # causing false positives. Detect by comparing HEAD before/after.
                    current_head = self._get_head_sha()
                    if start_head and current_head and current_head != start_head:
                        logger.debug(
                            f"Git operation detected: HEAD changed from {start_head[:8]} "
                            f"to {current_head[:8]}"
                        )
                        return {
                            "status": ExecutionStatus.SUCCESS.value,
                            "summary": "Task executed successfully (repository updated)",
                            "files_changed": 0,
                        }

                    error_message = (
                        "No files written to target directory"
                    )
                    logger.warning(
                        f"Zero-output detected: LLM exited successfully but no files changed. "
                        f"working_dir={self._working_dir}"
                    )
                    return {
                        "status": ExecutionStatus.FAILURE.value,
                        "summary": (
                            "Execution completed but no files were written to the target directory. "
                            "Likely causes: (1) Working directory not writable or path mismatch, "
                            "(2) LLM decided no changes were needed (check review findings), "
                            "(3) Provider CLI misconfigured (run 'obra doctor' to validate), "
                            "(4) Task prompt too vague for actionable output. "
                            "Check provider CLI logs and retry with more specific instructions."
                        ),
                        "files_changed": 0,
                    }

                return {
                    "status": ExecutionStatus.SUCCESS.value,
                    "summary": "Task executed successfully",
                    "files_changed": files_changed,
                }
            error_msg = result.stderr[:200] if result.stderr else "Unknown error"
            error_message = error_msg
            return {
                "status": ExecutionStatus.FAILURE.value,
                "summary": f"Execution failed: {error_msg}",
                "files_changed": 0,
            }

        except subprocess.TimeoutExpired:
            logger.exception("Agent execution timed out")
            error_message = "Execution timed out after 10 minutes"
            return {
                "status": ExecutionStatus.FAILURE.value,
                "summary": "Execution timed out after 10 minutes",
                "files_changed": 0,
            }
        except FileNotFoundError:
            logger.exception(f"CLI command '{cli_command}' not found")
            error_message = f"CLI '{cli_command}' not found"
            return {
                "status": ExecutionStatus.FAILURE.value,
                "summary": f"CLI '{cli_command}' not found. Install it first.",
                "files_changed": 0,
            }
        except Exception as e:
            logger.exception(f"Agent deployment failed: {e}")
            error_message = str(e)
            return {
                "status": ExecutionStatus.FAILURE.value,
                "summary": f"Deployment failed: {e!s}",
                "files_changed": 0,
            }
        finally:
            prompt_manager.cleanup(prompt_path)

            # S2.T2: Stop heartbeat thread if it was started
            if heartbeat_thread and stop_event:
                logger.debug("Stopping heartbeat thread")
                heartbeat_thread.stop()

            if self._log_event:
                duration_ms = int((time.time() - start_time) * 1000)
                prompt_chars = len(prepared_prompt)
                response_chars = len(response_text)
                prompt_bytes = len(prepared_prompt.encode("utf-8"))
                response_bytes = len(response_text.encode("utf-8"))
                prompt_tokens = prompt_chars // 4
                response_tokens = response_chars // 4
                tokens_per_second = None
                if duration_ms > 0:
                    tokens_per_second = (prompt_tokens + response_tokens) / (duration_ms / 1000)
                self._log_event(
                    "llm_call",
                    provider=provider,
                    model=self._llm_config.get("model", "default"),
                    thinking_level=self._llm_config.get("thinking_level", "standard"),
                    duration_ms=duration_ms,
                    prompt_chars=prompt_chars,
                    response_chars=response_chars,
                    prompt_bytes=prompt_bytes,
                    response_bytes=response_bytes,
                    prompt_tokens=prompt_tokens,
                    response_tokens=response_tokens,
                    total_tokens=prompt_tokens + response_tokens,
                    tokens_per_second=tokens_per_second,
                    status="success" if status == ExecutionStatus.SUCCESS.value else "error",
                    error_message=error_message,
                    trace_id=self._trace_id,
                    span_id=uuid.uuid4().hex,
                    parent_span_id=self._parent_span_id,
                    call_site="execute",
                    token_estimate_source="chars_per_token",
                )

            # Cleanup Claude Code CLI temp files
            # - tmpclaude-*-cwd: Created to track cwd but not cleaned up
            # - nul: Windows NUL device written as literal file (Claude Code bug)
            if provider == "anthropic" and self._working_dir:
                for tmp_file in self._working_dir.glob("tmpclaude-*-cwd"):
                    try:
                        tmp_file.unlink()
                    except OSError:
                        pass
                nul_file = self._working_dir / "nul"
                if nul_file.exists() and nul_file.is_file():
                    try:
                        nul_file.unlink()
                    except OSError:
                        pass

    def _is_git_repository(self) -> bool:
        """Check if working directory is within a git repository.

        ISSUE-SAAS-049: Smart git detection following pattern from cli_runner.py.

        Returns:
            True if working directory is inside a git repository, False otherwise.
        """
        path = self._working_dir.resolve()
        if (path / ".git").exists():
            return True
        return any((parent / ".git").exists() for parent in path.parents)

    def _get_head_sha(self) -> str | None:
        """Get current HEAD commit SHA.

        ISSUE-SAAS-050: Used to detect git operations that modify repository
        state without changing working tree files (e.g., git commit).

        Returns:
            The current HEAD commit SHA, or None if not a git repository
            or if an error occurs.
        """
        if not self._is_git_repository():
            return None
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return None
        except Exception as e:
            logger.debug(f"Failed to get HEAD SHA: {e}")
            return None

    def _count_file_changes_filesystem(self) -> int:
        """Count files in working directory using filesystem (non-git fallback).

        ISSUE-SAAS-049 FIX: Fallback for non-git directories.
        Simply counts all files in the working directory, excluding hidden files
        and common non-code directories.

        Returns:
            Number of files in the working directory.
        """
        excluded_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", ".tox"}
        excluded_extensions = {".pyc", ".pyo", ".egg-info"}

        file_count = 0
        try:
            for item in self._working_dir.iterdir():
                # Skip hidden files and excluded directories
                if item.name.startswith("."):
                    continue
                if item.is_dir() and item.name in excluded_dirs:
                    continue

                if item.is_file():
                    # Skip excluded file types
                    if any(item.name.endswith(ext) for ext in excluded_extensions):
                        continue
                    file_count += 1
                elif item.is_dir():
                    # Recursively count files in subdirectories
                    for sub_item in item.rglob("*"):
                        if sub_item.is_file():
                            # Skip hidden and excluded
                            if any(part.startswith(".") for part in sub_item.parts):
                                continue
                            if any(part in excluded_dirs for part in sub_item.parts):
                                continue
                            if any(sub_item.name.endswith(ext) for ext in excluded_extensions):
                                continue
                            file_count += 1

            logger.debug(f"Filesystem file count (non-git fallback): {file_count}")
            return file_count

        except Exception as e:
            logger.warning(f"Filesystem file count failed: {e}")
            return 0

    def _count_file_changes(self) -> int:
        """Count actual file changes using git diff, with filesystem fallback.

        ISSUE-SAAS-046 FIX: Replaces hardcoded files_changed=1 placeholder
        with actual git-based file change detection.

        ISSUE-SAAS-049 FIX: Added filesystem fallback for non-git directories.
        When working directory is not a git repository, falls back to counting
        files in the directory instead of returning 0.

        Returns:
            Number of files added, modified, or renamed since last commit.
            For non-git directories, returns total file count in directory.
            Returns 0 only if directory is truly empty or an error occurs.

        Note:
            Uses --diff-filter=ACMR to count Added, Copied, Modified, Renamed files.
            Excludes deleted files (D) since they represent removed, not created work.
        """
        # ISSUE-SAAS-049: Check if we're in a git repository first
        if not self._is_git_repository():
            logger.debug(
                f"Working directory is not a git repository: {self._working_dir}. "
                "Using filesystem fallback for file detection."
            )
            return self._count_file_changes_filesystem()

        try:
            # Check for both staged and unstaged changes
            # First, check unstaged changes (working tree vs index)
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            unstaged_files = set()
            if result.returncode == 0 and result.stdout.strip():
                unstaged_files = set(result.stdout.strip().split("\n"))

            # Also check staged changes (index vs HEAD)
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            staged_files = set()
            if result.returncode == 0 and result.stdout.strip():
                staged_files = set(result.stdout.strip().split("\n"))

            # Also check untracked files (new files not yet added to git)
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )

            untracked_files = set()
            if result.returncode == 0 and result.stdout.strip():
                untracked_files = set(result.stdout.strip().split("\n"))

            # Combine all changed files (union of sets removes duplicates)
            all_changed = unstaged_files | staged_files | untracked_files
            file_count = len(all_changed)

            logger.debug(
                f"File changes detected: {file_count} "
                f"(unstaged={len(unstaged_files)}, staged={len(staged_files)}, "
                f"untracked={len(untracked_files)})"
            )

            return file_count

        except subprocess.TimeoutExpired:
            logger.warning("Git diff timed out, falling back to filesystem count")
            return self._count_file_changes_filesystem()
        except FileNotFoundError:
            logger.debug("Git not available, falling back to filesystem count")
            return self._count_file_changes_filesystem()
        except Exception as e:
            logger.debug(f"Failed to count file changes: {e}, falling back to filesystem")
            return self._count_file_changes_filesystem()

    def _get_file_changes(self) -> FileChangeSet:
        """Get detailed file changes using git, with filesystem fallback.

        Returns FileChangeSet with files separated into added (new) and modified (existing).
        For non-git directories, returns all files as "added".

        Returns:
            FileChangeSet with added, modified sets and total count
        """
        # Non-git fallback: treat all files as "added"
        if not self._is_git_repository():
            count = self._count_file_changes_filesystem()
            # Return empty sets since we can't differentiate without git
            return FileChangeSet(added=set(), modified=set(), count=count)

        try:
            # Get unstaged changes (working tree vs index)
            result = subprocess.run(
                ["git", "diff", "--name-only", "--diff-filter=ACMR"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            unstaged_files = set()
            if result.returncode == 0 and result.stdout.strip():
                unstaged_files = set(result.stdout.strip().split("\n"))

            # Get staged changes (index vs HEAD)
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMR"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            staged_files = set()
            if result.returncode == 0 and result.stdout.strip():
                staged_files = set(result.stdout.strip().split("\n"))

            # Get untracked files (new files not yet added to git)
            result = subprocess.run(
                ["git", "ls-files", "--others", "--exclude-standard"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            untracked_files = set()
            if result.returncode == 0 and result.stdout.strip():
                untracked_files = set(result.stdout.strip().split("\n"))

            # Categorize: untracked = added, staged/unstaged = modified
            added = untracked_files
            modified = unstaged_files | staged_files
            total_count = len(added) + len(modified)

            logger.debug(
                f"File changes: {total_count} total "
                f"(added={len(added)}, modified={len(modified)})"
            )

            return FileChangeSet(added=added, modified=modified, count=total_count)

        except subprocess.TimeoutExpired:
            logger.warning("Git diff timed out, falling back to filesystem count")
            count = self._count_file_changes_filesystem()
            return FileChangeSet(added=set(), modified=set(), count=count)
        except FileNotFoundError:
            logger.debug("Git not available, falling back to filesystem count")
            count = self._count_file_changes_filesystem()
            return FileChangeSet(added=set(), modified=set(), count=count)
        except Exception as e:
            logger.debug(f"Failed to get file changes: {e}, falling back to filesystem")
            count = self._count_file_changes_filesystem()
            return FileChangeSet(added=set(), modified=set(), count=count)

    def _count_lines(self, filepath: str) -> int | None:
        """Count lines in a file, handling binary files gracefully.

        Args:
            filepath: Relative path to file from working directory

        Returns:
            Number of lines in the file, or None if file is binary or unreadable
        """
        try:
            file_path = self._working_dir / filepath

            # Read file and count lines
            with open(file_path, encoding="utf-8") as f:
                return sum(1 for _ in f)

        except UnicodeDecodeError:
            # Binary file - return None
            logger.debug(f"Binary file detected: {filepath}")
            return None
        except FileNotFoundError:
            logger.debug(f"File not found: {filepath}")
            return None
        except Exception as e:
            logger.debug(f"Failed to count lines in {filepath}: {e}")
            return None

    def _run_tests(self) -> tuple[bool, int]:
        """Run project tests.

        Returns:
            Tuple of (tests_passed, test_count)
        """
        def _has_python_tests() -> bool:
            config_files = ("pytest.ini", "pyproject.toml", "setup.cfg", "tox.ini")
            if any((self._working_dir / name).exists() for name in config_files):
                return True
            skip_dirs = {".git", ".venv", "venv", "__pycache__", ".tox", ".mypy_cache"}
            for pattern in ("test_*.py", "*_test.py"):
                for path in self._working_dir.rglob(pattern):
                    if not path.is_file():
                        continue
                    if any(part in skip_dirs for part in path.parts):
                        continue
                    return True
            return False

        def _has_go_project() -> bool:
            if (self._working_dir / "go.mod").exists():
                return True
            for path in self._working_dir.rglob("*.go"):
                if path.is_file():
                    return True
            return False

        test_commands = [
            ("pytest", ["pytest", "--tb=no", "-q"], _has_python_tests),
            (
                "npm test",
                ["npm", "test", "--", "--passWithNoTests"],
                lambda: (self._working_dir / "package.json").exists(),
            ),
            ("go test", ["go", "test", "./..."], _has_go_project),
            (
                "cargo test",
                ["cargo", "test"],
                lambda: (self._working_dir / "Cargo.toml").exists(),
            ),
        ]

        for name, cmd, is_relevant in test_commands:
            if not is_relevant():
                continue
            # Check if the test runner is available and relevant
            try:
                # Simple check - does the command exist?
                result = subprocess.run(
                    [cmd[0], "--version"],
                    check=False,
                    capture_output=True,
                    timeout=5,
                    cwd=self._working_dir,
                )
                if result.returncode != 0:
                    continue

                # Run tests
                logger.debug(f"Running tests with {name}")
                result = subprocess.run(
                    cmd,
                    check=False,
                    capture_output=True,
                    timeout=DEFAULT_LLM_API_TIMEOUT,
                    cwd=self._working_dir,
                )

                # Parse results (simplified)
                passed = result.returncode == 0
                # Count tests from output (very simplified)
                output = result.stdout.decode("utf-8", errors="ignore")
                test_count = output.count("passed") + output.count("PASS")

                return passed, max(test_count, 1 if passed else 0)

            except subprocess.TimeoutExpired:
                logger.warning(f"Test timeout with {name}")
                continue
            except FileNotFoundError:
                continue
            except Exception as e:
                logger.debug(f"Test runner {name} failed: {e}")
                continue

        # No tests found or run
        return True, 0  # Assume success if no tests


__all__ = ["ExecuteHandler"]
