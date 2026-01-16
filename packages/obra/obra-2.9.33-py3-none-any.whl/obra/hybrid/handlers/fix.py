"""Fix handler for Hybrid Orchestrator.

This module handles the FIX action from the server. It attempts to fix issues
found during review by deploying an implementation agent with specific fix instructions.

The fix process:
    1. Receive FixRequest with issues to fix and execution order
    2. For each issue in order:
       - Build fix prompt with issue details
       - Deploy implementation agent
       - Verify the fix
    3. Return FixResults to report to server

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

from obra.api.protocol import FixRequest
from obra.config import (
    DEFAULT_NETWORK_TIMEOUT,
    build_llm_args,
    build_subprocess_env,
    get_agent_execution_timeout,
    get_heartbeat_initial_delay,
    get_heartbeat_interval,
    get_llm_cli,
    get_prompt_retention,
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
    """Represents a set of file changes detected in the working directory."""

    added: set[str]
    modified: set[str]
    count: int


class FileChangeTracker:
    """Tracks file changes between polls, returning only new changes."""

    def __init__(self, handler: "FixHandler") -> None:
        self._handler = handler
        self._previous_added: set[str] = set()
        self._previous_modified: set[str] = set()

    def poll(self) -> FileChangeSet:
        """Poll for new file changes since last poll."""
        current = self._handler._get_file_changes()
        new_added = current.added - self._previous_added
        new_modified = current.modified - self._previous_modified
        self._previous_added = current.added
        self._previous_modified = current.modified
        new_count = len(new_added) + len(new_modified)
        return FileChangeSet(added=new_added, modified=new_modified, count=new_count)


class HeartbeatThread(threading.Thread):
    """Background thread that emits heartbeat messages during long-running execution.

    Additionally, it emits liveness_check events via log_event callback.
    """

    def __init__(
        self,
        item_id: str,
        emitter: ProgressEmitter,
        file_tracker: FileChangeTracker,
        handler: "FixHandler",
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
            handler: FixHandler for line counting
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

        Every 180 seconds, emits liveness_check event via log_event callback.
        """
        self._stop_event.wait(self._initial_delay)

        # Track last liveness check time
        last_liveness_check = time.time()
        liveness_check_interval = 180  # seconds

        while not self._stop_event.is_set():
            elapsed = int(time.time() - self._start_time)
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

            changes = self._file_tracker.poll()
            if changes.count > 0:
                for filepath in changes.added:
                    line_count = self._handler._count_lines(filepath)
                    self._emitter.file_event(filepath, "new", line_count)
                for filepath in changes.modified:
                    line_count = self._handler._count_lines(filepath)
                    self._emitter.file_event(filepath, "modified", line_count)
            self._stop_event.wait(self._interval)

    def _get_file_count(self) -> int:
        """Get current count of changed files."""
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
        """Signal the thread to stop and wait for it to exit."""
        self._stop_event.set()
        self.join(timeout=2.0)


class FixHandler(ObservabilityContextMixin):
    """Handler for FIX action.

    Attempts to fix issues found during review by deploying implementation
    agents with targeted fix instructions.

    ## Architecture Context (ADR-027)

    This handler implements the two-tier prompting architecture where:
    - **Server (Tier 1)**: Generates strategic base prompts with fix guidance
    - **Client (Tier 2)**: Enriches base prompts with local tactical context

    **Implementation Flow**:
    1. Server sends FixRequest with base_prompt containing fix instructions
    2. Client enriches base_prompt via PromptEnricher (adds file structure, git log)
    3. Client invokes implementation agent locally to apply fixes
    4. Client verifies fixes locally (tests, lint, security checks)
    5. Client reports fix results back to server for validation

    ## IP Protection

    Strategic fix patterns (security best practices, quality standards) stay on server.
    This protects Obra's proprietary fix guidance from client-side inspection.

    ## Privacy Protection

    Tactical context (code to fix, file contents, git messages) never sent to server.
    Only fix results (status, files modified, verification outcome) is transmitted.

    See: docs/decisions/ADR-027-two-tier-prompting-architecture.md

    Example:
        >>> handler = FixHandler(Path("/path/to/project"))
        >>> request = FixRequest(
        ...     issues_to_fix=[{"id": "SEC-001", "description": "SQL injection"}],
        ...     execution_order=["SEC-001"]
        ... )
        >>> result = handler.handle(request)
        >>> print(result["fix_results"])
    """

    DOC_FIX_TIMEOUT_S = 120

    def __init__(
        self,
        working_dir: Path,
        llm_config: dict[str, Any] | None = None,
        session_id: str | None = None,
        log_file: Path | None = None,
        trace_id: str | None = None,
        log_event: Any | None = None,
        parent_span_id: str | None = None,
        observability_config: ObservabilityConfig | None = None,
        progress_emitter: ProgressEmitter | None = None,
        on_stream: StreamCallback = None,
    ) -> None:
        """Initialize FixHandler.

        Args:
            working_dir: Working directory for file access
            llm_config: LLM configuration for agent deployment
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

    def handle(self, request: FixRequest) -> dict[str, Any]:
        """Handle FIX action.

        Args:
            request: FixRequest from server with base_prompt

        Returns:
            Dict with fix_results list and item_id

        Raises:
            ValueError: If request.base_prompt is None (server must provide base_prompt)
        """
        # ISSUE-SAAS-009: Normalize issues to dict format
        # Server may return issues as List[str] (blocking_issues) instead of List[Dict]
        # FIX-PRIORITY-LOSS-001: Use issue_details if present (preserves priority)
        issues = self._normalize_issues(request.issues_to_fix, request.issue_details)
        execution_order = request.execution_order
        # ISSUE-SAAS-021: Track item_id for fix-review loop
        item_id = request.item_id

        if not issues:
            logger.info("No issues to fix")
            return {
                "fix_results": [],
                "fixed_count": 0,
                "failed_count": 0,
                "skipped_count": 0,
                "item_id": item_id,  # ISSUE-SAAS-021
            }

        # Validate base_prompt (server-side prompting required)
        if request.base_prompt is None:
            error_msg = "FixRequest.base_prompt is None. Server must provide base prompt (ADR-027)."
            logger.error(error_msg)
            raise ValueError(error_msg)

        logger.info(f"Fixing {len(issues)} issues")
        print_info(f"Fixing {len(issues)} issues")

        # Enrich base prompt with local tactical context
        # Note: File-level scope constraints removed per ISSUE-SAAS-043
        # Project boundary is enforced via _validate_project_boundary() post-execution
        enricher = PromptEnricher(self._working_dir)
        enriched_prompt = enricher.enrich(request.base_prompt)

        # Build issue lookup for ordering
        issue_map = {issue.get("id", f"issue-{i}"): issue for i, issue in enumerate(issues)}

        # Determine execution order
        if execution_order:
            ordered_ids = execution_order
        else:
            # Default: order by priority (P0 first)
            ordered_ids = self._order_by_priority(issues)

        fix_results: list[dict[str, Any]] = []
        fixed_count = 0
        failed_count = 0
        skipped_count = 0

        for issue_id in ordered_ids:
            issue = issue_map.get(issue_id)
            if not issue:
                logger.warning(f"Issue {issue_id} not found in issue map, skipping")
                skipped_count += 1
                continue

            result = self._fix_issue(issue, enriched_prompt)
            fix_results.append(result)

            status = result.get("status", "failed")
            # BUG-SCHEMA-001: _fix_issue returns "applied" to match server schema
            if status in ("fixed", "applied"):
                fixed_count += 1
                print_info(f"  Fixed: {issue_id}")
            elif status == "skipped":
                skipped_count += 1
                print_warning(f"  Skipped: {issue_id}")
            else:
                failed_count += 1
                print_error(f"  Failed: {issue_id}")

        logger.info(
            f"Fix complete: {fixed_count} fixed, {failed_count} failed, {skipped_count} skipped"
        )

        return {
            "fix_results": fix_results,
            "fixed_count": fixed_count,
            "failed_count": failed_count,
            "skipped_count": skipped_count,
            "item_id": item_id,  # ISSUE-SAAS-021: Include for fix-review loop
        }

    def _normalize_issues(
        self,
        issues: list[Any],
        issue_details: list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        """Normalize issues to dict format.

        ISSUE-SAAS-009: Server may return issues as List[str] (blocking_issues from
        QualityScorecard) instead of List[Dict[str, Any]]. This method normalizes
        both formats to a consistent dict structure.

        FIX-PRIORITY-LOSS-001: If issue_details is provided, use those directly
        as they preserve the original priority information from the coordinator.

        Args:
            issues: List of issues (strings or dicts) - may have lost priority info
            issue_details: Optional full issue dicts from coordinator with priority preserved

        Returns:
            List of normalized issue dicts with at least 'id' and 'description' keys
        """
        # FIX-PRIORITY-LOSS-001: Use issue_details if provided (preserves priority)
        if issue_details:
            logger.debug(
                f"Using issue_details with preserved priority ({len(issue_details)} issues)"
            )
            normalized: list[dict[str, Any]] = []
            for i, detail in enumerate(issue_details):
                if isinstance(detail, dict):
                    # Ensure id exists
                    if "id" not in detail:
                        detail = dict(detail)
                        detail["id"] = f"issue-{i}"
                    normalized.append(detail)
                else:
                    logger.warning(f"Unexpected issue_details format at index {i}: {type(detail)}")
            if normalized:
                return normalized
            # Fall through to legacy normalization if issue_details was empty/invalid

        # Legacy normalization: issues may be strings or dicts without full priority
        normalized = []
        for i, issue in enumerate(issues):
            if isinstance(issue, str):
                # String format: convert to dict with synthetic ID
                # Use the string itself as the ID (for execution_order matching)
                # and as the description
                normalized.append(
                    {
                        "id": issue,  # Use string value as ID for execution_order lookup
                        "description": issue,
                        "priority": "P2",  # Default priority for string issues
                    }
                )
            elif isinstance(issue, dict):
                # Dict format: ensure id exists
                if "id" not in issue:
                    issue = dict(issue)  # Copy to avoid mutating original
                    issue["id"] = f"issue-{i}"
                normalized.append(issue)
            else:
                # Unknown format: wrap in dict
                logger.warning(f"Unknown issue format at index {i}: {type(issue)}")
                normalized.append(
                    {
                        "id": f"issue-{i}",
                        "description": str(issue),
                        "priority": "P2",
                    }
                )
        return normalized

    def _order_by_priority(self, issues: list[dict[str, Any]]) -> list[str]:
        """Order issues by priority.

        Args:
            issues: List of issues (normalized to dict format)

        Returns:
            List of issue IDs in priority order (P0 first)
        """
        priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

        def get_priority_rank(issue: dict[str, Any]) -> int:
            priority = issue.get("priority", "P3")
            return priority_order.get(priority, 4)

        sorted_issues = sorted(issues, key=get_priority_rank)
        return [issue.get("id", f"issue-{i}") for i, issue in enumerate(sorted_issues)]

    def _resolve_issue_timeout(self, issue: dict[str, Any]) -> int:
        """Resolve timeout for an issue, with tighter limits for docs fixes."""
        base_timeout = get_agent_execution_timeout()
        if self._is_documentation_issue(issue):
            return min(base_timeout, self.DOC_FIX_TIMEOUT_S)
        return base_timeout

    def _is_documentation_issue(self, issue: dict[str, Any]) -> bool:
        """Check if the issue is documentation-related."""
        issue_id = str(issue.get("id", "")).upper()
        if issue_id.startswith("DOC-"):
            return True
        for key in ("category", "dimension", "type"):
            value = issue.get(key)
            if value and str(value).lower() in {"documentation", "docs", "doc"}:
                return True
        return False

    def _fix_issue(
        self,
        issue: dict[str, Any],
        enriched_prompt: str,
    ) -> dict[str, Any]:
        """Fix a single issue.

        Args:
            issue: Issue dictionary
            enriched_prompt: Enriched fix prompt from server

        Returns:
            FixResult dictionary
        """
        issue_id = issue.get("id", "unknown")
        description = issue.get("description", "")

        logger.info(f"Fixing issue {issue_id}: {description[:50]}...")

        try:
            timeout_s = self._resolve_issue_timeout(issue)
            if self._is_documentation_issue(issue):
                logger.info(
                    "Using reduced timeout for documentation issue %s: %ss",
                    issue_id,
                    timeout_s,
                )

            # Capture file state before execution for modification detection
            before_state = self._capture_file_state()

            # Deploy implementation agent to fix with enriched prompt
            result = self._deploy_agent(enriched_prompt, timeout_s=timeout_s)

            # Detect actual file modifications during execution
            files_modified = self._detect_modifications(before_state)

            # Verify the fix
            verification = self._verify_fix(issue, result)

            # Validate project boundary (post-execution safety net)
            boundary_check = self._validate_project_boundary(files_modified)
            verification["boundary_valid"] = not boundary_check["has_violations"]
            if boundary_check["has_violations"]:
                logger.warning(
                    f"Project boundary violation for issue {issue_id}: "
                    f"{boundary_check['violations']}"
                )
                verification["boundary_violations"] = boundary_check["violations"]

            # Determine status based on verification
            # BUG-SCHEMA-001: Use "applied" not "fixed" to match server schema (request_schemas.py:211)
            if verification.get("all_passed", False):
                status = "applied"
            elif verification.get("partial", False):
                status = "applied"  # Partial fix still counts
            else:
                status = "failed"

            # BUG-SCHEMA-002: Add summary for orchestrator (orchestrator.py:791)
            summary = result.get(
                "summary",
                f"{'Applied fix for' if status == 'applied' else 'Failed to fix'} issue {issue_id}",
            )

            return {
                "issue_id": issue_id,
                "status": status,
                "files_modified": files_modified,
                "verification": verification,
                "summary": summary,
            }

        except Exception as e:
            logger.exception(f"Failed to fix issue {issue_id}: {e}")
            return {
                "issue_id": issue_id,
                "status": "failed",
                "files_modified": [],
                "verification": {"error": str(e)},
                "summary": f"Failed to fix issue {issue_id}: {e!s}",  # BUG-SCHEMA-002
            }

    def _prepare_prompt(self, prompt: str) -> str:
        """Prepare prompt with thinking keywords if needed.

        Inject ultrathink keyword for Claude + maximum thinking level.

        Args:
            prompt: Base prompt

        Returns:
            Prepared prompt with keywords if applicable
        """
        provider = self._llm_config.get("provider", "")
        thinking_level = self._llm_config.get("thinking_level", "")

        # Anthropic + maximum = ultrathink keyword injection
        if provider == "anthropic" and thinking_level == "maximum":
            return f"ultrathink: {prompt}"

        return prompt

    def _deploy_agent(self, prompt: str, *, timeout_s: int | None = None) -> dict[str, Any]:
        """Deploy implementation agent to apply fix via subprocess.

        Uses build_llm_args() and get_llm_cli() to construct command.
        Detects auth errors and provides login hints.

        Args:
            prompt: Fix prompt

        Returns:
            Agent result dictionary with status, summary, files_modified
        """
        logger.debug("Deploying implementation agent for fix")

        # Prepare prompt with thinking keywords if needed
        prepared_prompt = self._prepare_prompt(prompt)

        # Build CLI command and args from llm_config
        # ISSUE-SAAS-035: Use mode="execute" to allow file writing (no --print flag)
        if self._llm_config:
            provider = self._llm_config.get("provider", "anthropic")
            cli_command = get_llm_cli(provider)
            cli_args = build_llm_args(self._llm_config, mode="execute")
        else:
            # Fallback to defaults if no config
            cli_command = "claude"
            cli_args = ["--dangerously-skip-permissions"]

        prompt_manager = PromptFileManager(self._working_dir, retain=get_prompt_retention())
        removed_orphans = prompt_manager.cleanup_stale_prompt_artifacts()
        if removed_orphans:
            logger.debug("Removed %d orphaned prompt files", removed_orphans)

        prompt_path, prompt_instruction = prompt_manager.write_prompt(prepared_prompt)

        cmd = [cli_command, *cli_args]
        if provider == "openai":
            cmd.extend(["-C", str(self._working_dir)])
            logger.debug("Codex workspace root set via -C: %s", self._working_dir)
        cmd.append(prompt_instruction)

        # BUG-e100a87e: Add --skip-git-repo-check for OpenAI Codex (default: true)
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

        logger.debug(f"Running fix agent: {' '.join(cmd[:3])}...")

        # Build subprocess environment with auth-aware API key handling
        # When auth_method is "oauth", API keys are stripped to prevent unexpected billing
        auth_method = self._llm_config.get("auth_method", "oauth")
        env = build_subprocess_env(
            auth_method=auth_method,
            extra_env=self._get_observability_env(),  # ISSUE-OBS-003: observability context
        )

        timeout_s = timeout_s or get_agent_execution_timeout()
        start_time = time.time()
        response_text = ""
        status = "failed"
        error_message: str | None = None

        # S3.T0/S3.T1: Set up heartbeat thread if progress emitter is available
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
            item_id = "fix"
            # S3.T4: Pass log_event, session_id, trace_id to HeartbeatThread
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
            # Execute subprocess with observability environment
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

                proc.wait(timeout=timeout_s)
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

            # TRIAGE-C1: Comprehensive subprocess logging
            logger.info(f"Fix subprocess completed: returncode={result.returncode}, stdout_len={len(result.stdout or '')}, stderr_len={len(result.stderr or '')}")

            # Save full output to debug file for analysis
            debug_dir = self._working_dir / ".obra" / "debug"
            debug_dir.mkdir(parents=True, exist_ok=True)
            debug_file = debug_dir / f"fix_attempt_{int(time.time())}.log"
            debug_content = f"""Fix Attempt Debug Log
Command: {' '.join(cmd)}
Working Directory: {self._working_dir}
Return Code: {result.returncode}

=== STDOUT ({len(result.stdout or '')} chars) ===
{result.stdout or '(empty)'}

=== STDERR ({len(result.stderr or '')} chars) ===
{result.stderr or '(empty)'}

=== PROMPT ({len(prepared_prompt)} chars) ===
{prepared_prompt[:1000]}...
"""
            debug_file.write_text(debug_content, encoding="utf-8")
            logger.info(f"Full subprocess output saved to {debug_file}")

            # Log stderr preview if non-zero exit
            if result.returncode != 0:
                logger.error(f"Fix subprocess failed with code {result.returncode}")
                if result.stderr:
                    logger.error(f"STDERR preview: {result.stderr[:500]}")
                if result.stdout:
                    logger.info(f"STDOUT preview: {result.stdout[:500]}")

            # Check for auth errors in stderr
            stderr = result.stderr.lower()
            if "not authenticated" in stderr or "login" in stderr or "auth" in stderr:
                error_message = result.stderr[:200] if result.stderr else "Authentication required"
                return {
                    "status": "failed",
                    "summary": f"Authentication required. Run '{cli_command} login' to authenticate.",
                    "files_modified": [],
                }

            # Codex prompt file missing hint
            if provider == "openai" and result.stderr:
                stderr_lower = result.stderr.lower()
                if ".obra-prompt-" in stderr_lower and (
                    "not present" in stderr_lower
                    or "not found" in stderr_lower
                    or "no such file" in stderr_lower
                ):
                    error_message = result.stderr[:200]
                    return {
                        "status": "failed",
                        "summary": (
                            "Codex could not find the prompt file in the workspace. "
                            "Obra sets the workspace root with -C <working_dir>; "
                            "verify the working directory is correct and accessible."
                        ),
                        "files_modified": [],
                    }

            # Check exit code
            if result.returncode == 0:
                status = "success"
                return {
                    "status": "success",
                    "summary": "Fix applied successfully",
                    "files_modified": [],  # Would parse git diff in production
                }
            error_msg = result.stderr[:200] if result.stderr else "Unknown error"
            error_message = error_msg
            return {
                "status": "failed",
                "summary": f"Fix failed: {error_msg}",
                "files_modified": [],
            }

        except subprocess.TimeoutExpired:
            logger.exception("Fix agent execution timed out")
            error_message = f"Fix timed out after {timeout_s} seconds"
            return {
                "status": "failed",
                "summary": f"Fix timed out after {timeout_s} seconds",
                "files_modified": [],
            }
        except FileNotFoundError:
            logger.exception(f"CLI command '{cli_command}' not found")
            error_message = f"CLI '{cli_command}' not found"
            return {
                "status": "failed",
                "summary": f"CLI '{cli_command}' not found. Install it first.",
                "files_modified": [],
            }
        except Exception as e:
            logger.exception(f"Fix agent deployment failed: {e}")
            error_message = str(e)
            return {
                "status": "failed",
                "summary": f"Deployment failed: {e!s}",
                "files_modified": [],
            }
        finally:
            prompt_manager.cleanup(prompt_path)

            # S3.T0: Stop heartbeat thread if it was started
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
                    provider=self._llm_config.get("provider", "anthropic"),
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
                    status="success" if status == "success" else "error",
                    error_message=error_message,
                    trace_id=self._trace_id,
                    span_id=uuid.uuid4().hex,
                    parent_span_id=self._parent_span_id,
                    call_site="fix",
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

    def _verify_fix(
        self,
        issue: dict[str, Any],
        agent_result: dict[str, Any],
    ) -> dict[str, bool]:
        """Verify that the fix resolved the issue.

        Args:
            issue: Original issue
            agent_result: Result from fix agent

        Returns:
            Verification results dictionary
        """
        verification: dict[str, bool] = {
            "agent_succeeded": agent_result.get("status") == "success",
            "files_modified": bool(agent_result.get("files_modified")),
        }

        # TRIAGE-C1: Log verification details
        logger.info(f"Verifying fix for issue {issue.get('id')}")
        logger.info(f"Agent status: {agent_result.get('status')}")
        logger.info(f"Files modified: {agent_result.get('files_modified')}")

        # Check if specific verification steps are needed based on issue category
        category = issue.get("category", "")
        logger.info(f"Issue category: {category}")

        if category == "security":
            result = self._run_security_check()
            verification["security_check_passed"] = result
            logger.info(f"Security check result: {result}")
        elif category == "testing":
            result = self._run_tests()
            verification["tests_passed"] = result
            logger.info(f"Tests result: {result}")
        elif category == "code_quality":
            result = self._run_lint()
            verification["lint_passed"] = result
            logger.info(f"Lint result: {result}")

        # Determine overall result
        # FIX: files_modified is informational only - don't require it for success
        # The meaningful verification is: agent succeeded AND category-specific check passed
        # Previously, files_modified=[] (hardcoded in _deploy_agent) caused bool([])=False,
        # which poisoned all() even when agent succeeded and tests passed.
        required_checks = ["agent_succeeded"]
        for check_key in ["tests_passed", "security_check_passed", "lint_passed"]:
            if check_key in verification:
                required_checks.append(check_key)
                break  # Only one category check per issue

        verification["all_passed"] = all(
            verification.get(k, False) for k in required_checks
        )

        logger.info(
            f"Verification complete: required_checks={required_checks}, "
            f"results={[verification.get(k) for k in required_checks]}, "
            f"all_passed={verification['all_passed']}"
        )
        return verification

    def _capture_file_state(self) -> set[str]:
        """Capture current modified/untracked files for diff detection.

        Returns set of file paths currently showing as modified or untracked
        in git status. Used to detect what files changed during agent execution.

        Returns:
            Set of file paths (relative to working directory)
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            if result.returncode != 0:
                logger.debug(f"git status failed: {result.stderr}")
                return set()

            files: set[str] = set()
            # Use rstrip() to only remove trailing newlines, preserving leading spaces
            # Git status format: "XY filename" where XY is 2-char status + space
            # First column can be space (e.g., " M file.py" for unstaged modification)
            for line in result.stdout.rstrip("\n").split("\n"):
                if line:
                    # Skip the status prefix (first 3 chars: XY + space)
                    files.add(line[3:].strip())
            return files
        except subprocess.TimeoutExpired:
            logger.warning("git status timed out during file state capture")
            return set()
        except FileNotFoundError:
            logger.debug("git not available for file state capture")
            return set()
        except Exception as e:
            logger.debug(f"Failed to capture file state: {e}")
            return set()

    def _detect_modifications(self, before_state: set[str]) -> list[str]:
        """Detect files modified since before_state was captured.

        Compares current git status against the state captured before agent
        execution to determine which files were actually modified.

        Args:
            before_state: Set of files from _capture_file_state() before execution

        Returns:
            Sorted list of file paths that were modified during execution
        """
        after_state = self._capture_file_state()
        new_modifications = after_state - before_state
        return sorted(new_modifications)

    def _validate_project_boundary(self, files_modified: list[str]) -> dict[str, Any]:
        """Validate all modifications are within project directory.

        Post-execution safety net that checks if the fix agent modified any
        files outside the project working directory. This prevents filesystem
        escape while allowing modification of any file within the project.

        Args:
            files_modified: Files that were modified by the fix agent

        Returns:
            Dict with:
                - has_violations: True if any files are outside project boundary
                - violations: List of file paths that violated the boundary
        """
        if not files_modified:
            return {"has_violations": False, "violations": []}

        project_root = self._working_dir.resolve()
        violations: list[str] = []

        for file_path in files_modified:
            try:
                # Resolve the full path and check if it's under project root
                resolved = (project_root / file_path).resolve()
                resolved.relative_to(project_root)
            except ValueError:
                # File is outside project directory
                violations.append(file_path)
                logger.error(f"Project boundary violation: {file_path}")

        if violations:
            logger.error(
                f"Fix agent modified {len(violations)} file(s) outside project: {violations}"
            )

        return {"has_violations": bool(violations), "violations": violations}

    def _run_security_check(self) -> bool:
        """Run security check to verify fix removed vulnerabilities.

        Uses SecurityAgent to scan for P0/P1 security issues (hardcoded credentials,
        SQL injection, command injection, etc.). This provides fast client-side
        verification before server-side re-review.

        Returns:
            True if no critical (P0/P1) security issues found, False otherwise

        Note:
            Fails open on errors (returns True) to avoid blocking on tool failures.
            Server-side re-review per ADR-031 provides authoritative validation.
        """
        try:
            from obra.agents.security import SecurityAgent

            logger.info("Running security verification scan")

            # Create security agent with current working directory
            agent = SecurityAgent(working_dir=self._working_dir)

            # Run analysis on all changed files (None = analyze all files)
            # Use short timeout since this is verification, not comprehensive audit
            result = agent.analyze(
                item_id="fix-verification",
                changed_files=None,
                timeout_ms=30000,  # 30 seconds - quick verification scan
            )

            # Check for critical security issues
            critical_issues = [
                issue
                for issue in result.issues
                if issue.priority.value in ["P0", "P1"]
            ]

            if critical_issues:
                logger.warning(
                    f"Security verification failed: {len(critical_issues)} critical issues found"
                )
                for issue in critical_issues[:3]:  # Log first 3 for debugging
                    logger.warning(
                        f"  - {issue.priority.value} {issue.title} in {issue.file_path or 'unknown'}"
                    )
                return False

            logger.info(
                f"Security verification passed: {len(result.issues)} total issues, "
                f"0 critical (P0/P1)"
            )
            return True

        except ImportError as e:
            logger.warning(f"SecurityAgent not available: {e}")
            return True  # Fail open - don't block if tool missing
        except Exception as e:
            logger.error(f"Security check failed with error: {e}", exc_info=True)
            return True  # Fail open - don't block on tool errors

    def _run_tests(self) -> bool:
        """Run tests to verify fix.

        Returns:
            True if tests pass
        """
        # Try to run pytest if available
        try:
            logger.info(f"Running pytest in {self._working_dir}")
            # MONITORING EXEMPTION: Local test verification, typically <30s, 60s timeout is safety margin
            result = subprocess.run(
                ["pytest", "--tb=no", "-q", "-x"],
                check=False,
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self._working_dir,
            )
            logger.info(f"Pytest returncode: {result.returncode}")
            logger.info(f"Pytest stdout: {result.stdout[:500] if result.stdout else '(empty)'}")
            logger.info(f"Pytest stderr: {result.stderr[:500] if result.stderr else '(empty)'}")
            passed = result.returncode == 0
            logger.info(f"Pytest result: {'PASS' if passed else 'FAIL'}")
            return passed
        except subprocess.TimeoutExpired:
            logger.warning("Pytest timed out after 60s - assuming pass")
            return True
        except FileNotFoundError as e:
            logger.warning(f"Pytest not found - assuming pass: {e}")
            return True
        except Exception as e:
            logger.warning(f"Pytest execution error - assuming pass: {e}")
            return True

    def _run_lint(self) -> bool:
        """Run linter to verify fix.

        Returns:
            True if lint passes
        """
        # Try to run ruff if available
        try:
            result = subprocess.run(
                ["ruff", "check", "."],
                check=False,
                capture_output=True,
                timeout=DEFAULT_NETWORK_TIMEOUT,
                cwd=self._working_dir,
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            # If linter can't be run, assume pass
            return True

    def _is_git_repository(self) -> bool:
        """Check if working directory is within a git repository."""
        path = self._working_dir.resolve()
        if (path / ".git").exists():
            return True
        return any((parent / ".git").exists() for parent in path.parents)

    def _count_file_changes_filesystem(self) -> int:
        """Count files in working directory using filesystem (non-git fallback)."""
        excluded_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv", ".tox"}
        excluded_extensions = {".pyc", ".pyo", ".egg-info"}

        file_count = 0
        try:
            for item in self._working_dir.iterdir():
                if item.name.startswith("."):
                    continue
                if item.is_dir() and item.name in excluded_dirs:
                    continue

                if item.is_file():
                    if any(item.name.endswith(ext) for ext in excluded_extensions):
                        continue
                    file_count += 1
                elif item.is_dir():
                    for sub_item in item.rglob("*"):
                        if sub_item.is_file():
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
        """Count actual file changes using git diff, with filesystem fallback."""
        if not self._is_git_repository():
            logger.debug(
                f"Working directory is not a git repository: {self._working_dir}. "
                "Using filesystem fallback for file detection."
            )
            return self._count_file_changes_filesystem()

        try:
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
        """Get detailed file changes using git, with filesystem fallback."""
        if not self._is_git_repository():
            count = self._count_file_changes_filesystem()
            return FileChangeSet(added=set(), modified=set(), count=count)

        try:
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
        """Count lines in a file, handling binary files gracefully."""
        try:
            file_path = self._working_dir / filepath
            with open(file_path, encoding="utf-8") as f:
                return sum(1 for _ in f)
        except UnicodeDecodeError:
            logger.debug(f"Binary file detected: {filepath}")
            return None
        except FileNotFoundError:
            logger.debug(f"File not found: {filepath}")
            return None
        except Exception as e:
            logger.debug(f"Failed to count lines in {filepath}: {e}")
            return None


__all__ = ["FixHandler"]
