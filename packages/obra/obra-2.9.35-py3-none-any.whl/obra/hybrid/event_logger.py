"""Minimal event logger for hybrid mode observability (ISSUE-SAAS-042).

This module provides a standalone event logger that works in both:
- Development environment (running from source)
- Installed package (pip install obra)

The logger writes JSONL events to ~/obra-runtime/logs/hybrid.jsonl.

Why this exists:
- ProductionLogger (src/monitoring/production_logger.py) is not packaged
- Sessions run from installed package had no event logging (silent failure)
- This minimal implementation provides observability for all obra users

Design principles:
- No dependencies on src/ modules (must work in installed package)
- Thread-safe for concurrent event logging
- Simple JSONL format compatible with ProductionLogger events
- Immediate flush for real-time monitoring
- ISSUE-OBS-003: Log rotation at 10MB with 5 backup files
"""

import json
import logging
import os
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any

# Log rotation settings
MAX_LOG_SIZE_BYTES = 10 * 1024 * 1024  # 10MB
MAX_BACKUP_COUNT = 5  # Keep 5 rotated files

logger = logging.getLogger(__name__)


class HybridEventLogger:
    """Minimal JSONL event logger for hybrid mode.

    Thread-safe event logger that writes structured events to a JSONL file.
    Compatible with ProductionLogger event format for tooling compatibility.

    Example:
        >>> logger = HybridEventLogger()
        >>> logger.log_event("session_started", session_id="abc-123", objective="test")
    """

    def __init__(self, log_path: Path | None = None):
        """Initialize HybridEventLogger.

        Args:
            log_path: Path to log file. Defaults to ~/obra-runtime/logs/hybrid.jsonl
        """
        self._lock = Lock()
        self._log_path = log_path or self._get_default_log_path()
        self._trace_id: str | None = None
        self._span_id: str | None = None
        self._parent_span_id: str | None = None
        self._component: str | None = "hybrid_client"
        self._work_unit_id: str | None = None

        # Ensure log directory exists
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.debug(f"HybridEventLogger initialized: {self._log_path}")

    def set_trace_context(
        self,
        trace_id: str,
        span_id: str | None = None,
        parent_span_id: str | None = None,
    ) -> None:
        """Set trace context for subsequent log events."""
        self._trace_id = trace_id
        if span_id:
            self._span_id = span_id
        if parent_span_id:
            self._parent_span_id = parent_span_id

    def set_component(self, component: str) -> None:
        """Set component label for subsequent log events."""
        self._component = component

    def set_work_unit(self, work_unit_id: str | None) -> None:
        """Set work unit ID for subsequent log events."""
        self._work_unit_id = work_unit_id

    @staticmethod
    def _get_default_log_path() -> Path:
        """Get the default log file path.

        Returns:
            Path to ~/obra-runtime/logs/hybrid.jsonl
        """
        runtime_dir = Path(os.environ.get("OBRA_RUNTIME_DIR", "~/obra-runtime")).expanduser()
        return runtime_dir / "logs" / "hybrid.jsonl"

    def _rotate_if_needed(self) -> None:
        """Rotate log file if it exceeds MAX_LOG_SIZE_BYTES.

        ISSUE-OBS-003: Implements simple log rotation to prevent unbounded growth.
        Rotates to .1, .2, etc. and keeps MAX_BACKUP_COUNT backups.
        """
        try:
            if not self._log_path.exists():
                return

            current_size = self._log_path.stat().st_size
            if current_size < MAX_LOG_SIZE_BYTES:
                return

            # Rotate existing backups (.5 -> deleted, .4 -> .5, etc.)
            for i in range(MAX_BACKUP_COUNT, 0, -1):
                old_path = self._log_path.with_suffix(f".jsonl.{i}")
                if i == MAX_BACKUP_COUNT:
                    # Delete oldest backup
                    if old_path.exists():
                        old_path.unlink()
                else:
                    # Rename to next number
                    new_path = self._log_path.with_suffix(f".jsonl.{i + 1}")
                    if old_path.exists():
                        old_path.rename(new_path)

            # Rotate current file to .1
            backup_path = self._log_path.with_suffix(".jsonl.1")
            self._log_path.rename(backup_path)

            logger.info(f"Rotated log file: {self._log_path} -> {backup_path}")

        except Exception as e:
            # Never fail logging due to rotation errors
            logger.warning(f"Log rotation failed: {e}")

    def log_event(self, event_type: str, session_id: str = "", **kwargs: Any) -> None:
        """Log a structured event to the JSONL file.

        Args:
            event_type: Type of event (session_started, phase_started, etc.)
            session_id: Session ID for event correlation
            **kwargs: Event-specific data

        Example:
            >>> logger.log_event(
            ...     "derivation_started",
            ...     session_id="abc-123",
            ...     objective="Build calculator app"
            ... )
        """
        with self._lock:
            try:
                # ISSUE-OBS-003: Check for log rotation before writing
                self._rotate_if_needed()

                now_iso = datetime.now(UTC).isoformat()
                event = {
                    "type": event_type,
                    "ts": now_iso,
                    "timestamp": now_iso,
                    "session": session_id,
                    **kwargs,
                }

                if "trace_id" not in event and self._trace_id:
                    event["trace_id"] = self._trace_id
                if "span_id" not in event and self._span_id:
                    event["span_id"] = self._span_id
                if "parent_span_id" not in event and self._parent_span_id:
                    event["parent_span_id"] = self._parent_span_id
                if "component" not in event and self._component:
                    event["component"] = self._component
                if "work_unit_id" not in event and self._work_unit_id:
                    event["work_unit_id"] = self._work_unit_id

                # Append JSONL line to file
                with open(self._log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(event, default=str) + "\n")
                    f.flush()  # Immediate flush for real-time monitoring

            except Exception as e:
                # Never fail the main operation due to logging
                logger.warning(f"Failed to log event '{event_type}': {e}")


# Module-level singleton for convenience
_hybrid_logger: HybridEventLogger | None = None


def get_hybrid_logger() -> HybridEventLogger:
    """Get or create the module-level HybridEventLogger instance.

    Returns:
        HybridEventLogger singleton instance
    """
    global _hybrid_logger
    if _hybrid_logger is None:
        _hybrid_logger = HybridEventLogger()
    return _hybrid_logger


__all__ = ["HybridEventLogger", "get_hybrid_logger"]
