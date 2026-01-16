"""Observability data collection for feedback reports.

This module collects and sanitizes event logs from:
1. Local hybrid.jsonl event log (~/.obra-runtime/logs/hybrid.jsonl)
2. Server-side session events (via API client)
3. Session console logs (~/.obra-runtime/logs/sessions/{session_id}.log)

Privacy levels control how much observability data is included:
- MINIMAL: No data (too identifying)
- STANDARD: 50 events + 100 console lines, sanitized
- FULL: 200 events + 500 console lines + server events
"""

import json
import logging
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from obra.feedback.models import PrivacyLevel

logger = logging.getLogger(__name__)


class ObservabilityCollector:
    """Collects observability data for feedback reports.

    Gathers events from local hybrid.jsonl, session console logs, and
    optionally server-side session events, respecting privacy level settings.

    Example:
        collector = ObservabilityCollector(
            privacy_level=PrivacyLevel.STANDARD,
            session_id="abc-123"
        )
        events = collector.get_sanitized_events()
        console_log = collector.get_session_console_log()
    """

    # Event limits per privacy level
    LOCAL_EVENT_LIMITS = {
        PrivacyLevel.MINIMAL: 0,
        PrivacyLevel.STANDARD: 50,
        PrivacyLevel.FULL: 200,
    }

    SERVER_EVENT_LIMITS = {
        PrivacyLevel.MINIMAL: 0,
        PrivacyLevel.STANDARD: 0,  # Standard doesn't fetch server events
        PrivacyLevel.FULL: 100,
    }

    # Console log line limits per privacy level
    CONSOLE_LOG_LIMITS = {
        PrivacyLevel.MINIMAL: 0,
        PrivacyLevel.STANDARD: 100,
        PrivacyLevel.FULL: 500,
    }

    # Session logs directory
    SESSION_LOG_DIR = Path(os.environ.get("OBRA_RUNTIME_DIR", "~/obra-runtime")).expanduser() / "logs" / "sessions"

    # Fields to always redact (contain sensitive data)
    REDACT_FIELDS = {
        "prompt", "system_prompt", "user_prompt", "api_key", "token",
        "password", "secret", "credential", "authorization",
    }

    # Fields safe to include at all levels
    SAFE_FIELDS = {
        "type", "ts", "timestamp", "session", "session_id",
        "phase", "component", "event_type", "status",
        "iteration", "item_id", "work_unit_id",
    }

    # Additional fields for STANDARD level
    STANDARD_FIELDS = SAFE_FIELDS | {
        "error", "error_type", "error_message", "duration_ms",
        "item_count", "trace_id", "span_id",
    }

    # Additional fields for FULL level (most fields except explicitly redacted)
    FULL_FIELDS = STANDARD_FIELDS | {
        "result", "details", "context", "metadata", "config",
        "objective", "task_type", "severity",
    }

    def __init__(
        self,
        privacy_level: PrivacyLevel = PrivacyLevel.STANDARD,
        session_id: str | None = None,
        max_age_hours: int = 24,
    ):
        """Initialize observability collector.

        Args:
            privacy_level: Privacy level for data collection
            session_id: Session ID to filter events (optional)
            max_age_hours: Maximum age of events to include (default 24h)
        """
        self.privacy_level = privacy_level
        self.session_id = session_id
        self.max_age = timedelta(hours=max_age_hours)
        self._log_path = self._get_log_path()

    @staticmethod
    def _get_log_path() -> Path:
        """Get path to hybrid.jsonl log file."""
        runtime_dir = Path(os.environ.get("OBRA_RUNTIME_DIR", "~/obra-runtime")).expanduser()
        return runtime_dir / "logs" / "hybrid.jsonl"

    def collect_local_events(self) -> list[dict[str, Any]]:
        """Collect events from local hybrid.jsonl file.

        Returns:
            List of event dictionaries, filtered and limited by privacy level
        """
        limit = self.LOCAL_EVENT_LIMITS[self.privacy_level]
        if limit == 0:
            return []

        if not self._log_path.exists():
            logger.debug(f"No local event log found at {self._log_path}")
            return []

        events = []
        cutoff_time = datetime.now(UTC) - self.max_age

        try:
            with open(self._log_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    # Filter by session_id if provided
                    if self.session_id:
                        event_session = event.get("session") or event.get("session_id")
                        if event_session != self.session_id:
                            continue

                    # Filter by age
                    ts = event.get("ts") or event.get("timestamp")
                    if ts:
                        try:
                            event_time = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                            if event_time < cutoff_time:
                                continue
                        except (ValueError, TypeError):
                            pass

                    events.append(event)

        except Exception as e:
            logger.warning(f"Failed to read local events: {e}")
            return []

        # Return most recent events up to limit
        return events[-limit:] if len(events) > limit else events

    def collect_server_events(self) -> list[dict[str, Any]]:
        """Collect events from server via API client.

        Returns:
            List of server event dictionaries
        """
        limit = self.SERVER_EVENT_LIMITS[self.privacy_level]
        if limit == 0 or not self.session_id:
            return []

        try:
            from obra.api import APIClient

            client = APIClient.from_config()
            response = client.get_session_events(
                session_id=self.session_id,
                limit=limit,
            )

            return response.get("events", [])

        except Exception as e:
            logger.warning(f"Failed to fetch server events: {e}")
            return []

    def sanitize_event(self, event: dict[str, Any]) -> dict[str, Any]:
        """Sanitize a single event based on privacy level.

        Args:
            event: Raw event dictionary

        Returns:
            Sanitized event dictionary
        """
        if self.privacy_level == PrivacyLevel.MINIMAL:
            return {}

        # Determine allowed fields based on privacy level
        if self.privacy_level == PrivacyLevel.FULL:
            allowed_fields = self.FULL_FIELDS
        else:
            allowed_fields = self.STANDARD_FIELDS

        sanitized = {}
        for key, value in event.items():
            # Always skip redacted fields
            if key.lower() in self.REDACT_FIELDS:
                continue

            # Check if field is allowed at this privacy level
            if key in allowed_fields:
                sanitized[key] = self._sanitize_value(value)
            elif self.privacy_level == PrivacyLevel.FULL:
                # At FULL level, include unknown fields but sanitize values
                sanitized[key] = self._sanitize_value(value)

        return sanitized

    def _sanitize_value(self, value: Any) -> Any:
        """Recursively sanitize a value.

        Args:
            value: Value to sanitize

        Returns:
            Sanitized value
        """
        if isinstance(value, dict):
            return {
                k: self._sanitize_value(v)
                for k, v in value.items()
                if k.lower() not in self.REDACT_FIELDS
            }
        if isinstance(value, list):
            return [self._sanitize_value(item) for item in value]
        if isinstance(value, str):
            # Truncate very long strings
            if len(value) > 1000 and self.privacy_level != PrivacyLevel.FULL:
                return value[:500] + f"... [{len(value) - 500} chars truncated]"
            return value
        return value

    def get_sanitized_events(self) -> list[dict[str, Any]]:
        """Get all events, sanitized according to privacy level.

        Combines local and server events, applies sanitization,
        and returns the result.

        Returns:
            List of sanitized event dictionaries
        """
        if self.privacy_level == PrivacyLevel.MINIMAL:
            return []

        # Collect from both sources
        local_events = self.collect_local_events()
        server_events = self.collect_server_events()

        # Combine (local first, then server)
        all_events = local_events + server_events

        # Sanitize each event
        sanitized = [self.sanitize_event(event) for event in all_events]

        # Filter out empty events
        return [e for e in sanitized if e]

    def get_session_console_log(self) -> str:
        """Get the session console log content.

        Returns:
            Sanitized console log content (last N lines based on privacy level)
        """
        limit = self.CONSOLE_LOG_LIMITS[self.privacy_level]
        if limit == 0:
            return ""

        # Try session-specific log first
        if self.session_id:
            log_path = self.SESSION_LOG_DIR / f"{self.session_id}.log"
            if log_path.exists():
                return self._read_and_sanitize_log(log_path, limit)

        # Fall back to most recent session log
        try:
            log_files = sorted(
                self.SESSION_LOG_DIR.glob("*.log"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )
            if log_files:
                return self._read_and_sanitize_log(log_files[0], limit)
        except Exception as e:
            logger.warning(f"Failed to find session console log: {e}")

        return ""

    def _read_and_sanitize_log(self, log_path: Path, max_lines: int) -> str:
        """Read and sanitize a log file.

        Args:
            log_path: Path to log file
            max_lines: Maximum number of lines to include

        Returns:
            Sanitized log content
        """
        try:
            content = log_path.read_text(encoding="utf-8", errors="replace")
            lines = content.split("\n")

            # Get last N lines
            if len(lines) > max_lines:
                lines = [f"[... {len(lines) - max_lines} lines truncated ...]"] + lines[-max_lines:]

            content = "\n".join(lines)

            # Apply sanitization based on privacy level
            if self.privacy_level != PrivacyLevel.FULL:
                # Import sanitizer to reuse sanitization logic
                from obra.feedback.sanitizer import DataSanitizer
                sanitizer = DataSanitizer(self.privacy_level)
                content = sanitizer.sanitize_log_content(content, max_lines=max_lines)

            return content

        except Exception as e:
            logger.warning(f"Failed to read log file {log_path}: {e}")
            return ""

    def get_all_observability_data(self) -> dict[str, Any]:
        """Get all observability data in a single call.

        Returns:
            Dictionary with events, console_log, and summary
        """
        return {
            "events": self.get_sanitized_events(),
            "console_log": self.get_session_console_log(),
            "summary": self.get_summary(),
        }

    def get_summary(self) -> dict[str, Any]:
        """Get a summary of available observability data.

        Returns:
            Dictionary with event counts and availability info
        """
        session_log_path = None
        session_log_exists = False

        if self.session_id:
            session_log_path = self.SESSION_LOG_DIR / f"{self.session_id}.log"
            session_log_exists = session_log_path.exists()

        return {
            "log_path": str(self._log_path),
            "log_exists": self._log_path.exists(),
            "session_log_path": str(session_log_path) if session_log_path else None,
            "session_log_exists": session_log_exists,
            "session_id": self.session_id,
            "privacy_level": self.privacy_level.value,
            "local_event_limit": self.LOCAL_EVENT_LIMITS[self.privacy_level],
            "server_event_limit": self.SERVER_EVENT_LIMITS[self.privacy_level],
            "console_log_limit": self.CONSOLE_LOG_LIMITS[self.privacy_level],
            "max_age_hours": self.max_age.total_seconds() / 3600,
        }


__all__ = ["ObservabilityCollector"]
