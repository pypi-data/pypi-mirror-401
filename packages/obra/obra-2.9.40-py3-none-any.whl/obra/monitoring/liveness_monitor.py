"""Liveness monitoring for task execution hang detection.

This module provides the LivenessMonitor class which monitors multiple indicators
of task liveness to distinguish between legitimate slow progress and true hangs.

Part of FEAT-TIMEOUT-LIVENESS-001: Intelligent Timeout with Liveness Detection.
"""

import logging
import time
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class LivenessStatus(Enum):
    """Liveness detection status.

    Attributes:
        HUNG: 0 indicators active - task is truly hung
        INVESTIGATE: 1 indicator active - ambiguous, needs investigation
        ALIVE: 2+ indicators active - task showing clear progress
    """

    HUNG = "HUNG"
    INVESTIGATE = "INVESTIGATE"
    ALIVE = "ALIVE"


class LivenessMonitor:
    """Monitor task execution liveness through multiple indicators.

    Monitors 5 independent indicators to detect task progress:
    1. Log activity - new entries in log files
    2. CPU activity - CPU time delta
    3. File changes - workspace file modifications
    4. Database updates - StateManager timestamp changes
    5. Process state - process health via psutil

    Decision logic:
    - 0 active indicators → HUNG (immediate kill)
    - 1 active indicator → INVESTIGATE (run hang investigation)
    - 2+ active indicators → ALIVE (extend timeout)

    Example:
        >>> monitor = LivenessMonitor(
        ...     task_id=123,
        ...     config=config,
        ...     workspace_path=Path("./workspace"),
        ...     log_path=Path("./logs/production.jsonl")
        ... )
        >>> monitor.capture_baseline()
        >>> time.sleep(180)  # Wait 3 minutes
        >>> status = monitor.check_liveness()
        >>> if status == LivenessStatus.HUNG:
        ...     kill_task()

    Attributes:
        task_id: Task ID being monitored
        config: Configuration dict with liveness thresholds
        workspace_path: Path to task workspace directory
        log_path: Path to log file (production.jsonl)
        baseline_cpu: Baseline CPU time for delta calculation
        baseline_timestamp: Timestamp of baseline capture
        baseline_file_mtimes: Workspace file modification times at baseline
    """

    def __init__(
        self,
        task_id: int,
        config: dict[str, Any],
        workspace_path: Path,
        production_logger: Any,
        log_path: Path | None = None,
        state_manager: Any | None = None,
        process_pid: int | None = None,
    ):
        """Initialize liveness monitor.

        Args:
            task_id: Task ID to monitor
            config: Configuration dict containing orchestration.timeout settings
            workspace_path: Path to task workspace directory
            production_logger: ProductionLogger instance for event logging
            log_path: Optional path to log file (default: ~/obra-runtime/logs/production.jsonl)
            state_manager: Optional StateManager instance for DB activity checks
            process_pid: Optional process PID to monitor
        """
        self.task_id = task_id
        self.config = config
        self.workspace_path = workspace_path
        self.production_logger = production_logger
        self.log_path = log_path
        self.state_manager = state_manager
        self.process_pid = process_pid

        # Extract thresholds from config (with defaults)
        timeout_config = config.get("orchestration", {}).get("timeout", {})
        self.cpu_delta_threshold = timeout_config.get("cpu_delta_threshold", 1.0)
        self.log_silence_threshold = timeout_config.get("log_silence_threshold", 300)
        self.file_mtime_window = timeout_config.get("file_mtime_window", 300)
        self.db_update_window = timeout_config.get("db_update_window", 300)
        self.min_alive_indicators = timeout_config.get("min_alive_indicators", 2)

        # Baseline data (captured before monitoring)
        self.baseline_cpu: float = 0.0
        self.baseline_timestamp: float = 0.0
        self.baseline_file_mtimes: dict[str, float] = {}
        self.baseline_db_timestamp: float | None = None

        # psutil availability flag
        self._psutil_available = False
        try:
            import psutil

            self._psutil_available = True
            logger.debug("psutil available for process monitoring")
        except ImportError:
            logger.warning(
                "psutil not available - process state indicator disabled. "
                "Install psutil for full liveness detection: pip install psutil"
            )

        logger.info(
            f"LivenessMonitor initialized: task_id={task_id}, "
            f"thresholds=(cpu={self.cpu_delta_threshold}s, "
            f"log={self.log_silence_threshold}s, "
            f"file={self.file_mtime_window}s, db={self.db_update_window}s), "
            f"min_alive={self.min_alive_indicators}"
        )

    def capture_baseline(self) -> None:
        """Capture baseline measurements for delta calculations.

        Must be called before check_liveness() to establish baseline.
        Captures:
        - Current CPU time
        - Current timestamp
        - Workspace file modification times
        - Database last_updated timestamp (if StateManager available)

        Example:
            >>> monitor.capture_baseline()
            >>> # ... task executes for some time ...
            >>> status = monitor.check_liveness()
        """
        self.baseline_timestamp = time.time()

        # Capture CPU baseline if psutil available and PID provided
        if self._psutil_available and self.process_pid:
            try:
                import psutil

                process = psutil.Process(self.process_pid)
                cpu_times = process.cpu_times()
                self.baseline_cpu = cpu_times.user + cpu_times.system
                logger.debug(f"Baseline CPU captured: {self.baseline_cpu}s")
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                logger.warning(f"Failed to capture CPU baseline: {e}")
                self.baseline_cpu = 0.0

        # Capture file mtimes baseline
        if self.workspace_path.exists():
            for file_path in self.workspace_path.rglob("*"):
                if file_path.is_file() and not self._should_ignore_file(file_path):
                    try:
                        self.baseline_file_mtimes[str(file_path)] = file_path.stat().st_mtime
                    except OSError:
                        pass  # File may have been deleted
            logger.debug(f"Baseline files captured: {len(self.baseline_file_mtimes)} files")

        # Capture DB timestamp baseline if StateManager available
        if self.state_manager:
            try:
                task = self.state_manager.get_task(self.task_id)
                if task and hasattr(task, "last_updated"):
                    self.baseline_db_timestamp = task.last_updated.timestamp()
                    logger.debug(f"Baseline DB timestamp captured: {self.baseline_db_timestamp}")
            except Exception as e:
                logger.warning(f"Failed to capture DB baseline: {e}")
                self.baseline_db_timestamp = None

        logger.info(f"Baseline captured for task {self.task_id} at {self.baseline_timestamp}")

    def check_liveness(self, session_id: str | None = None) -> LivenessStatus:
        """Check task liveness across all indicators.

        Checks all 5 indicators and applies decision logic:
        - 0 active → HUNG
        - 1 active → INVESTIGATE
        - 2+ active → ALIVE

        Args:
            session_id: Optional session ID for production logging

        Returns:
            LivenessStatus enum value (HUNG, INVESTIGATE, or ALIVE)

        Raises:
            RuntimeError: If capture_baseline() not called first

        Example:
            >>> status = monitor.check_liveness(session_id="abc-123")
            >>> if status == LivenessStatus.HUNG:
            ...     print("Task is hung - kill immediately")
            >>> elif status == LivenessStatus.INVESTIGATE:
            ...     print("Ambiguous - run hang investigation")
            >>> else:
            ...     print("Task is alive - extend timeout")
        """
        if self.baseline_timestamp == 0.0:
            raise RuntimeError("Must call capture_baseline() before check_liveness()")

        # Check all 5 indicators
        indicators = {
            "logs_active": self.check_logs_active(),
            "cpu_active": self.check_cpu_active(),
            "files_modified": self.check_files_modified(),
            "db_updated": self.check_db_updated(),
            "process_running": self.check_process_running(),
        }

        # Count active indicators
        alive_count = sum(1 for active in indicators.values() if active)

        logger.info(
            f"Liveness check: task_id={self.task_id}, "
            f"indicators={indicators}, alive_count={alive_count}/{len(indicators)}"
        )

        # Apply decision logic
        if alive_count == 0:
            status = LivenessStatus.HUNG
        elif alive_count == 1:
            status = LivenessStatus.INVESTIGATE
        else:  # alive_count >= 2
            status = LivenessStatus.ALIVE

        # Log liveness check event
        if session_id:
            self.production_logger.log_liveness_check(
                session_id=session_id,
                task_id=self.task_id,
                status=status.value,
                alive_count=alive_count,
                total_indicators=len(indicators),
                indicators=indicators,
            )

        return status

    def check_logs_active(self) -> bool:
        """Check if log file has new entries within threshold.

        Returns:
            True if log file modified within log_silence_threshold seconds
        """
        if not self.log_path or not self.log_path.exists():
            logger.debug("Log file not available for liveness check")
            return False

        try:
            log_mtime = self.log_path.stat().st_mtime
            time_since_log = time.time() - log_mtime
            is_active = time_since_log < self.log_silence_threshold

            logger.debug(
                f"Log activity check: mtime={log_mtime}, "
                f"time_since={time_since_log:.1f}s, "
                f"threshold={self.log_silence_threshold}s, active={is_active}"
            )

            return is_active
        except OSError as e:
            logger.warning(f"Failed to check log activity: {e}")
            return False

    def check_cpu_active(self) -> bool:
        """Check if CPU time has increased since baseline.

        Returns:
            True if CPU delta >= cpu_delta_threshold seconds
        """
        if not self._psutil_available or not self.process_pid:
            logger.debug("CPU activity check unavailable (no psutil or PID)")
            return False

        try:
            import psutil

            process = psutil.Process(self.process_pid)
            cpu_times = process.cpu_times()
            current_cpu = cpu_times.user + cpu_times.system
            cpu_delta = current_cpu - self.baseline_cpu
            is_active = cpu_delta >= self.cpu_delta_threshold

            logger.debug(
                f"CPU activity check: baseline={self.baseline_cpu:.2f}s, "
                f"current={current_cpu:.2f}s, delta={cpu_delta:.2f}s, "
                f"threshold={self.cpu_delta_threshold}s, active={is_active}"
            )

            return is_active
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            logger.warning(f"Failed to check CPU activity: {e}")
            return False

    def check_files_modified(self) -> bool:
        """Check if any workspace files modified since baseline.

        Returns:
            True if any files have mtime > baseline within file_mtime_window
        """
        if not self.workspace_path.exists():
            logger.debug("Workspace path does not exist")
            return False

        try:
            current_time = time.time()

            for file_path in self.workspace_path.rglob("*"):
                if file_path.is_file() and not self._should_ignore_file(file_path):
                    file_path_str = str(file_path)
                    current_mtime = file_path.stat().st_mtime
                    baseline_mtime = self.baseline_file_mtimes.get(file_path_str, 0.0)

                    # Check if file modified since baseline
                    if current_mtime > baseline_mtime:
                        # Check if modification within time window
                        time_since_mod = current_time - current_mtime
                        if time_since_mod < self.file_mtime_window:
                            logger.debug(
                                f"File activity detected: {file_path.name}, "
                                f"modified {time_since_mod:.1f}s ago"
                            )
                            return True

            logger.debug("No recent file modifications detected")
            return False
        except OSError as e:
            logger.warning(f"Failed to check file activity: {e}")
            return False

    def check_db_updated(self) -> bool:
        """Check if task last_updated timestamp changed since baseline.

        Uses StateManager to check task.last_updated field for recent changes.

        Returns:
            True if task.last_updated within db_update_window seconds
        """
        if not self.state_manager or self.baseline_db_timestamp is None:
            logger.debug("DB activity check unavailable (no StateManager or baseline)")
            return False

        try:
            task = self.state_manager.get_task(self.task_id)
            if not task or not hasattr(task, "last_updated"):
                logger.warning(f"Task {self.task_id} not found or missing last_updated")
                return False

            current_db_timestamp = task.last_updated.timestamp()
            time_since_update = time.time() - current_db_timestamp
            is_active = time_since_update < self.db_update_window

            logger.debug(
                f"DB activity check: baseline={self.baseline_db_timestamp:.1f}, "
                f"current={current_db_timestamp:.1f}, "
                f"time_since={time_since_update:.1f}s, "
                f"threshold={self.db_update_window}s, active={is_active}"
            )

            return is_active
        except Exception as e:
            logger.warning(f"Failed to check DB activity: {e}")
            return False

    def check_process_running(self) -> bool:
        """Check if process is in healthy state (not zombie/defunct).

        Returns:
            True if process exists and is in running/sleeping state
        """
        if not self._psutil_available or not self.process_pid:
            logger.debug("Process state check unavailable (no psutil or PID)")
            return False

        try:
            import psutil

            process = psutil.Process(self.process_pid)
            status = process.status()

            # Healthy states: running, sleeping
            # Unhealthy states: zombie, dead, stopped
            healthy_states = {
                psutil.STATUS_RUNNING,
                psutil.STATUS_SLEEPING,
                psutil.STATUS_DISK_SLEEP,
            }

            is_healthy = status in healthy_states

            logger.debug(
                f"Process state check: pid={self.process_pid}, "
                f"status={status}, healthy={is_healthy}"
            )

            return is_healthy
        except psutil.NoSuchProcess:
            logger.warning(f"Process {self.process_pid} no longer exists")
            return False
        except psutil.AccessDenied as e:
            logger.warning(f"Access denied to process {self.process_pid}: {e}")
            return False

    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored in liveness checks.

        Ignores common cache/build directories and file types.

        Args:
            file_path: Path to file

        Returns:
            True if file should be ignored
        """
        ignore_parts = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            "venv",
            ".pytest_cache",
            ".mypy_cache",
            ".ruff_cache",
        }

        ignore_suffixes = {".pyc", ".pyo", ".pyd", ".so", ".o"}

        # Check if any ignore pattern in path
        if any(part in file_path.parts for part in ignore_parts):
            return True

        # Check if file has ignore suffix
        if file_path.suffix in ignore_suffixes:
            return True

        return False
