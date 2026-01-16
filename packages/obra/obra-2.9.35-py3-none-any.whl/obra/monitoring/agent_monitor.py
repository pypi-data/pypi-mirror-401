"""Shared agent monitoring infrastructure for timeout and liveness detection.

This module provides MonitoringThread, a reusable class for monitoring agent
subprocess execution with intelligent timeout management and hang detection.

FEAT-TIMEOUT-LIVENESS-001 S5.T1: Refactored from ClaudeCodeLocalAgent for
reuse across all agent types (Claude Code, OpenAI Codex, Gemini CLI).
"""

import logging
import subprocess
import threading
import time
from pathlib import Path
from typing import Any

from obra.monitoring.hang_investigator import HangClassification, HangInvestigator
from obra.monitoring.liveness_monitor import LivenessMonitor, LivenessStatus

LIVENESS_AVAILABLE = True

logger = logging.getLogger(__name__)


class MonitoringThread:
    """Manages timeout monitoring for agent subprocess execution.

    Provides 3-tier intelligent timeout monitoring:
    1. Liveness detection - checks multiple activity indicators
    2. Hang investigation - forensic analysis when liveness ambiguous
    3. Adaptive timeout - extends timeout for tasks showing progress

    Key Features:
    - Thread-safe operation (daemon mode)
    - Configurable check intervals and timeouts
    - Auto-kill on confirmed hangs (optional)
    - Graceful shutdown on task completion
    - Event-based communication with parent thread

    Attributes:
        process: subprocess.Popen object to monitor
        config: Configuration dict with timeout settings
        workspace_path: Path to workspace directory
        state_manager: Optional StateManager for DB activity checks
        task_id: Optional task ID for state manager access
        base_timeout: Initial timeout in seconds

    Thread State Events:
        monitoring_active: Signals thread to stop monitoring
        timeout_extended: Signals timeout has been extended
        process_killed: Signals process was killed by monitor
    """

    def __init__(
        self,
        process: subprocess.Popen,
        config: dict[str, Any],
        workspace_path: Path,
        production_logger: Any,
        session_id: str,
        state_manager: Any | None = None,
        task_id: int | None = None,
        base_timeout: float = 1200,
    ):
        """Initialize monitoring thread manager.

        Args:
            process: subprocess.Popen object to monitor
            config: Configuration dict with timeout settings
            workspace_path: Path to workspace directory
            production_logger: ProductionLogger for event logging
            session_id: Session ID for event logging
            state_manager: Optional StateManager for DB activity checks
            task_id: Optional task ID for state manager access
            base_timeout: Initial timeout in seconds (default: 1200 = 20 min)
        """
        self.process = process
        self.config = config
        self.workspace_path = workspace_path
        self.production_logger = production_logger
        self.session_id = session_id
        self.state_manager = state_manager
        self.task_id = task_id or 0
        self.base_timeout = base_timeout

        # Thread state
        self._thread: threading.Thread | None = None
        self._monitoring_active = threading.Event()  # Signal to stop monitoring
        self._timeout_extended = threading.Event()  # Signal timeout extension
        self._process_killed = threading.Event()  # Signal process killed

        # Current effective timeout (starts at base, may extend)
        self.current_timeout = base_timeout

        logger.debug(
            f"MonitoringThread initialized: PID={process.pid}, base_timeout={base_timeout}s"
        )

    def start(self) -> None:
        """Start monitoring thread in daemon mode.

        Thread will run in background, checking liveness periodically and
        extending timeout or killing process as needed.
        """
        if not LIVENESS_AVAILABLE:
            logger.warning("Liveness monitoring unavailable - monitoring disabled")
            return

        # Reset state
        self._monitoring_active.clear()
        self._timeout_extended.clear()
        self._process_killed.clear()
        self.current_timeout = self.base_timeout

        # Create and start thread
        self._thread = threading.Thread(
            target=self._worker,
            daemon=True,  # Daemon thread exits when main thread exits
            name="agent-liveness-monitor",
        )
        self._thread.start()
        logger.info(
            f"Monitoring thread started: PID={self.process.pid}, "
            f"base_timeout={self.base_timeout}s"
        )

    def stop(self, timeout: float = 2.0) -> None:
        """Stop monitoring thread gracefully.

        Args:
            timeout: Maximum seconds to wait for thread to exit
        """
        if not self._thread or not self._thread.is_alive():
            return

        self._monitoring_active.set()  # Signal thread to stop
        self._thread.join(timeout=timeout)

        if self._thread.is_alive():
            logger.warning("Monitoring thread did not exit cleanly")
        else:
            logger.debug("Monitoring thread stopped gracefully")

    def is_process_killed(self) -> bool:
        """Check if monitoring thread killed the process.

        Returns:
            True if process was killed by hang detection
        """
        return self._process_killed.is_set()

    def is_timeout_extended(self) -> bool:
        """Check if timeout was extended by liveness detection.

        Returns:
            True if timeout was extended due to progress
        """
        return self._timeout_extended.is_set()

    def get_current_timeout(self) -> float:
        """Get current effective timeout in seconds.

        Returns:
            Current timeout (may be extended from base_timeout)
        """
        return self.current_timeout

    def _worker(self) -> None:
        """Monitoring thread worker - runs liveness checks and hang investigation.

        This is the core monitoring loop that:
        1. Checks liveness periodically (every liveness_check_interval)
        2. Extends timeout when task shows progress (ALIVE status)
        3. Investigates ambiguous cases (INVESTIGATE status)
        4. Kills hung processes (HUNG status or confirmed real hang)

        Runs until process completes or monitoring_active signal received.
        """
        if not LIVENESS_AVAILABLE:
            logger.warning("Liveness monitoring unavailable - worker exiting")
            return

        try:
            # Extract timeout config
            timeout_config = self.config.get("orchestration", {}).get("timeout", {})
            investigation_config = self.config.get("orchestration", {}).get(
                "hang_investigation", {}
            )

            liveness_check_interval = timeout_config.get("liveness_check_interval", 180)
            extended_timeout = timeout_config.get("extended_timeout", 3600)
            auto_kill = investigation_config.get("auto_kill_on_confirmed_hang", True)

            # Determine log path (default to ~/obra-runtime/logs/production.jsonl)
            log_path_candidate = Path.home() / "obra-runtime" / "logs" / "production.jsonl"
            log_path: Path | None = log_path_candidate if log_path_candidate.exists() else None

            # Initialize LivenessMonitor
            monitor = LivenessMonitor(
                task_id=self.task_id,
                config=self.config,
                workspace_path=self.workspace_path,
                log_path=log_path,
                state_manager=self.state_manager,
                process_pid=self.process.pid,
                production_logger=self.production_logger,
            )

            # Capture baseline
            monitor.capture_baseline()
            logger.info(
                f"Monitoring worker started: PID={self.process.pid}, "
                f"interval={liveness_check_interval}s, "
                f"base_timeout={self.base_timeout}s, extended_timeout={extended_timeout}s"
            )

            # Liveness check loop
            start_time = time.time()
            while not self._monitoring_active.is_set():
                # Sleep for check interval (with early exit on stop signal)
                if self._monitoring_active.wait(timeout=liveness_check_interval):
                    logger.debug("Monitoring worker received stop signal")
                    break

                # Check if process still running
                if self.process.poll() is not None:
                    logger.info("Process completed - monitoring worker exiting")
                    break

                # Check liveness
                try:
                    status = monitor.check_liveness(session_id=self.session_id)
                    elapsed = time.time() - start_time

                    logger.info(
                        f"Liveness check: status={status.value}, elapsed={elapsed:.1f}s, "
                        f"current_timeout={self.current_timeout:.1f}s"
                    )

                    # ALIVE status - extend timeout
                    if status == LivenessStatus.ALIVE:
                        if self.current_timeout < extended_timeout:
                            old_timeout = self.current_timeout
                            self.current_timeout = extended_timeout
                            self._timeout_extended.set()
                            logger.info(
                                f"Timeout extended: task showing progress, "
                                f"new_timeout={extended_timeout}s"
                            )

                            # Log timeout extension event
                            self.production_logger.log_timeout_extended(
                                session_id=self.session_id,
                                task_id=self.task_id,
                                pid=self.process.pid,
                                reason="liveness_alive",
                                old_timeout=old_timeout,
                                new_timeout=extended_timeout,
                                justification="Task showing clear progress (2+ liveness indicators active)",
                            )

                    # INVESTIGATE status - run hang investigation
                    elif status == LivenessStatus.INVESTIGATE:
                        logger.warning("Ambiguous liveness (1 indicator) - starting investigation")

                        investigator = HangInvestigator(
                            pid=self.process.pid,
                            config=self.config,
                            workspace_path=self.workspace_path,
                            task_id=self.task_id,
                            production_logger=self.production_logger,
                        )

                        evidence = investigator.investigate(session_id=self.session_id)

                        logger.info(
                            f"Investigation complete: classification={evidence.classification.value}, "
                            f"confidence={evidence.confidence:.2f}, "
                            f"action={evidence.action_recommended}"
                        )

                        # REAL_HANG classification - kill process if auto_kill enabled
                        if evidence.classification == HangClassification.REAL_HANG and auto_kill:
                            logger.error(
                                f"Confirmed hang detected - killing process PID={self.process.pid} "
                                f"(confidence={evidence.confidence:.2f})"
                            )

                            try:
                                self.process.terminate()
                                signal_sent = "SIGTERM"
                                time.sleep(2)  # Wait for graceful termination

                                if self.process.poll() is None:
                                    logger.warning("Process did not terminate - sending SIGKILL")
                                    self.process.kill()
                                    signal_sent = "SIGKILL"

                                self._process_killed.set()
                                logger.info("Process killed successfully")

                                # Log hang detection event
                                self.production_logger.log_hang_detected(
                                    session_id=self.session_id,
                                    task_id=self.task_id,
                                    pid=self.process.pid,
                                    classification="real_hang",
                                    signal_sent=signal_sent,
                                    confidence=evidence.confidence,
                                )

                                break

                            except Exception as e:
                                logger.error(f"Failed to kill process: {e}")

                        # SLOW_PROGRESS or EXTERNAL_BLOCKING - extend timeout
                        elif evidence.action_recommended == "extend":
                            if self.current_timeout < extended_timeout:
                                old_timeout = self.current_timeout
                                self.current_timeout = extended_timeout
                                self._timeout_extended.set()
                                logger.info(
                                    f"Timeout extended after investigation: "
                                    f"classification={evidence.classification.value}, "
                                    f"new_timeout={extended_timeout}s"
                                )

                                # Log timeout extension event
                                self.production_logger.log_timeout_extended(
                                    session_id=self.session_id,
                                    task_id=self.task_id,
                                    pid=self.process.pid,
                                    reason="investigation_result",
                                    old_timeout=old_timeout,
                                    new_timeout=extended_timeout,
                                    justification=f"Investigation classified as {evidence.classification.value} "
                                    f"(confidence={evidence.confidence:.2f})",
                                )

                    # HUNG status - immediate kill (0 indicators active)
                    elif status == LivenessStatus.HUNG:
                        logger.error(
                            f"Task hung - no liveness indicators active, "
                            f"killing process PID={self.process.pid}"
                        )

                        try:
                            self.process.terminate()
                            signal_sent = "SIGTERM"
                            time.sleep(2)

                            if self.process.poll() is None:
                                self.process.kill()
                                signal_sent = "SIGKILL"

                            self._process_killed.set()
                            logger.info("Hung process killed successfully")

                            # Log hang detection event
                            self.production_logger.log_hang_detected(
                                session_id=self.session_id,
                                task_id=self.task_id,
                                pid=self.process.pid,
                                classification="hung_zero_indicators",
                                signal_sent=signal_sent,
                                confidence=1.0,  # High confidence - 0 indicators is definitive
                            )

                            break

                        except Exception as e:
                            logger.error(f"Failed to kill hung process: {e}")

                except Exception as e:
                    logger.error(f"Error during liveness check: {e}", exc_info=True)

            logger.info("Monitoring worker exiting")

        except Exception as e:
            logger.error(f"Monitoring worker crashed: {e}", exc_info=True)
