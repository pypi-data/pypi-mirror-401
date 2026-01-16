"""Hybrid Orchestrator for EPIC-HYBRID-001.

This module provides the client-side orchestration logic for the Unified Hybrid Architecture.
It connects to the server, dispatches actions to appropriate handlers, and manages the
orchestration loop.

Design Principle (from PRD):
    - Server owns the brain (decisions, orchestration logic)
    - Client owns the hands (execution, code access)

The HybridOrchestrator:
    1. Starts a session with the server
    2. Receives action instructions from the server
    3. Dispatches to appropriate handlers (derive, examine, revise, execute, review, fix)
    4. Reports results back to the server
    5. Repeats until completion or escalation

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 3
    - obra/api/protocol.py
    - obra/hybrid/handlers/*.py
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import time
import uuid
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from pydantic import BaseModel

from obra.api import APIClient
from obra.api.protocol import (
    ActionType,
    CompletionNotice,
    DerivedPlan,
    DeriveRequest,
    EscalationNotice,
    EscalationReason,
    ExaminationReport,
    ExamineRequest,
    ExecutionRequest,
    ExecutionResult,
    ExecutionStatus,
    FixRequest,
    ResumeContext,
    ReviewRequest,
    RevisedPlan,
    RevisionRequest,
    ServerAction,
    SessionPhase,
    SessionStart,
    UserDecision,
    UserDecisionChoice,
)
from obra.config import get_max_iterations
from obra.display import console, print_info, print_warning
from obra.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    ConnectionError,
    OrchestratorError,
)

# ISSUE-SAAS-042: Use HybridEventLogger for observability
# This is the SaaS-spec logger - always available in published package
from obra.hybrid.event_logger import HybridEventLogger
from obra.model_registry import resolve_quality_tier
from obra.review.config import ReviewConfig

logger = logging.getLogger(__name__)

# ISSUE-CLI-012: Maximum polling retry attempts before circuit breaker triggers
# Set to 5 per industry best practices (AWS, Google Cloud, Stripe all use 3-5)
# Observed behavior showed 7 attempts before manual termination
MAX_POLLING_RETRIES = 5


class HybridOrchestrator:
    """Client-side orchestrator for Obra hybrid architecture.

    ## Architecture

    This orchestrator implements the **client-side** of the Obra SaaS hybrid
    architecture (ADR-027):

    - **Server**: Provides orchestration decisions, action instructions, and validation
    - **Client**: Builds prompts locally, executes LLM/agents, reports results

    ## Handler Responsibilities

    Each handler (`DeriveHandler`, `ExamineHandler`, etc.) implements client-side logic:
    1. Receives action request from server (objective, plan items, issues, etc.)
    2. Builds prompts entirely client-side
    3. Gathers tactical context locally (files, git, errors)
    4. Invokes LLM or agent locally
    5. Reports results back to server for validation

    Note: The marker-based prompt enrichment described in ADR-027 is an aspirational
    design. The current implementation builds prompts entirely client-side.

    ## Privacy Model

    Tactical context (file contents, git messages, errors) stays client-side.
    Server never receives file contents or local project details.

    See: docs/decisions/ADR-027-two-tier-prompting-architecture.md
    """

    def __init__(
        self,
        client: APIClient,
        working_dir: Path | None = None,
        on_progress: Callable[[str, dict[str, Any]], None] | None = None,
        on_escalation: Callable[[EscalationNotice], UserDecisionChoice] | None = None,
        on_stream: Callable[[str, str], None] | None = None,
        review_config: ReviewConfig | None = None,
        defaults_json: bool = False,
        observability_config: "ObservabilityConfig | None" = None,
        progress_emitter: "ProgressEmitter | None" = None,
    ) -> None:
        """Initialize HybridOrchestrator.

        Args:
            client: APIClient for server communication
            working_dir: Working directory for file operations
            on_progress: Optional callback for progress updates (action, payload)
            on_escalation: Optional callback for handling escalations
            on_stream: Optional callback for LLM streaming chunks (event_type, content)
            review_config: Review configuration (selection/modifiers/output)
            defaults_json: Whether to output JSON defaults
            observability_config: Optional observability configuration for progress visibility
            progress_emitter: Optional progress emitter for heartbeat and file events
        """
        self._client = client
        # GIT-HARD-001 S2.T3: Track if working_dir was explicitly provided (for Inbox exemption)
        self._working_dir_explicit = working_dir is not None
        self._working_dir = working_dir or Path.cwd()
        self._session_id: str | None = None
        self._trace_id: str | None = None
        self._pipeline_start_time: float | None = None
        self._pipeline_span_id: str | None = None
        self._phase_span_id: str | None = None
        self._subphase_span_id: str | None = None
        self._component = "hybrid_client"
        self._on_progress = on_progress
        self._on_escalation = on_escalation
        self._on_stream = on_stream
        self._bypass_modes: list[str] = []
        self._skip_completed_items: list[str] = []  # For --continue-from recovery
        self._defaults_json = defaults_json
        self._observability_config = observability_config
        self._progress_emitter = progress_emitter

        # Handler registry - lazily initialized
        self._handlers: dict[ActionType, Any] = {}

        # Local plan context loaded from client-side plan files (plan_id workflow)
        self._plan_context: dict[str, Any] | None = None

        # LLM config - set by from_config() or defaults to None
        self._llm_config: dict[str, Any] | None = None

        # Phase tracking for observability (S3.T3)
        self._current_phase: SessionPhase | None = None
        self._phase_start_time: float | None = None

        # Polling failure tracking for diagnostics
        self._polling_failure_count: int = 0
        self._last_item_id: str | None = None

        # ISSUE-SAAS-042: Initialize HybridEventLogger for observability
        # This is the SaaS-spec logger - always available in published package
        self._event_logger = HybridEventLogger()
        self._event_logger.set_component(self._component)

        # Review configuration for handler creation
        self._review_config = review_config or ReviewConfig()

        logger.debug(f"HybridOrchestrator initialized for {self._working_dir}")

    def create_monitoring_context(
        self,
        task_id: str | None = None,
        liveness_interval: int = 180,
    ) -> dict[str, Any] | None:
        """Create monitoring context dict for subprocess operations.

        ADR-043 Phase 3: Helper factory to simplify monitoring context construction.
        Returns dict compatible with MonitoringThread initialization.

        Args:
            task_id: Optional task ID for monitoring context (agent operations)
            liveness_interval: Liveness check interval in seconds (default: 180s)

        Returns:
            Monitoring context dict with keys: config, workspace_path, event_logger, session_id
            Returns None if session_id not available

        Usage:
            context = orchestrator.create_monitoring_context(task_id="T-001")
            handler = DeriveHandler(..., monitoring_context=context)
        """
        if not self._session_id:
            return None

        return {
            "config": {
                "orchestration": {
                    "monitoring": {"enabled": True},
                    "timeout": {"liveness_check_interval": liveness_interval},
                }
            },
            "workspace_path": str(self._working_dir),
            "event_logger": self._event_logger,
            "session_id": self._session_id,
            "task_id": task_id,
        }

    def _log_session_event(self, event_type: str, **kwargs) -> None:
        """Log hybrid session event for observability (ISSUE-SAAS-042).

        Uses HybridEventLogger - the SaaS-spec logger always available in published package.

        Args:
            event_type: Event type (session_started, derivation_started, etc.)
            **kwargs: Event-specific data
        """
        session_id = self._session_id or ""
        if self._trace_id and "trace_id" not in kwargs:
            kwargs["trace_id"] = self._trace_id
        if "component" not in kwargs:
            kwargs["component"] = self._component

        # ISSUE-015: Pop session_id from kwargs to avoid collision
        # Some handlers (like IntentHandler) pass session_id=None in kwargs,
        # which would cause TypeError: multiple values for keyword argument 'session_id'
        kwargs.pop("session_id", None)

        try:
            self._event_logger.log_event(event_type, session_id=session_id, **kwargs)
        except Exception as e:
            logger.warning(f"Failed to log hybrid event '{event_type}': {e}")

    def _log_pipeline_completed(self) -> None:
        """Log pipeline completion with total duration if available."""
        if self._pipeline_start_time is None:
            return
        duration_ms = int((time.time() - self._pipeline_start_time) * 1000)
        self._log_session_event(
            "pipeline_completed",
            duration_ms=duration_ms,
            span_id=self._pipeline_span_id,
        )
        self._log_resource_snapshot("pipeline_end")

        # Stop session console logging for feedback system
        try:
            from obra.feedback import stop_session_logging
            stop_session_logging()
            logger.debug("Session console logging stopped")
        except Exception as e:
            logger.warning(f"Failed to stop session console logging: {e}")

    def _log_resource_snapshot(self, snapshot_type: str) -> None:
        """Log a resource snapshot via event logger."""
        self._log_session_event("resource_snapshot", snapshot_type=snapshot_type)

    def _start_subphase(self, subphase: str) -> float:
        """Start a subphase span and return its start time."""
        self._subphase_span_id = uuid.uuid4().hex
        self._log_session_event(
            "subphase_started",
            subphase=subphase,
            span_id=self._subphase_span_id,
            parent_span_id=self._phase_span_id,
        )
        return time.time()

    def _complete_subphase(
        self,
        subphase: str,
        start_time: float,
        status: str = "success",
        error_message: str | None = None,
    ) -> None:
        """Complete subphase span with duration and status."""
        duration_ms = int((time.time() - start_time) * 1000)
        self._log_session_event(
            "subphase_completed",
            subphase=subphase,
            duration_ms=duration_ms,
            status=status,
            error_message=error_message,
            span_id=self._subphase_span_id,
            parent_span_id=self._phase_span_id,
        )
        self._subphase_span_id = None

    def _request_with_observability(
        self,
        method: str,
        endpoint: str,
        json: dict[str, Any] | None = None,
        response_schema: type[BaseModel] | None = None,
    ) -> dict[str, Any]:
        """Make API request with observability timing events."""
        request_id = uuid.uuid4().hex
        start_time = time.time()
        start_iso = datetime.now(UTC).isoformat()
        parent_span_id = self._subphase_span_id or self._phase_span_id or self._pipeline_span_id
        self._log_session_event(
            "client_request_started",
            request_id=request_id,
            endpoint=endpoint,
            method=method,
            client_request_start_ts=start_iso,
            span_id=self._pipeline_span_id,
            parent_span_id=parent_span_id,
        )
        try:
            response = self._client._request(
                method,
                endpoint,
                json=json,
                response_schema=response_schema,
                request_id=request_id,
                client_request_start_ts=start_time,
            )
            status = "success"
            return cast(dict[str, Any], response)
        except Exception as e:
            status = "error"
            error_message = str(e)
            self._log_session_event(
                "client_request_completed",
                request_id=request_id,
                endpoint=endpoint,
                method=method,
                client_request_start_ts=start_iso,
                client_response_ts=datetime.now(UTC).isoformat(),
                duration_ms=int((time.time() - start_time) * 1000),
                status=status,
                error_class=type(e).__name__,
                error_message=error_message,
                span_id=self._pipeline_span_id,
                parent_span_id=parent_span_id,
            )
            raise
        finally:
            if status == "success":
                self._log_session_event(
                    "client_request_completed",
                    request_id=request_id,
                    endpoint=endpoint,
                    method=method,
                    client_request_start_ts=start_iso,
                    client_response_ts=datetime.now(UTC).isoformat(),
                    duration_ms=int((time.time() - start_time) * 1000),
                    status=status,
                    span_id=self._pipeline_span_id,
                    parent_span_id=parent_span_id,
                )

    @classmethod
    def from_config(
        cls,
        working_dir: Path | None = None,
        on_progress: Callable[[str, dict[str, Any]], None] | None = None,
        on_escalation: Callable[[EscalationNotice], UserDecisionChoice] | None = None,
        on_stream: Callable[[str, str], None] | None = None,
        impl_provider: str | None = None,
        impl_model: str | None = None,
        thinking_level: str | None = None,
        review_config: ReviewConfig | None = None,
        bypass_modes: list[str] | None = None,
        defaults_json: bool = False,
        observability_config: "ObservabilityConfig | None" = None,
        progress_emitter: "ProgressEmitter | None" = None,
        skip_git_check: bool | None = None,
        auto_init_git: bool | None = None,
    ) -> "HybridOrchestrator":
        """Create HybridOrchestrator from configuration.

        Loads APIClient from ~/.obra/client-config.yaml.

        Args:
            working_dir: Working directory for file operations
            on_progress: Optional progress callback
            on_escalation: Optional escalation callback
            on_stream: Optional streaming callback for LLM output
            impl_provider: Optional implementation provider override (S5.T1)
            impl_model: Optional implementation model override (S5.T1)
            thinking_level: Optional thinking level override (S5.T1)
            review_config: Optional review configuration to pass to handlers
            bypass_modes: Optional list of validation modes to bypass
            defaults_json: Whether to output JSON defaults
            observability_config: Optional observability configuration for progress visibility
            progress_emitter: Optional progress emitter for heartbeat and file events
            skip_git_check: Optional CLI flag to skip git validation (overrides config)
            auto_init_git: Optional CLI flag to auto-init git (overrides config)

        Returns:
            Configured HybridOrchestrator

        Raises:
            ConfigurationError: If configuration is invalid or missing
        """
        try:
            client = APIClient.from_config()
        except ConfigurationError:
            raise
        except Exception as e:
            raise ConfigurationError(f"Failed to create API client: {e}")

        # S5.T2: Resolve LLM config with overrides
        from obra.config import resolve_llm_config

        llm_config = resolve_llm_config(
            role="implementation",
            override_provider=impl_provider,
            override_model=impl_model,
            override_thinking_level=thinking_level,
            override_skip_git_check=skip_git_check,
            override_auto_init_git=auto_init_git,
        )

        orchestrator = cls(
            client=client,
            working_dir=working_dir,
            on_progress=on_progress,
            on_escalation=on_escalation,
            on_stream=on_stream,
            review_config=review_config,
            defaults_json=defaults_json,
            observability_config=observability_config,
            progress_emitter=progress_emitter,
        )

        # S5.T2: Store resolved config for handler creation
        orchestrator._llm_config = llm_config
        orchestrator._bypass_modes = bypass_modes or []

        return orchestrator

    @property
    def client(self) -> APIClient:
        """Get the API client."""
        return self._client

    @property
    def working_dir(self) -> Path:
        """Get the working directory."""
        return self._working_dir

    @property
    def session_id(self) -> str | None:
        """Get the current session ID."""
        return self._session_id

    def is_online(self) -> bool:
        """Check if the server is reachable.

        Returns:
            True if server is reachable, False otherwise.
        """
        try:
            self._client.health_check()
            return True
        except ConnectionError as e:
            logger.warning("Health check failed: Network connectivity issue - %s", e)
            return False
        except AuthenticationError as e:
            logger.warning("Health check failed: Authentication error - %s", e)
            return False
        except ConfigurationError as e:
            logger.warning("Health check failed: Configuration error - %s", e)
            return False
        except APIError as e:
            if e.status_code == 401:
                logger.warning("Health check failed: Authentication invalid (401) - %s", e)
            elif e.status_code == 403:
                logger.warning("Health check failed: Access forbidden (403) - %s", e)
            else:
                logger.warning(
                    "Health check failed: API error (status %s) - %s",
                    e.status_code or "unknown",
                    e,
                )
            return False
        except Exception as e:
            logger.warning(
                "Health check failed: Unexpected error (%s) - %s",
                type(e).__name__,
                e,
            )
            return False

    def _ensure_online(self) -> None:
        """Ensure server is reachable.

        Raises:
            ConnectionError: If server is not reachable
        """
        if not self.is_online():
            raise ConnectionError()

    def _hash_working_dir(self) -> str:
        """Create SHA256 hash of working directory path.

        Returns:
            SHA256 hex digest of working directory path
        """
        return hashlib.sha256(str(self._working_dir).encode()).hexdigest()

    def _apply_resolved_llm_config(self, metadata: dict[str, Any]) -> dict[str, str] | None:
        """Apply server-resolved LLM config to local runtime settings."""
        resolved = metadata.get("resolved_llm_config")
        if not isinstance(resolved, dict):
            return None
        if self._llm_config is None:
            self._llm_config = {}
        for key in ("provider", "model", "thinking_level"):
            value = resolved.get(key)
            if value:
                self._llm_config[key] = value
        return {
            "provider": self._llm_config.get("provider", ""),
            "model": self._llm_config.get("model", ""),
            "thinking_level": self._llm_config.get("thinking_level", ""),
        }

    def _get_review_config(self) -> dict[str, Any] | None:
        """Get LLM config for review agents.

        Review agents use the same LLM settings as implementation agents.

        Returns:
            LLM config dict if available, None otherwise.
        """
        if self._llm_config is None:
            logger.debug("No LLM config available for review agents")
            return None

        logger.debug(f"Using LLM config for review agents: provider={self._llm_config.get('provider')}")
        return self._llm_config

    def _get_project_context(self) -> dict[str, Any]:
        """Gather minimal project context (no code content).

        Returns:
            Dictionary with project context (languages, frameworks, etc.)
        """
        context: dict[str, Any] = {
            "languages": [],
            "frameworks": [],
            "has_tests": False,
            "file_count": 0,
        }

        # Detect languages by file extensions
        extensions = set()
        file_count = 0
        try:
            for path in self._working_dir.rglob("*"):
                if path.is_file() and not any(part.startswith(".") for part in path.parts):
                    file_count += 1
                    if path.suffix:
                        extensions.add(path.suffix.lower())
        except Exception:
            pass  # Permission errors, etc.

        context["file_count"] = file_count

        # Map extensions to languages
        ext_to_lang = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".tsx": "typescript",
            ".jsx": "javascript",
            ".go": "go",
            ".rs": "rust",
            ".java": "java",
            ".rb": "ruby",
            ".php": "php",
            ".cs": "csharp",
            ".cpp": "cpp",
            ".c": "c",
        }
        context["languages"] = list(
            {ext_to_lang.get(ext) for ext in extensions if ext in ext_to_lang}
        )

        # Detect common test directories
        test_dirs = ["tests", "test", "__tests__", "spec"]
        context["has_tests"] = any((self._working_dir / d).is_dir() for d in test_dirs)

        # Detect frameworks by config files
        framework_files = {
            "package.json": ["node"],
            "requirements.txt": ["python"],
            "pyproject.toml": ["python"],
            "Cargo.toml": ["rust"],
            "go.mod": ["go"],
            "pom.xml": ["java", "maven"],
            "build.gradle": ["java", "gradle"],
            "Gemfile": ["ruby"],
            "composer.json": ["php"],
        }
        for filename, frameworks in framework_files.items():
            if (self._working_dir / filename).exists():
                context["frameworks"].extend(frameworks)

        context["frameworks"] = list(set(context["frameworks"]))

        return context

    def _emit_progress(self, action: str, payload: dict[str, Any]) -> None:
        """Emit progress update.

        Args:
            action: Action being performed
            payload: Action payload
        """
        if self._on_progress:
            try:
                self._on_progress(action, payload)
            except Exception as e:
                logger.warning(
                    f"Progress callback failed for action '{action}': {e}", exc_info=True
                )

    def _display_bypass_notices(self, server_action: ServerAction) -> None:
        """Render bypass-related warnings for the current action."""
        if server_action.bypass_modes_active:
            print_warning(f"Bypass modes active: {', '.join(server_action.bypass_modes_active)}")
            console.print("  Results may not reflect production behavior.")

        bypassed_p1 = None
        if isinstance(server_action.metadata, dict):
            bypassed_p1 = server_action.metadata.get("bypassed_p1_count")

        if isinstance(bypassed_p1, int) and bypassed_p1 > 0:
            console.print(f"[yellow]Bypassing {bypassed_p1} P1 issues in permissive mode[/yellow]")

    def _should_prompt_for_defaults(self) -> bool:
        """Determine if we should prompt the user for defaults confirmation."""
        if self._defaults_json:
            return False

        return (
            sys.stdin.isatty()
            and os.environ.get("CI") != "true"
            and os.environ.get("OBRA_HEADLESS") != "1"
        )

    def _inject_defaults_into_prompt(
        self,
        base_prompt: str | None,
        defaults: list[dict[str, Any]],
    ) -> str:
        """Append confirmed defaults to the revision prompt."""
        defaults_block = json.dumps(defaults, indent=2)
        prefix = base_prompt or ""
        return (
            f"{prefix}\n\n"
            "# User-confirmed defaults (apply unless overridden)\n"
            "The following defaults were confirmed to unblock refinement. "
            "Incorporate them into the revised plan explicitly:\n"
            f"{defaults_block}\n"
        )

    def _process_proposed_defaults(
        self,
        proposed_defaults: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        """Render and optionally collect confirmation for proposed defaults."""
        if not proposed_defaults:
            return []

        console.print()
        console.print("[bold]Proposed defaults detected[/bold]")

        if self._defaults_json:
            console.print(json.dumps({"proposed_defaults": proposed_defaults}, indent=2))
            raise OrchestratorError(
                "Defaults exported via --defaults-json; rerun interactively to confirm.",
                session_id=self._session_id or "",
            )

        should_prompt = self._should_prompt_for_defaults()
        if not should_prompt:
            print_warning(
                "Non-interactive environment detected; auto-accepting proposed defaults."
            )

        confirmed: list[dict[str, Any]] = []
        for default in proposed_defaults:
            value = default.get("proposed_value", "")
            issue_id = default.get("issue_id", "unknown")
            rationale = default.get("rationale", "")
            confidence = default.get("confidence", 0.0)

            console.print(
                f"[cyan]I'll assume[/cyan] {value} "
                f"[dim](issue {issue_id}, confidence {confidence:.2f})[/dim]"
            )
            if rationale:
                console.print(f"[dim]{rationale}[/dim]")

            if should_prompt:
                console.print(
                    "[dim]Enter a new value to override, 'skip' to reject, or press Enter to accept:[/dim] ",
                    end="",
                )
                try:
                    user_input = input().strip()
                except (EOFError, KeyboardInterrupt):
                    user_input = ""

                if user_input.lower() == "skip":
                    continue
                if user_input:
                    default = {
                        **default,
                        "proposed_value": user_input,
                        "rationale": f"User override: {rationale or 'custom default'}",
                    }

            confirmed.append(default)

        return confirmed

    def _poll_with_backoff(
        self,
        poll_count: int,
        base_delay: float = 1.0,
        max_delay: float = 30.0,
        multiplier: float = 2.0,
    ) -> float:
        """Calculate and execute exponential backoff delay for polling.

        Implements exponential backoff: delay = base_delay * (multiplier ^ poll_count)
        capped at max_delay.

        Args:
            poll_count: Current poll iteration (0-indexed)
            base_delay: Initial delay in seconds (default: 1.0)
            max_delay: Maximum delay in seconds (default: 30.0)
            multiplier: Exponential multiplier (default: 2.0)

        Returns:
            The actual delay used in seconds
        """
        import time

        # Calculate delay with exponential backoff: 1, 2, 4, 8, 16, 30, 30...
        delay = min(base_delay * (multiplier**poll_count), max_delay)
        time.sleep(delay)

        logger.debug(f"Polling wait: {delay:.1f}s (poll #{poll_count + 1})")
        return delay

    def _action_to_phase(self, action: ActionType) -> SessionPhase | None:
        """Map action type to session phase.

        Args:
            action: Action type from server

        Returns:
            Corresponding session phase, or None for non-phase actions
        """
        phase_mapping = {
            ActionType.DERIVE: SessionPhase.DERIVATION,
            ActionType.EXAMINE: SessionPhase.REFINEMENT,
            ActionType.REVISE: SessionPhase.REFINEMENT,
            ActionType.EXECUTE: SessionPhase.EXECUTION,
            ActionType.REVIEW: SessionPhase.REVIEW,
        }
        return phase_mapping.get(action)

    def _emit_phase_event(self, action: ActionType) -> None:
        """Emit phase transition events based on action.

        Tracks phase changes and emits phase_started/phase_completed events
        via the on_progress callback.

        Args:
            action: Current action type
        """
        import time

        new_phase = self._action_to_phase(action)
        if new_phase is None:
            return  # Skip non-phase actions (COMPLETE, ESCALATE, etc.)

        # Check if phase changed
        if new_phase != self._current_phase:
            # Emit phase_completed for previous phase
            if self._current_phase is not None and self._phase_start_time is not None:
                duration_ms = int((time.time() - self._phase_start_time) * 1000)
                self._emit_progress(
                    "phase_completed",
                    {
                        "phase": self._current_phase.value,
                        "duration_ms": duration_ms,
                    },
                )
                # ISSUE-OBS-002: Log phase_completed to production logger
                self._log_session_event(
                    "phase_completed",
                    phase=self._current_phase.value,
                    duration_ms=duration_ms,
                    span_id=self._phase_span_id,
                    parent_span_id=self._pipeline_span_id,
                )
                self._log_resource_snapshot(f"phase_{self._current_phase.value}_end")

            # Emit phase_started for new phase
            self._current_phase = new_phase
            self._phase_start_time = time.time()
            self._phase_span_id = uuid.uuid4().hex
            self._emit_progress(
                "phase_started",
                {
                    "phase": new_phase.value,
                },
            )
            # ISSUE-OBS-002: Log phase_started to production logger
            self._log_session_event(
                "phase_started",
                phase=new_phase.value,
                span_id=self._phase_span_id,
                parent_span_id=self._pipeline_span_id,
            )
            self._log_resource_snapshot(f"phase_{new_phase.value}_start")

    def _git_preflight(self) -> None:
        """Run git repository validation before orchestration begins.

        GIT-HARD-001 Story 2: Git preflight check for hybrid orchestration.

        Validates that the working directory is a git repository before starting
        orchestration. Behavior controlled by llm.git config section.

        Config options:
            llm.git.skip_check (bool): Skip git validation entirely (default: False)
            llm.git.auto_init (bool): Auto-initialize git if missing (default: False)

        Exemptions:
            - Inbox projects (working_dir is None) are exempted from validation

        Raises:
            GitValidationError: If not in git repo and auto_init is False

        Task breakdown:
            S2.T0: Method exists and reads config
            S2.T1: Called before first handler dispatch
            S2.T2: Validates working_dir not cwd
            S2.T3: Exempts Inbox projects
            S2.T4: Logs auto-init actions
        """
        # S2.T3: Exempt Inbox projects (no explicit working_dir provided)
        # When working_dir is not explicitly provided (None in constructor),
        # it defaults to cwd but should be treated as an Inbox project
        if not self._working_dir_explicit:
            logger.debug("Git preflight: Skipping (Inbox project - no explicit working_dir)")
            return

        # Get git config settings (with safe defaults)
        git_config = {}
        if self._llm_config:
            git_config = self._llm_config.get("git", {})

        skip_check = git_config.get("skip_check", False)
        auto_init = git_config.get("auto_init", False)

        # Honor skip_check flag
        if skip_check:
            logger.info("Git preflight: Skipping (llm.git.skip_check enabled)")
            return

        # S2.T2: Validate working_dir not cwd
        # Use self._working_dir which is the project working directory
        logger.debug(f"Git preflight: Validating {self._working_dir}")

        # Import git_utils locally to avoid circular imports
        from obra.utils.git_utils import ensure_git_repository

        try:
            # S2.T4: Log auto-init actions (handled by ensure_git_repository)
            # Note: ensure_git_repository logs auto-init at INFO level
            ensure_git_repository(self._working_dir, auto_init=auto_init)
            logger.info(f"Git preflight: Passed for {self._working_dir}")
        except Exception as e:
            logger.error(f"Git preflight: Failed for {self._working_dir}: {e}")
            raise

    def _get_handler(self, action: ActionType) -> Any:
        """Get handler for action type.

        Lazily imports and instantiates handlers.

        Args:
            action: Action type

        Returns:
            Handler instance

        Raises:
            OrchestratorError: If handler not found
            ConfigurationError: If llm_config is invalid or missing required keys
        """
        if action not in self._handlers:
            # Validate llm_config for handlers that require it (C11)
            # DERIVE, EXAMINE, REVISE, EXECUTE, and FIX all need llm_config
            if action in (
                ActionType.DERIVE,
                ActionType.EXAMINE,
                ActionType.REVISE,
                ActionType.EXECUTE,
                ActionType.FIX,
            ):
                if self._llm_config is None:
                    raise ConfigurationError(
                        f"Cannot create {action.value} handler: llm_config is None. "
                        f"LLM configuration is required for {action.value} actions.",
                        recovery="Run 'obra config' to set up LLM configuration or use 'obra derive' with --model and --provider flags.",
                    )

                # Validate required keys
                required_keys = {"provider"}
                missing_keys = required_keys - set(self._llm_config.keys())
                if missing_keys:
                    raise ConfigurationError(
                        f"Cannot create {action.value} handler: llm_config missing required keys: {missing_keys}. "
                        f"Current config: {self._llm_config}",
                        recovery="Run 'obra config' to set up LLM configuration or use 'obra derive' with --model and --provider flags.",
                    )
            # ISSUE-CLI-016/CLI-017 FIX: Build monitoring context for liveness checks
            # ADR-043 Phase 3: Use helper factory for consistent context construction
            monitoring_context = self.create_monitoring_context()

            # Import handlers lazily to avoid circular imports
            if action == ActionType.DERIVE:
                from obra.hybrid.handlers.derive import DeriveHandler

                # S3.T6: Pass on_stream callback to handler
                # S4.T2: Pass llm_config to handler
                # ISSUE-CLI-016/017: Pass monitoring context
                self._handlers[action] = DeriveHandler(
                    self._working_dir,
                    on_stream=self._on_stream,
                    llm_config=self._llm_config,
                    log_event=self._log_session_event,
                    trace_id=self._trace_id,
                    parent_span_id=self._phase_span_id,
                    monitoring_context=monitoring_context,
                    bypass_modes=self._bypass_modes,
                    plan_context=self._plan_context,
                )
            elif action == ActionType.EXAMINE:
                from obra.hybrid.handlers.examine import ExamineHandler

                # S3.T6: Pass on_stream callback to handler
                # S4.T3: Pass llm_config to handler
                # ISSUE-CLI-016/017: Pass monitoring context
                self._handlers[action] = ExamineHandler(
                    self._working_dir,
                    on_stream=self._on_stream,
                    llm_config=self._llm_config,
                    log_event=self._log_session_event,
                    trace_id=self._trace_id,
                    parent_span_id=self._phase_span_id,
                    monitoring_context=monitoring_context,
                )
            elif action == ActionType.REVISE:
                from obra.hybrid.handlers.revise import ReviseHandler

                # S3.T6: Pass on_stream callback to handler
                # S4.T4: Pass llm_config to handler
                # ISSUE-CLI-016/017: Pass monitoring context
                self._handlers[action] = ReviseHandler(
                    self._working_dir,
                    on_stream=self._on_stream,
                    llm_config=self._llm_config,
                    log_event=self._log_session_event,
                    trace_id=self._trace_id,
                    parent_span_id=self._phase_span_id,
                    monitoring_context=monitoring_context,
                )
            elif action == ActionType.EXECUTE:
                from obra.hybrid.handlers.execute import ExecuteHandler

                # S5.T3: Pass llm_config to ExecuteHandler
                # ISSUE-OBS-003: Pass observability context for cross-process propagation
                # S2.T4: Pass observability_config and progress_emitter for heartbeat
                log_file = (
                    Path(os.environ.get("OBRA_RUNTIME_DIR", "~/obra-runtime")).expanduser()
                    / "logs"
                    / "hybrid.jsonl"
                )
                self._handlers[action] = ExecuteHandler(
                    self._working_dir,
                    llm_config=self._llm_config,
                    session_id=self._session_id,
                    log_file=log_file,
                    trace_id=self._trace_id,
                    log_event=self._log_session_event,
                    parent_span_id=self._phase_span_id,
                    observability_config=self._observability_config,
                    progress_emitter=self._progress_emitter,
                    on_stream=self._on_stream,
                )
            elif action == ActionType.REVIEW:
                from obra.hybrid.handlers.review import ReviewHandler

                self._handlers[action] = ReviewHandler(
                    self._working_dir,
                    llm_config=self._get_review_config(),
                    review_config=self._review_config,
                    log_event=self._log_session_event,
                    trace_id=self._trace_id,
                    parent_span_id=self._phase_span_id,
                )
            elif action == ActionType.FIX:
                from obra.hybrid.handlers.fix import FixHandler

                # ISSUE-OBS-003: Pass observability context for cross-process propagation
                # S3.T2: Pass observability_config and progress_emitter for heartbeat
                log_file = (
                    Path(os.environ.get("OBRA_RUNTIME_DIR", "~/obra-runtime")).expanduser()
                    / "logs"
                    / "hybrid.jsonl"
                )
                self._handlers[action] = FixHandler(
                    self._working_dir,
                    llm_config=self._llm_config,
                    session_id=self._session_id,
                    log_file=log_file,
                    trace_id=self._trace_id,
                    log_event=self._log_session_event,
                    parent_span_id=self._phase_span_id,
                    observability_config=self._observability_config,
                    progress_emitter=self._progress_emitter,
                    on_stream=self._on_stream,
                )
            else:
                raise OrchestratorError(
                    f"No handler for action: {action.value}",
                    session_id=self._session_id or "",
                )

        return self._handlers[action]

    def _handle_action(self, server_action: ServerAction) -> dict[str, Any]:
        """Handle a server action by dispatching to appropriate handler.

        Args:
            server_action: Server action to handle

        Returns:
            Result to report back to server

        Raises:
            OrchestratorError: If action handling fails
        """
        action = server_action.action
        payload = server_action.payload

        logger.info(f"Handling action: {action.value} (iteration {server_action.iteration})")

        # S3.T3: Emit phase transition events
        self._emit_phase_event(action)

        self._emit_progress(action.value, payload)

        # Handle special actions
        if action == ActionType.COMPLETE:
            completion_notice = CompletionNotice.from_payload(payload)
            return {"completed": True, "notice": completion_notice}

        if action == ActionType.ESCALATE:
            escalation_notice = EscalationNotice.from_payload(payload)
            return self._handle_escalation(escalation_notice)

        if action == ActionType.ERROR:
            error_msg = server_action.error_message or "Unknown server error"
            error_code = server_action.error_code or "UNKNOWN"
            raise OrchestratorError(
                f"Server error [{error_code}]: {error_msg}",
                session_id=self._session_id or "",
            )

        if action == ActionType.WAIT:
            # Server is processing async, wait and poll
            return {"waiting": True}

        # Get handler for action
        handler = self._get_handler(action)

        # Create typed request from payload and dispatch to handler
        if action == ActionType.DERIVE:
            derive_req = DeriveRequest.from_payload(payload)
            subphase_start = self._start_subphase("derive")
            if hasattr(handler, "_parent_span_id"):
                handler._parent_span_id = self._subphase_span_id
            # ISSUE-OBS-002: Log derivation_started event
            self._log_session_event(
                "derivation_started",
                objective=derive_req.objective,
                plan_id=getattr(derive_req, "plan_id", None),
                span_id=self._subphase_span_id,
                parent_span_id=self._phase_span_id,
            )
            try:
                result = cast(dict[str, Any], handler.handle(derive_req))
            except Exception as e:
                self._complete_subphase("derive", subphase_start, status="error", error_message=str(e))
                if self._current_phase:
                    self._log_session_event(
                        "phase_failed",
                        phase=self._current_phase.value,
                        failure_stage="derive",
                        error_code="HANDLER_ERROR",
                        error_class=type(e).__name__,
                        error_message=str(e),
                        span_id=self._phase_span_id,
                        parent_span_id=self._pipeline_span_id,
                    )
                raise
            # ISSUE-OBS-002: Log derivation_complete event
            self._log_session_event(
                "derivation_complete",
                plan_items_count=len(result.get("plan_items", [])),
                span_id=self._subphase_span_id,
                parent_span_id=self._phase_span_id,
            )
            self._complete_subphase("derive", subphase_start)
            return result
        if action == ActionType.EXAMINE:
            examine_req = ExamineRequest.from_payload(payload)
            subphase_start = self._start_subphase("examine")
            if hasattr(handler, "_parent_span_id"):
                handler._parent_span_id = self._subphase_span_id
            try:
                result = cast(dict[str, Any], handler.handle(examine_req))
            except Exception as e:
                self._complete_subphase("examine", subphase_start, status="error", error_message=str(e))
                if self._current_phase:
                    self._log_session_event(
                        "phase_failed",
                        phase=self._current_phase.value,
                        failure_stage="examine",
                        error_code="HANDLER_ERROR",
                        error_class=type(e).__name__,
                        error_message=str(e),
                        span_id=self._phase_span_id,
                        parent_span_id=self._pipeline_span_id,
                    )
                raise
            self._complete_subphase("examine", subphase_start)
            return result
        if action == ActionType.REVISE:
            revise_req = RevisionRequest.from_payload(payload)
            subphase_start = self._start_subphase("revise")
            if hasattr(handler, "_parent_span_id"):
                handler._parent_span_id = self._subphase_span_id

            proposed_defaults = revise_req.proposed_defaults or payload.get("proposed_defaults") or []
            try:
                if proposed_defaults:
                    confirmed_defaults = self._process_proposed_defaults(proposed_defaults)
                    revise_req.base_prompt = self._inject_defaults_into_prompt(
                        revise_req.base_prompt,
                        confirmed_defaults,
                    )
                    revise_req.proposed_defaults = confirmed_defaults
            except OrchestratorError:
                self._complete_subphase(
                    "revise",
                    subphase_start,
                    status="error",
                    error_message="defaults confirmation aborted",
                )
                raise
            try:
                result = cast(dict[str, Any], handler.handle(revise_req))
            except Exception as e:
                self._complete_subphase("revise", subphase_start, status="error", error_message=str(e))
                if self._current_phase:
                    self._log_session_event(
                        "phase_failed",
                        phase=self._current_phase.value,
                        failure_stage="revise",
                        error_code="HANDLER_ERROR",
                        error_class=type(e).__name__,
                        error_message=str(e),
                        span_id=self._phase_span_id,
                        parent_span_id=self._pipeline_span_id,
                    )
                raise
            self._complete_subphase("revise", subphase_start)
            return result
        if action == ActionType.EXECUTE:
            execute_req = ExecutionRequest.from_payload(payload)
            subphase_start = self._start_subphase("execute")
            if hasattr(handler, "_parent_span_id"):
                handler._parent_span_id = self._subphase_span_id
            if execute_req.current_item and execute_req.current_item.get("id"):
                self._last_item_id = execute_req.current_item.get("id")

            # --continue-from: Skip items that were completed in the source session
            if self._skip_completed_items and execute_req.current_item:
                item_title = execute_req.current_item.get("title", "")
                if item_title in self._skip_completed_items:
                    logger.info(f"Skipping completed item: {item_title}")
                    self._emit_progress("item_skipped", {
                        "item": execute_req.current_item,
                        "reason": "completed_in_previous_session",
                    })
                    self._log_session_event(
                        "item_skipped",
                        item=execute_req.current_item,
                        reason="completed_in_previous_session",
                        span_id=self._subphase_span_id,
                        parent_span_id=self._phase_span_id,
                    )
                    self._complete_subphase("execute", subphase_start, status="skipped")
                    return {
                        "item_id": execute_req.current_item.get("id", ""),
                        "status": "completed",  # Report as completed since it was in previous session
                        "summary": f"Skipped (completed in previous session): {item_title}",
                        "files_changed": 0,
                        "tests_passed": True,
                    }

            # Compatibility: some server versions return ActionType.EXECUTE with fix payload
            # (item_id + issues_to_fix) instead of ActionType.FIX. Route to FixHandler but report as FIX.
            if execute_req.current_item is None and payload.get("issues_to_fix"):
                fix_handler = self._get_handler(ActionType.FIX)
                if hasattr(fix_handler, "_parent_span_id"):
                    fix_handler._parent_span_id = self._subphase_span_id
                fix_req = FixRequest.from_payload(payload)
                try:
                    fix_result = cast(dict[str, Any], fix_handler.handle(fix_req))
                except Exception as e:
                    self._complete_subphase(
                        "execute",
                        subphase_start,
                        status="error",
                        error_message=str(e),
                    )
                    if self._current_phase:
                        self._log_session_event(
                            "phase_failed",
                            phase=self._current_phase.value,
                            failure_stage="execute",
                            error_code="HANDLER_ERROR",
                            error_class=type(e).__name__,
                            error_message=str(e),
                            span_id=self._phase_span_id,
                            parent_span_id=self._pipeline_span_id,
                        )
                    raise
                fix_result["_report_as"] = ActionType.FIX.value
                self._complete_subphase("execute", subphase_start)
                return fix_result

            # S3.T5: Emit item_started event
            if execute_req.current_item:
                self._emit_progress("item_started", {"item": execute_req.current_item})
                # ISSUE-OBS-002: Log item_started to production logger
                self._log_session_event(
                    "item_started",
                    item=execute_req.current_item,
                    span_id=self._subphase_span_id,
                    parent_span_id=self._phase_span_id,
                )

            try:
                result = cast(dict[str, Any], handler.handle(execute_req))
            except Exception as e:
                self._complete_subphase("execute", subphase_start, status="error", error_message=str(e))
                if self._current_phase:
                    self._log_session_event(
                        "phase_failed",
                        phase=self._current_phase.value,
                        failure_stage="execute",
                        error_code="HANDLER_ERROR",
                        error_class=type(e).__name__,
                        error_message=str(e),
                        span_id=self._phase_span_id,
                        parent_span_id=self._pipeline_span_id,
                    )
                raise

            # S3.T5: Emit item_completed event
            if execute_req.current_item:
                self._emit_progress(
                    "item_completed",
                    {"item": execute_req.current_item, "result": result},
                )
                # ISSUE-OBS-002: Log item_completed to production logger
                self._log_session_event(
                    "item_completed",
                    item=execute_req.current_item,
                    status=result.get("status", "unknown"),
                    files_changed=result.get("files_changed", 0),
                    span_id=self._subphase_span_id,
                    parent_span_id=self._phase_span_id,
                )

            self._complete_subphase("execute", subphase_start)
            return result
        if action == ActionType.REVIEW:
            review_payload = payload
            if not payload.get("item_id") and self._last_item_id:
                review_payload = dict(payload)
                review_payload["item_id"] = self._last_item_id
            review_req = ReviewRequest.from_payload(review_payload)
            if review_req.item_id:
                self._last_item_id = review_req.item_id
            subphase_start = self._start_subphase("review")
            if hasattr(handler, "_parent_span_id"):
                handler._parent_span_id = self._subphase_span_id
            try:
                result = cast(dict[str, Any], handler.handle(review_req))
            except Exception as e:
                self._complete_subphase("review", subphase_start, status="error", error_message=str(e))
                if self._current_phase:
                    self._log_session_event(
                        "phase_failed",
                        phase=self._current_phase.value,
                        failure_stage="review",
                        error_code="HANDLER_ERROR",
                        error_class=type(e).__name__,
                        error_message=str(e),
                        span_id=self._phase_span_id,
                        parent_span_id=self._pipeline_span_id,
                    )
                raise
            self._complete_subphase("review", subphase_start)
            return result
        if action == ActionType.FIX:
            fix_payload = payload
            if not payload.get("item_id") and self._last_item_id:
                fix_payload = dict(payload)
                fix_payload["item_id"] = self._last_item_id
            fix_req = FixRequest.from_payload(fix_payload)
            if fix_req.item_id:
                self._last_item_id = fix_req.item_id
            subphase_start = self._start_subphase("fix")
            if hasattr(handler, "_parent_span_id"):
                handler._parent_span_id = self._subphase_span_id
            try:
                result = cast(dict[str, Any], handler.handle(fix_req))
            except Exception as e:
                self._complete_subphase("fix", subphase_start, status="error", error_message=str(e))
                if self._current_phase:
                    self._log_session_event(
                        "phase_failed",
                        phase=self._current_phase.value,
                        failure_stage="fix",
                        error_code="HANDLER_ERROR",
                        error_class=type(e).__name__,
                        error_message=str(e),
                        span_id=self._phase_span_id,
                        parent_span_id=self._pipeline_span_id,
                    )
                raise
            self._complete_subphase("fix", subphase_start)
            return result
        raise OrchestratorError(
            f"Unhandled action: {action.value}",
            session_id=self._session_id or "",
        )

    def _handle_escalation(self, notice: EscalationNotice) -> dict[str, Any]:
        """Handle escalation by prompting user.

        Args:
            notice: Escalation notice from server

        Returns:
            User decision result
        """
        # If callback provided, use it
        if self._on_escalation:
            decision = self._on_escalation(notice)
            return {
                "escalation_id": notice.escalation_id,
                "decision": decision.value,
                "reason": "",
            }

        # Default: display and force complete
        print_warning(f"Escalation: {notice.reason.value}")

        # Defensive check for blocking_issues structure
        blocking_issues = notice.blocking_issues
        if not isinstance(blocking_issues, list):
            logger.warning(
                f"Invalid blocking_issues type: expected list, got {type(blocking_issues).__name__}. "
                f"Converting to empty list."
            )
            blocking_issues = []
        else:
            # Ensure all items are dicts
            validated_issues = []
            for idx, issue in enumerate(blocking_issues):
                if not isinstance(issue, dict):
                    logger.warning(
                        f"Invalid blocking_issue at index {idx}: expected dict, got {type(issue).__name__}. "
                        f"Skipping item."
                    )
                else:
                    validated_issues.append(issue)
            blocking_issues = validated_issues

        console.print(f"  Blocking issues: {len(blocking_issues)}")
        for issue in blocking_issues[:5]:  # Show first 5
            priority = issue.get("priority", "P3")
            description = issue.get("description", "Unknown")
            console.print(f"    - [{priority}] {description}")

        # Show validated item count if available in iteration_history
        if notice.iteration_history:
            last_iteration = notice.iteration_history[-1] if notice.iteration_history else {}
            validated = last_iteration.get("validated_count")
            total = last_iteration.get("total_items")
            if validated is not None and total is not None:
                console.print(f"\n  Plan items validated: {validated} of {total}")

        # Show --permissive tip for refinement-related escalations
        refinement_reasons = {
            EscalationReason.MAX_ITERATIONS,
            EscalationReason.MAX_REFINEMENT_ITERATIONS,
            EscalationReason.BLOCKED,
            EscalationReason.QUALITY_THRESHOLD_NOT_MET,
        }
        if notice.reason in refinement_reasons and blocking_issues:
            console.print("\n  [bold]Tip:[/bold] Use --permissive to bypass P1 issues and proceed.")
            console.print("       Or clarify your objective and retry, e.g.:")
            console.print('       "Add feature X (use library Y, handle errors with Z)"')

        return {
            "escalation_id": notice.escalation_id,
            "decision": UserDecisionChoice.FORCE_COMPLETE.value,
            "reason": "Auto-completed (no interactive handler)",
        }

    def _report_result(
        self,
        action: ActionType,
        result: dict[str, Any],
    ) -> ServerAction:
        """Report action result to server.

        Args:
            action: Action that was handled
            result: Result from handler

        Returns:
            Next server action
        """
        if not self._session_id:
            raise OrchestratorError("No active session")

        try:
            if action == ActionType.DERIVE:
                response = self._request_with_observability(
                    "POST",
                    "report_derivation",
                    json=DerivedPlan(
                        session_id=self._session_id,
                        plan_items=result.get("plan_items", []),
                        raw_response=result.get("raw_response", ""),
                    ).to_dict(),
                )
            elif action == ActionType.EXAMINE:
                response = self._request_with_observability(
                    "POST",
                    "report_examination",
                    json=ExaminationReport(
                        session_id=self._session_id,
                        iteration=result.get("iteration", 0),
                        issues=result.get("issues", []),
                        thinking_budget_used=result.get("thinking_budget_used", 0),
                        thinking_fallback=result.get("thinking_fallback", False),
                        raw_response=result.get("raw_response", ""),
                    ).to_dict(),
                )
            elif action == ActionType.REVISE:
                response = self._request_with_observability(
                    "POST",
                    "report_revision",
                    json=RevisedPlan(
                        session_id=self._session_id,
                        plan_items=result.get("plan_items", []),
                        changes_summary=result.get("changes_summary", ""),
                        raw_response=result.get("raw_response", ""),
                    ).to_dict(),
                )
            elif action == ActionType.EXECUTE:
                response = self._request_with_observability(
                    "POST",
                    "report_execution",
                    json=ExecutionResult(
                        session_id=self._session_id,
                        item_id=result.get("item_id", ""),
                        status=ExecutionStatus(result.get("status", "failure")),
                        summary=result.get("summary", ""),
                        files_changed=result.get("files_changed", 0),
                        tests_passed=result.get("tests_passed", False),
                        test_count=result.get("test_count", 0),
                        coverage_delta=result.get("coverage_delta", 0.0),
                    ).to_dict(),
                )
            elif action == ActionType.REVIEW:
                agent_reports = result.get("agent_reports", [])
                item_id = result.get("item_id") or self._last_item_id or ""
                # ISSUE-SAAS-015: Map client status values to server API contract
                # Client uses: complete, timeout, error, skipped (execution state)
                # Server expects: pass, fail, warning (quality assessment)
                status_mapping = {
                    "complete": "pass",  # Completed successfully = pass
                    "timeout": "warning",  # Timed out = warning (couldn't complete)
                    "error": "fail",  # Error = fail
                    "skipped": "pass",  # BUG-fad06fe5: Skipped (no files) = pass with 0 issues
                }
                mapped_reports = []
                for report in agent_reports:
                    mapped_report = dict(report)  # Shallow copy
                    client_status = mapped_report.get("status", "complete")
                    mapped_report["status"] = status_mapping.get(client_status, client_status)
                    mapped_reports.append(mapped_report)
                response = self._request_with_observability(
                    "POST",
                    "report_review",
                    json={
                        "session_id": self._session_id,
                        "item_id": item_id,
                        "agent_reports": mapped_reports,
                        "iteration": result.get("iteration", 0),
                    },
                )
            elif action == ActionType.FIX:
                fix_results = result.get("fix_results", [])
                item_id = result.get("item_id") or self._last_item_id or ""
                response = self._request_with_observability(
                    "POST",
                    "report_fix",
                    json={
                        "session_id": self._session_id,
                        "item_id": item_id,  # ISSUE-SAAS-021: Include for fix-review loop
                        "fixes_applied": result.get("fixed_count", 0),
                        "fixes_failed": result.get("failed_count", 0),
                        "fix_details": [
                            {
                                "issue_id": fr.get("issue_id", ""),
                                "status": fr.get("status", ""),
                                "summary": fr.get(
                                    "summary", ""
                                ),  # BUG-SCHEMA-002: Get from fix result, not verification
                            }
                            for fr in fix_results
                        ],
                    },
                )
            elif action == ActionType.ESCALATE:
                response = self._request_with_observability(
                    "POST",
                    "user_decision",
                    json=UserDecision(
                        session_id=self._session_id,
                        escalation_id=result.get("escalation_id", ""),
                        decision=UserDecisionChoice(result.get("decision", "force_complete")),
                        reason=result.get("reason", ""),
                    ).to_dict(),
                )
            else:
                raise OrchestratorError(
                    f"Cannot report result for action: {action.value}",
                    session_id=self._session_id,
                )

            server_action = ServerAction.from_dict(response)
            self._display_bypass_notices(server_action)
            return server_action

        except APIError:
            raise
        except Exception as e:
            raise OrchestratorError(
                f"Failed to report result: {e}",
                session_id=self._session_id,
            )

    def _parse_polling_action_response(
        self,
        response: dict[str, Any],
        iteration: int,
    ) -> ServerAction:
        """Parse polling responses from get_session_action into ServerAction.

        Supports both full ServerAction payloads and the polling shape:
        {action, reason, confidence, status}.
        """
        if "session_id" in response:
            return ServerAction.from_dict(response)

        if "action" in response and "status" in response:
            logger.info(
                "Polling response missing session_id; adapting to ServerAction "
                "(action=%s, status=%s).",
                response.get("action"),
                response.get("status"),
            )
            adapted = {
                "action": response.get("action", ActionType.WAIT.value),
                "session_id": self._session_id or "",
                "iteration": iteration,
                "payload": {"polling": response},
                "metadata": {"polling_adapted": True},
            }
            return ServerAction.from_dict(adapted)

        raise OrchestratorError(
            f"Unexpected polling response shape: {response}",
            session_id=self._session_id,
        )

    def derive(
        self,
        objective: str,
        working_dir: Path | None = None,
        project_id: str | None = None,
        repo_root: str | None = None,
        llm_provider: str = "anthropic",
        max_iterations: int | None = None,
        plan_id: str | None = None,
        plan_context: dict[str, Any] | None = None,
        plan_only: bool = False,
        bypass_modes: list[str] | None = None,
        skip_completed_items: list[str] | None = None,
    ) -> CompletionNotice:
        """Start a new derivation session.

        This is the main entry point for the hybrid orchestration loop.
        It creates a new session, derives a plan, refines it, executes
        the plan items, runs quality review, and completes the session.

        Args:
            objective: Task objective to plan and execute
            working_dir: Working directory (overrides instance default)
            project_id: Optional project ID override
            repo_root: Optional git repo root (absolute path, not sent to server)
            llm_provider: LLM provider to use
            max_iterations: Maximum orchestration loop iterations (None = use config)
            plan_id: Optional reference to uploaded plan (for plan import workflow)
            plan_context: Optional plan context from local plan file (plan import workflow)
            plan_only: If True, stop before execution once plan is ready (default: False)
            skip_completed_items: List of task titles to skip (for --continue-from recovery)

        Returns:
            CompletionNotice with session summary

        Raises:
            ConnectionError: If server is not reachable
            OrchestratorError: If orchestration fails
        """
        if bypass_modes is not None:
            self._bypass_modes = bypass_modes

        # Store skip_completed_items for --continue-from recovery
        self._skip_completed_items = skip_completed_items or []

        # Resolve max_iterations from config if not provided
        if max_iterations is None:
            max_iterations = get_max_iterations()

        # Update working dir if provided
        if working_dir:
            self._working_dir = working_dir

        # Store client-side plan context (if provided)
        self._plan_context = plan_context

        # Privacy: repo_root is intentionally unused because server no longer accepts path fields
        _ = repo_root

        # S2.T1: Run git preflight check before starting session
        # GIT-HARD-001: Validate git repository before orchestration begins
        self._git_preflight()

        # Ensure we can reach the server
        self._ensure_online()

        # Gather project context
        project_context = self._get_project_context()
        project_hash = self._hash_working_dir()

        # Get client version
        try:
            from obra import __version__ as client_version
        except ImportError:
            client_version = "0.0.0-dev"

        # Initialize trace context for end-to-end observability
        if not self._trace_id:
            self._trace_id = uuid.uuid4().hex
        self._pipeline_span_id = uuid.uuid4().hex
        self._pipeline_start_time = time.time()
        try:
            self._client.set_trace_context(self._trace_id, span_id=self._pipeline_span_id)
        except Exception:
            logger.debug("Failed to set trace context on API client", exc_info=True)
        self._event_logger.set_trace_context(self._trace_id, span_id=self._pipeline_span_id)

        # Log pipeline start for end-to-end timing
        self._log_session_event(
            "pipeline_started",
            objective=objective[:200] if len(objective) > 200 else objective,
            working_dir=str(self._working_dir),
            client_version=client_version,
            span_id=self._pipeline_span_id,
        )
        self._log_resource_snapshot("pipeline_start")

        # Start session
        print_info(f"Starting session for: {objective[:50]}...")
        logger.info(f"Starting session: {objective}")

        # Extract LLM config from stored _llm_config (ISSUE-CLI-005 fix)
        impl_provider = None
        impl_model = None
        thinking_level = None
        if hasattr(self, "_llm_config") and self._llm_config:
            impl_provider = self._llm_config.get("provider")
            impl_model = self._llm_config.get("model")
            thinking_level = self._llm_config.get("thinking_level")
            # Use provider from _llm_config if available
            provider_override = self._llm_config.get("provider")
            if isinstance(provider_override, str):
                llm_provider = provider_override

        try:
            response = self._request_with_observability(
                "POST",
                "hybrid_orchestrate",
                json=SessionStart(
                    objective=objective,
                    project_hash=project_hash,
                    project_id=project_id,
                    project_context=project_context,
                    client_version=client_version,
                    llm_provider=llm_provider,
                    impl_provider=impl_provider,
                    impl_model=impl_model,
                    thinking_level=thinking_level,
                    plan_id=plan_id,
                    bypass_modes=bypass_modes or self._bypass_modes,
                ).to_dict(),
            )
        except APIError as e:
            raise OrchestratorError(
                f"Failed to start session: {e}",
                recovery="Check your authentication with 'obra whoami'",
            )

        # Parse server response
        server_action = ServerAction.from_dict(response)
        self._session_id = server_action.session_id

        # Start session console logging for feedback system
        try:
            from obra.feedback import start_session_logging
            start_session_logging(self._session_id)
            logger.debug(f"Session console logging started: {self._session_id}")
        except Exception as e:
            # Don't fail orchestration if session logging fails
            logger.warning(f"Failed to start session console logging: {e}")

        self._display_bypass_notices(server_action)

        resolved_llm = self._apply_resolved_llm_config(server_action.metadata)
        if resolved_llm:
            provider = resolved_llm.get("provider", "unknown")
            model = resolved_llm.get("model", "default")
            thinking = resolved_llm.get("thinking_level", "medium")
            console.print(f"[dim]LLM (server): {provider} ({model}) | thinking: {thinking}[/dim]")

        project_notice = server_action.metadata.get("project_notice")
        if project_notice:
            print_info(project_notice)
        project_warning = server_action.metadata.get("project_warning")
        if project_warning:
            print_warning(project_warning)

        if server_action.is_error():
            raise OrchestratorError(
                server_action.error_message or "Failed to start session",
                session_id=self._session_id,
            )

        logger.info(f"Session started: {self._session_id}")
        print_info(f"Session: {self._session_id[:8]}...")

        # ISSUE-OBS-002: Log session_started event for observability
        # FEAT-MODEL-QUALITY-001 S3.T2: Include quality_tier for audit trail
        quality_tier = resolve_quality_tier(llm_provider, impl_model or "")
        self._log_session_event(
            "session_started",
            objective=objective,
            working_dir=str(self._working_dir),
            llm_provider=llm_provider,
            plan_id=plan_id,
            client_version=client_version,
            quality_tier=quality_tier,
        )

        # Main orchestration loop
        iteration = 0
        poll_count = 0  # Track consecutive WAIT responses for backoff
        try:
            while iteration < max_iterations:
                iteration += 1
                logger.debug(f"Orchestration loop iteration {iteration}")

                # Handle current action
                result = self._handle_action(server_action)

                # Check for completion
                if result.get("completed"):
                    notice = result.get("notice")
                    if isinstance(notice, CompletionNotice):
                        logger.info(f"Session completed: {self._session_id}")
                        # ISSUE-OBS-002: Log session_completed event
                        self._log_session_event(
                            "session_completed",
                            items_completed=notice.items_completed,
                            total_iterations=notice.total_iterations,
                            quality_score=notice.quality_score,
                        )
                        self._log_pipeline_completed()
                        return notice
                    # Create notice from result if not already
                    notice = CompletionNotice(
                        session_summary=result.get("session_summary", ""),
                        items_completed=result.get("items_completed", 0),
                        total_iterations=result.get("total_iterations", iteration),
                        quality_score=result.get("quality_score", 0.0),
                    )
                    # ISSUE-OBS-002: Log session_completed event for alternate completion path
                    self._log_session_event(
                        "session_completed",
                        items_completed=notice.items_completed,
                        total_iterations=notice.total_iterations,
                        quality_score=notice.quality_score,
                    )
                    self._log_pipeline_completed()
                    return notice

                # Check for waiting (async processing)
                if result.get("waiting"):
                    self._poll_with_backoff(poll_count)
                    poll_count += 1
                    # Poll server for updated action
                    # ISSUE-009 Bug #3: Use query param format (not path param)
                    # Cloud Functions routing: get_session_action?session_id={id}
                    try:
                        response = self._request_with_observability(
                            "GET",
                            f"get_session_action?session_id={self._session_id}",
                        )
                        server_action = self._parse_polling_action_response(
                            response,
                            iteration,
                        )
                        self._display_bypass_notices(server_action)
                        # Reset failure count on successful poll
                        self._polling_failure_count = 0
                    except APIError as e:
                        # Increment failure counter
                        self._polling_failure_count += 1

                        # ISSUE-CLI-012: Fast-fail on non-retryable errors (404, 401, 403)
                        # These errors indicate endpoint doesn't exist or auth failure
                        if hasattr(e, "status_code") and e.status_code in (404, 401, 403):
                            logger.error(
                                f"Polling endpoint returned non-retryable error {e.status_code}. "
                                f"Session: {self._session_id}, "
                                f"Endpoint likely does not exist or auth failed. "
                                f"Error: {e}"
                            )
                            raise OrchestratorError(
                                f"Polling endpoint failed with non-retryable error (HTTP {e.status_code}). "
                                f"The get_session_action?session_id={self._session_id} endpoint may not exist or requires authentication. "
                                f"Original error: {e}",
                                session_id=self._session_id,
                                recovery=f"Check server logs for endpoint availability. Resume with: obra resume --session-id {self._session_id}",
                            )

                        # Log warning on each failure
                        logger.warning(
                            f"Polling backoff exception (attempt {self._polling_failure_count}): {e}"
                        )

                        # After 5 consecutive failures, log error with diagnostics
                        if self._polling_failure_count >= 5:
                            logger.error(
                                f"Polling endpoint failed {self._polling_failure_count} consecutive times. "
                                f"Session: {self._session_id}, "
                                f"Poll count: {poll_count}, "
                                f"Iteration: {iteration}, "
                                f"Last error: {e}"
                            )

                        # ISSUE-CLI-012: Circuit breaker - exit after max retries
                        if self._polling_failure_count >= MAX_POLLING_RETRIES:
                            logger.error(
                                f"Polling circuit breaker triggered after {MAX_POLLING_RETRIES} consecutive failures. "
                                f"Session: {self._session_id}, "
                                f"Last error: {e}"
                            )
                            raise OrchestratorError(
                                f"Polling endpoint failed after {MAX_POLLING_RETRIES} consecutive attempts. "
                                f"Session: {self._session_id}. "
                                f"This may indicate the endpoint does not exist or the server is not responding. "
                                f"Last error: {e}",
                                session_id=self._session_id,
                                recovery=f"Check server logs for endpoint availability. Resume with: obra resume --session-id {self._session_id}",
                            )

                        # Continue with current action if polling endpoint not available
                    continue
                # Reset poll count when not waiting
                poll_count = 0

                # Report result and get next action
                report_as = result.pop("_report_as", None)
                action_to_report = (
                    ActionType(report_as)
                    if isinstance(report_as, str) and report_as
                    else server_action.action
                )
                server_action = self._report_result(action_to_report, result)

                # Plan-only mode: stop before execution once plan is ready.
                if plan_only and server_action.action in (
                    ActionType.EXECUTE,
                    ActionType.REVIEW,
                    ActionType.FIX,
                ):
                    if action_to_report == ActionType.REVISE:
                        plan_summary = result.get("changes_summary", "Plan revised")
                        items_count = len(result.get("plan_items", []))
                    elif action_to_report == ActionType.EXAMINE:
                        issues_count = len(result.get("issues", []))
                        plan_summary = f"Plan examined with {issues_count} issue(s)"
                        items_count = 0
                    else:
                        plan_summary = "Plan-only mode: stopping before execution"
                        items_count = len(result.get("plan_items", []))

                    notice = CompletionNotice(
                        session_summary=f"Plan-only mode: {plan_summary}",
                        items_completed=0,
                        total_iterations=iteration,
                        quality_score=0.0,
                    )

                    logger.info(f"Plan-only session completed: {self._session_id}")
                    self._log_session_event(
                        "session_completed",
                        plan_only=True,
                        plan_items_count=items_count,
                        total_iterations=iteration,
                    )
                    self._log_pipeline_completed()
                    return notice

                # Check for error response
                if server_action.is_error():
                    raise OrchestratorError(
                        server_action.error_message or "Server returned error",
                        session_id=self._session_id,
                    )

            # Max iterations reached
            raise OrchestratorError(
                f"Orchestration loop exceeded {max_iterations} iterations",
                session_id=self._session_id,
                recovery=f"This may indicate a bug. Resume with: obra resume --session-id {self._session_id}",
            )
        except Exception as e:
            error_message = str(e)
            error_class = type(e).__name__
            self._log_session_event(
                "pipeline_failed",
                failure_stage=self._current_phase.value if self._current_phase else "unknown",
                error_code="ORCHESTRATOR_ERROR",
                error_class=error_class,
                error_message=error_message,
                span_id=self._pipeline_span_id,
            )
            if self._current_phase:
                self._log_session_event(
                    "phase_failed",
                    phase=self._current_phase.value,
                    failure_stage="orchestration_loop",
                    error_code="ORCHESTRATOR_ERROR",
                    error_class=error_class,
                    error_message=error_message,
                    span_id=self._phase_span_id,
                    parent_span_id=self._pipeline_span_id,
                )
            # ISSUE-OBS-003: Emit session_failed to properly close session lifecycle
            self._log_session_event(
                "session_failed",
                error_code="ORCHESTRATOR_ERROR",
                error_class=error_class,
                error_message=error_message,
                phase=self._current_phase.value if self._current_phase else "unknown",
            )
            raise

    def resume(self, session_id: str) -> CompletionNotice:
        """Resume an interrupted session.

        Args:
            session_id: Session ID to resume

        Returns:
            CompletionNotice with session summary

        Raises:
            ConnectionError: If server is not reachable
            OrchestratorError: If session cannot be resumed
        """
        self._ensure_online()

        # Initialize trace context for resumed run
        if not self._trace_id:
            self._trace_id = uuid.uuid4().hex
        self._pipeline_span_id = uuid.uuid4().hex
        self._pipeline_start_time = time.time()
        try:
            self._client.set_trace_context(self._trace_id, span_id=self._pipeline_span_id)
        except Exception:
            logger.debug("Failed to set trace context on API client", exc_info=True)
        self._event_logger.set_trace_context(self._trace_id, span_id=self._pipeline_span_id)

        self._log_session_event(
            "pipeline_started",
            objective="resume_session",
            working_dir=str(self._working_dir),
            resumed_session_id=session_id,
            span_id=self._pipeline_span_id,
        )
        self._log_resource_snapshot("pipeline_start")

        # Get session state (supports short IDs - ISSUE-SAAS-044 fix)
        try:
            response = self._client.get_session(session_id)
            resume_context = ResumeContext.from_dict(response)
        except APIError as e:
            if e.status_code == 404:
                raise OrchestratorError(
                    f"Session not found: {session_id}",
                    recovery="The session may have expired. Start a new session with 'obra derive'",
                )
            raise

        if not resume_context.can_resume:
            # Build detailed error message with status, reason, and recovery guidance
            status = response.get("status", "unknown")
            escalation_reason = response.get("escalation_reason")

            # Get progress info from plan if available
            progress_info = ""
            try:
                plan_data = self._client.get_session_plan(session_id)
                completed = plan_data.get("completed_count", 0)
                total = plan_data.get("total_count", 0)
                if total > 0:
                    progress_info = f"\nProgress: {completed}/{total} tasks completed"
            except Exception:
                pass  # Progress info is optional

            # Build error message parts
            error_parts = [f"Session cannot be resumed (status: {status})"]
            if escalation_reason:
                error_parts.append(f"Reason: {escalation_reason}")
            if progress_info:
                error_parts[0] += progress_info

            error_message = "\n".join(error_parts)

            # Build recovery suggestion
            short_id = session_id[:8] if len(session_id) > 8 else session_id
            recovery = (
                f"To continue from the last checkpoint:\n"
                f"  obra run --continue-from {short_id}\n"
                f"To start fresh:\n"
                f'  obra run "<objective>"'
            )

            raise OrchestratorError(
                error_message,
                session_id=session_id,
                recovery=recovery,
            )

        # Use full session ID from response (in case short ID was provided)
        full_session_id = response.get("session_id", session_id)
        self._session_id = full_session_id
        print_info(f"Resuming session: {full_session_id[:8]}...")
        print_info(f"  Last step: {resume_context.last_successful_step}")

        # Request resume from server
        try:
            response = self._request_with_observability(
                "POST",
                "resume",
                json={"session_id": full_session_id},
            )
        except APIError as e:
            raise OrchestratorError(
                f"Failed to resume session: {e}",
                session_id=session_id,
            )

        server_action = ServerAction.from_dict(response)

        # Continue orchestration loop from resume point
        iteration = 0
        poll_count = 0  # Track consecutive WAIT responses for backoff
        max_iterations = get_max_iterations()
        try:
            while iteration < max_iterations:
                iteration += 1

                result = self._handle_action(server_action)

                if result.get("completed"):
                    notice = result.get("notice")
                    if isinstance(notice, CompletionNotice):
                        self._log_session_event(
                            "session_completed",
                            items_completed=notice.items_completed,
                            total_iterations=notice.total_iterations,
                            quality_score=notice.quality_score,
                        )
                        self._log_pipeline_completed()
                        return notice
                    self._log_session_event(
                        "session_completed",
                        items_completed=result.get("items_completed", 0),
                        total_iterations=result.get("total_iterations", iteration),
                        quality_score=result.get("quality_score", 0.0),
                    )
                    self._log_pipeline_completed()
                    return CompletionNotice(
                        session_summary=result.get("session_summary", ""),
                        items_completed=result.get("items_completed", 0),
                        total_iterations=result.get("total_iterations", iteration),
                        quality_score=result.get("quality_score", 0.0),
                    )

                if result.get("waiting"):
                    self._poll_with_backoff(poll_count)
                    poll_count += 1
                    # Poll server for updated action
                    # ISSUE-009 Bug #3: Use query param format (not path param)
                    # Cloud Functions routing: get_session_action?session_id={id}
                    try:
                        response = self._request_with_observability(
                            "GET",
                            f"get_session_action?session_id={self._session_id}",
                        )
                        server_action = ServerAction.from_dict(response)
                        # Reset failure count on successful poll
                        self._polling_failure_count = 0
                    except APIError as e:
                        # Increment failure counter
                        self._polling_failure_count += 1

                        # ISSUE-CLI-012: Fast-fail on non-retryable errors (404, 401, 403)
                        if hasattr(e, "status_code") and e.status_code in (404, 401, 403):
                            logger.error(
                                f"Resume polling endpoint returned non-retryable error {e.status_code}. "
                                f"Session: {self._session_id}, Error: {e}"
                            )
                            raise OrchestratorError(
                                f"Resume polling endpoint failed with non-retryable error (HTTP {e.status_code}). "
                                f"Original error: {e}",
                                session_id=self._session_id,
                                recovery=f"Check server logs. Resume with: obra resume --session-id {self._session_id}",
                            )

                        # ISSUE-CLI-012: Circuit breaker - exit after max retries
                        if self._polling_failure_count >= MAX_POLLING_RETRIES:
                            logger.error(
                                f"Resume polling circuit breaker triggered after {MAX_POLLING_RETRIES} failures. "
                                f"Session: {self._session_id}, Last error: {e}"
                            )
                            raise OrchestratorError(
                                f"Resume polling failed after {MAX_POLLING_RETRIES} attempts. "
                                f"Last error: {e}",
                                session_id=self._session_id,
                                recovery=f"Check server status. Resume with: obra resume --session-id {self._session_id}",
                            )

                        # If polling endpoint not available, continue with current action
                        logger.warning(
                            f"Resume polling attempt {self._polling_failure_count} failed: {e}"
                        )
                    continue
                # Reset poll count when not waiting
                poll_count = 0

                server_action = self._report_result(server_action.action, result)

                if server_action.is_error():
                    raise OrchestratorError(
                        server_action.error_message or "Server returned error",
                        session_id=self._session_id,
                    )

            raise OrchestratorError(
                f"Orchestration loop exceeded {max_iterations} iterations",
                session_id=self._session_id,
            )
        except Exception as e:
            error_message = str(e)
            error_class = type(e).__name__
            self._log_session_event(
                "pipeline_failed",
                failure_stage=self._current_phase.value if self._current_phase else "unknown",
                error_code="ORCHESTRATOR_ERROR",
                error_class=error_class,
                error_message=error_message,
                span_id=self._pipeline_span_id,
            )
            if self._current_phase:
                self._log_session_event(
                    "phase_failed",
                    phase=self._current_phase.value,
                    failure_stage="resume_loop",
                    error_code="ORCHESTRATOR_ERROR",
                    error_class=error_class,
                    error_message=error_message,
                    span_id=self._phase_span_id,
                    parent_span_id=self._pipeline_span_id,
                )
            # ISSUE-OBS-003: Emit session_failed to properly close session lifecycle
            self._log_session_event(
                "session_failed",
                error_code="ORCHESTRATOR_ERROR",
                error_class=error_class,
                error_message=error_message,
                phase=self._current_phase.value if self._current_phase else "unknown",
            )
            raise

    def get_status(self, session_id: str | None = None) -> ResumeContext:
        """Get session status.

        Args:
            session_id: Session ID to check (defaults to current session)

        Returns:
            ResumeContext with session status

        Raises:
            OrchestratorError: If no session ID provided and no active session
        """
        sid = session_id or self._session_id
        if not sid:
            raise OrchestratorError(
                "No session ID provided",
                recovery="Provide a session ID or start a new session with 'obra derive'",
            )

        try:
            response = self._request_with_observability("GET", f"session/{sid}")
            return ResumeContext.from_dict(response)
        except APIError as e:
            if e.status_code == 404:
                raise OrchestratorError(
                    f"Session not found: {sid}",
                    recovery="The session may have expired.",
                )
            raise


__all__ = [
    "ConnectionError",
    "HybridOrchestrator",
    "OrchestratorError",
]
