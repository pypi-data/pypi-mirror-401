"""Automatic session console output capture for feedback reports.

This module provides automatic capture of all CLI output to session-specific
log files, enabling zero-friction inclusion of console output in bug reports.

Design:
- Captures stdout/stderr to session-specific log files
- Strips Rich formatting for plain text storage
- Auto-prunes old session logs (keeps last 10)
- Thread-safe for concurrent output
- Works with Rich Console streaming output

Usage:
    with SessionConsoleLogger(session_id="abc-123") as logger:
        # All print/console output is captured
        console.print("Hello world")
        print("Also captured")

    # Or as a singleton for the CLI entry point:
    logger = get_session_logger()
    logger.start("session-123")
    # ... CLI execution ...
    logger.stop()
"""

import io
import logging
import os
import sys
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock
from typing import Any, TextIO

logger = logging.getLogger(__name__)


class SessionConsoleLogger:
    """Captures console output to a session-specific log file.

    This class intercepts stdout/stderr and writes a copy to a log file
    while still displaying output to the terminal.

    Features:
    - Tee-style capture (output goes to both terminal and file)
    - Thread-safe writing
    - Auto-creates log directory
    - Auto-prunes old session logs
    - Strips ANSI escape codes for clean log files
    """

    # Maximum sessions to keep
    MAX_SESSIONS = 10

    # Log directory
    LOG_DIR = Path(os.environ.get("OBRA_RUNTIME_DIR", "~/obra-runtime")).expanduser() / "logs" / "sessions"

    def __init__(self, session_id: str | None = None):
        """Initialize session console logger.

        Args:
            session_id: Session ID for log file naming. If None, uses timestamp.
        """
        self.session_id = session_id or datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
        self._log_path = self.LOG_DIR / f"{self.session_id}.log"
        self._lock = Lock()
        self._file: TextIO | None = None
        self._original_stdout: TextIO | None = None
        self._original_stderr: TextIO | None = None
        self._started = False

    @property
    def log_path(self) -> Path:
        """Get the path to the session log file."""
        return self._log_path

    def start(self) -> "SessionConsoleLogger":
        """Start capturing console output.

        Returns:
            Self for chaining
        """
        if self._started:
            return self

        try:
            # Create log directory
            self.LOG_DIR.mkdir(parents=True, exist_ok=True)

            # Open log file
            self._file = open(self._log_path, "w", encoding="utf-8")

            # Write header
            self._file.write(f"# Session Console Log: {self.session_id}\n")
            self._file.write(f"# Started: {datetime.now(UTC).isoformat()}\n")
            self._file.write("# This log is auto-generated for debugging purposes\n")
            self._file.write("-" * 60 + "\n\n")
            self._file.flush()

            # Install tee writers
            self._original_stdout = sys.stdout
            self._original_stderr = sys.stderr
            sys.stdout = _TeeWriter(self._original_stdout, self._file, self._lock)
            sys.stderr = _TeeWriter(self._original_stderr, self._file, self._lock, prefix="[stderr] ")

            self._started = True

            # Prune old sessions
            self._prune_old_sessions()

            logger.debug(f"Session console logging started: {self._log_path}")

        except Exception as e:
            logger.warning(f"Failed to start session console logging: {e}")
            # Don't fail the CLI if logging fails
            self._cleanup()

        return self

    def stop(self) -> None:
        """Stop capturing console output."""
        if not self._started:
            return

        try:
            # Restore original streams
            if self._original_stdout:
                sys.stdout = self._original_stdout
            if self._original_stderr:
                sys.stderr = self._original_stderr

            # Write footer and close
            if self._file:
                self._file.write("\n" + "-" * 60 + "\n")
                self._file.write(f"# Ended: {datetime.now(UTC).isoformat()}\n")
                self._file.close()

            logger.debug(f"Session console logging stopped: {self._log_path}")

        except Exception as e:
            logger.warning(f"Error stopping session console logging: {e}")
        finally:
            self._cleanup()

    def _cleanup(self) -> None:
        """Clean up resources."""
        self._file = None
        self._original_stdout = None
        self._original_stderr = None
        self._started = False

    def _prune_old_sessions(self) -> None:
        """Remove old session logs, keeping only the most recent."""
        try:
            log_files = sorted(
                self.LOG_DIR.glob("*.log"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )

            # Remove files beyond the limit
            for old_file in log_files[self.MAX_SESSIONS:]:
                try:
                    old_file.unlink()
                    logger.debug(f"Pruned old session log: {old_file}")
                except Exception as e:
                    logger.warning(f"Failed to prune {old_file}: {e}")

        except Exception as e:
            logger.warning(f"Failed to prune old session logs: {e}")

    def __enter__(self) -> "SessionConsoleLogger":
        """Context manager entry."""
        return self.start()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit."""
        self.stop()

    @classmethod
    def get_session_log(cls, session_id: str) -> str | None:
        """Read the contents of a session log file.

        Args:
            session_id: Session ID to read

        Returns:
            Log contents as string, or None if not found
        """
        log_path = cls.LOG_DIR / f"{session_id}.log"
        if not log_path.exists():
            return None

        try:
            return log_path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            logger.warning(f"Failed to read session log {session_id}: {e}")
            return None

    @classmethod
    def get_recent_session_log(cls) -> tuple[str | None, str | None]:
        """Get the most recent session log.

        Returns:
            Tuple of (session_id, log_contents) or (None, None) if no logs exist
        """
        try:
            log_files = sorted(
                cls.LOG_DIR.glob("*.log"),
                key=lambda p: p.stat().st_mtime,
                reverse=True,
            )

            if not log_files:
                return None, None

            most_recent = log_files[0]
            session_id = most_recent.stem
            content = most_recent.read_text(encoding="utf-8", errors="replace")
            return session_id, content

        except Exception as e:
            logger.warning(f"Failed to get recent session log: {e}")
            return None, None

    @classmethod
    def list_sessions(cls) -> list[dict[str, Any]]:
        """List all available session logs.

        Returns:
            List of session info dictionaries
        """
        sessions = []
        try:
            for log_file in cls.LOG_DIR.glob("*.log"):
                stat = log_file.stat()
                sessions.append({
                    "session_id": log_file.stem,
                    "path": str(log_file),
                    "size_bytes": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime, UTC).isoformat(),
                })

            return sorted(sessions, key=lambda x: x["modified"], reverse=True)

        except Exception as e:
            logger.warning(f"Failed to list session logs: {e}")
            return []


class _TeeWriter(io.TextIOBase):
    """A writer that outputs to both a terminal and a file.

    Strips ANSI escape codes when writing to the file for clean logs.
    """

    # ANSI escape code pattern
    import re
    ANSI_PATTERN = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]|\x1b\].*?\x07")

    def __init__(
        self,
        terminal: TextIO,
        file: TextIO,
        lock: Lock,
        prefix: str = "",
    ):
        """Initialize tee writer.

        Args:
            terminal: Original terminal stream
            file: File to also write to
            lock: Lock for thread-safe writing
            prefix: Optional prefix for file output (e.g., "[stderr] ")
        """
        self._terminal = terminal
        self._file = file
        self._lock = lock
        self._prefix = prefix

    def write(self, data: str) -> int:
        """Write to both terminal and file."""
        if not data:
            return 0

        # Always write to terminal with original formatting
        try:
            self._terminal.write(data)
        except Exception:
            pass

        # Write cleaned version to file
        try:
            with self._lock:
                # Strip ANSI codes for clean log
                clean_data = self.ANSI_PATTERN.sub("", data)
                if clean_data:
                    if self._prefix and clean_data.strip():
                        # Add prefix only to non-empty lines
                        lines = clean_data.split("\n")
                        prefixed = "\n".join(
                            f"{self._prefix}{line}" if line.strip() else line
                            for line in lines
                        )
                        self._file.write(prefixed)
                    else:
                        self._file.write(clean_data)
                    self._file.flush()
        except Exception:
            pass

        return len(data)

    def flush(self) -> None:
        """Flush both streams."""
        try:
            self._terminal.flush()
        except Exception:
            pass
        try:
            self._file.flush()
        except Exception:
            pass

    def fileno(self) -> int:
        """Return terminal's file descriptor for compatibility."""
        return self._terminal.fileno()

    @property
    def encoding(self) -> str:
        """Return terminal's encoding."""
        return getattr(self._terminal, "encoding", "utf-8")

    def isatty(self) -> bool:
        """Return whether terminal is a TTY."""
        return self._terminal.isatty()


# Module-level singleton
_session_logger: SessionConsoleLogger | None = None


def get_session_logger() -> SessionConsoleLogger | None:
    """Get the current session logger singleton.

    Returns:
        SessionConsoleLogger instance or None if not started
    """
    return _session_logger


def start_session_logging(session_id: str) -> SessionConsoleLogger:
    """Start session console logging (singleton).

    Args:
        session_id: Session ID for log file naming

    Returns:
        SessionConsoleLogger instance
    """
    global _session_logger
    if _session_logger is not None:
        _session_logger.stop()

    _session_logger = SessionConsoleLogger(session_id)
    _session_logger.start()
    return _session_logger


def stop_session_logging() -> None:
    """Stop session console logging."""
    global _session_logger
    if _session_logger is not None:
        _session_logger.stop()
        _session_logger = None


@contextmanager
def session_logging(session_id: str):
    """Context manager for session console logging.

    Args:
        session_id: Session ID for log file naming

    Yields:
        SessionConsoleLogger instance
    """
    logger = start_session_logging(session_id)
    try:
        yield logger
    finally:
        stop_session_logging()


__all__ = [
    "SessionConsoleLogger",
    "get_session_logger",
    "session_logging",
    "start_session_logging",
    "stop_session_logging",
]
