"""Hang investigation system for diagnosing task execution stalls.

This module provides the HangInvestigator class which performs deep analysis
when liveness detection returns INVESTIGATE status (1 active indicator).

Part of FEAT-TIMEOUT-LIVENESS-001: Intelligent Timeout with Liveness Detection.
"""

import logging
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class HangClassification(Enum):
    """Classification of hang type.

    Attributes:
        REAL_HANG: True hang - process stuck, no progress possible
        SLOW_PROGRESS: Legitimate slow progress - extend timeout
        EXTERNAL_BLOCKING: Blocked by external resource (I/O, network)
        UNKNOWN: Unable to classify with available evidence
    """

    REAL_HANG = "real_hang"
    SLOW_PROGRESS = "slow_progress"
    EXTERNAL_BLOCKING = "external_blocking"
    UNKNOWN = "unknown"


@dataclass
class ProcessStateInfo:
    """Process state information from /proc or psutil.

    Attributes:
        pid: Process ID
        state: Process state (R/S/D/Z/T)
        wchan: Kernel function where process is sleeping (if available)
        cpu_time: Total CPU time consumed (user + system)
        threads: Number of threads
        open_files: Number of open file descriptors
    """

    pid: int
    state: str
    wchan: str | None = None
    cpu_time: float = 0.0
    threads: int = 1
    open_files: int = 0


@dataclass
class SubprocessInfo:
    """Information about subprocess tree.

    Attributes:
        zombie_count: Number of zombie child processes
        orphaned_waits: PIDs of processes waiting on orphaned subprocesses
        subprocess_pids: List of all subprocess PIDs
    """

    zombie_count: int = 0
    orphaned_waits: list[int] = None
    subprocess_pids: list[int] = None

    def __post_init__(self):
        """Initialize mutable default arguments."""
        if self.orphaned_waits is None:
            self.orphaned_waits = []
        if self.subprocess_pids is None:
            self.subprocess_pids = []


@dataclass
class IOBlockingInfo:
    """I/O blocking information.

    Attributes:
        blocked_on_io: Whether process is blocked on I/O
        open_pipes: Number of open pipes
        open_sockets: Number of open sockets
        blocking_file: Path to file causing block (if identifiable)
    """

    blocked_on_io: bool = False
    open_pipes: int = 0
    open_sockets: int = 0
    blocking_file: Path | None = None


@dataclass
class HangEvidence:
    """Evidence collected during hang investigation.

    Attributes:
        process_state: Process state information
        subprocess_info: Subprocess tree information
        io_blocking: I/O blocking information
        classification: Hang classification result
        confidence: Confidence in classification (0.0-1.0)
        action_recommended: Recommended action (kill, extend, investigate)
        details: Additional diagnostic details
    """

    process_state: ProcessStateInfo | None = None
    subprocess_info: SubprocessInfo | None = None
    io_blocking: IOBlockingInfo | None = None
    classification: HangClassification = HangClassification.UNKNOWN
    confidence: float = 0.0
    action_recommended: str = "investigate"
    details: dict[str, Any] = None

    def __post_init__(self):
        """Initialize mutable default arguments."""
        if self.details is None:
            self.details = {}


class HangInvestigator:
    """Investigate task hangs to classify as real hang vs slow progress.

    This class is invoked when LivenessMonitor returns INVESTIGATE status
    (exactly 1 active indicator). It performs deep process analysis to
    determine whether the task is truly hung or making legitimate slow progress.

    Analysis methods:
    1. Process state analysis - extract state, wchan, CPU delta
    2. Subprocess tree analysis - detect zombie children, orphaned waits
    3. I/O blocking analysis - detect I/O waits via lsof/psutil

    Classification logic:
    - REAL_HANG: Process in S state, wchan on defunct subprocess wait
    - SLOW_PROGRESS: Active CPU delta, normal state, no blocking
    - EXTERNAL_BLOCKING: Blocked on I/O, network, or external resource
    - UNKNOWN: Insufficient evidence for classification

    Example:
        >>> investigator = HangInvestigator(
        ...     pid=12345,
        ...     config=config,
        ...     workspace_path=Path("./workspace")
        ... )
        >>> evidence = investigator.investigate()
        >>> if evidence.classification == HangClassification.REAL_HANG:
        ...     kill_process(evidence.process_state.pid)

    Attributes:
        pid: Process ID to investigate
        config: Configuration dict with investigation thresholds
        workspace_path: Path to task workspace directory
        investigation_timeout: Max time to spend investigating (seconds)
    """

    def __init__(
        self,
        pid: int,
        config: dict[str, Any],
        workspace_path: Path,
        production_logger: Any,
        task_id: int | None = None,
    ):
        """Initialize hang investigator.

        Args:
            pid: Process ID to investigate
            config: Configuration dict containing orchestration.hang_investigation settings
            workspace_path: Path to task workspace directory
            production_logger: ProductionLogger instance for event logging
            task_id: Optional task ID for logging
        """
        self.pid = pid
        self.config = config
        self.workspace_path = workspace_path
        self.production_logger = production_logger
        self.task_id = task_id

        # Extract thresholds from config (with defaults)
        investigation_config = config.get("orchestration", {}).get("hang_investigation", {})
        self.investigation_timeout = investigation_config.get("investigation_timeout", 300)
        self.zombie_threshold = investigation_config.get("zombie_threshold", 1)
        self.cpu_delta_threshold = investigation_config.get("cpu_delta_threshold", 1.0)
        self.io_wait_threshold = investigation_config.get("io_wait_threshold", 60)

        # psutil availability flag
        self._psutil_available = False
        try:
            import psutil

            self._psutil_available = True
            logger.debug("psutil available for process investigation")
        except ImportError:
            logger.warning(
                "psutil not available - process investigation limited. "
                "Install psutil for full investigation: pip install psutil"
            )

        # Platform detection
        self._has_proc_fs = Path("/proc").exists()
        if not self._has_proc_fs:
            logger.info("No /proc filesystem - using psutil-only mode (macOS compatible)")

        logger.info(
            f"HangInvestigator initialized: pid={pid}, "
            f"timeout={self.investigation_timeout}s, "
            f"psutil={'available' if self._psutil_available else 'unavailable'}, "
            f"proc_fs={'available' if self._has_proc_fs else 'unavailable'}"
        )

    def investigate(self, session_id: str | None = None) -> HangEvidence:
        """Run full hang investigation and return classification.

        Performs all analysis methods and synthesizes evidence into
        a classification with recommended action.

        Args:
            session_id: Optional session ID for production logging

        Returns:
            HangEvidence with classification, confidence, and action

        Example:
            >>> evidence = investigator.investigate(session_id="abc-123")
            >>> print(evidence.classification)  # HangClassification.REAL_HANG
            >>> print(evidence.action_recommended)  # "kill"
            >>> print(evidence.confidence)  # 0.95
        """
        import time

        logger.info(f"Starting hang investigation for PID {self.pid}")
        start_time = time.time()

        # Log investigation started event
        if session_id and self.task_id is not None:
            self.production_logger.log_hang_investigation_started(
                session_id=session_id,
                task_id=self.task_id,
                pid=self.pid,
            )

        # Collect evidence from all analysis methods with timeout checks
        process_state = self.analyze_process_state()

        # Check timeout after first analysis
        elapsed = time.time() - start_time
        if elapsed > self.investigation_timeout:
            logger.warning(
                f"Investigation timeout after process_state analysis: "
                f"{elapsed:.1f}s > {self.investigation_timeout}s"
            )
            return self._create_timeout_evidence(elapsed)

        subprocess_info = self.analyze_subprocess_tree()

        # Check timeout after second analysis
        elapsed = time.time() - start_time
        if elapsed > self.investigation_timeout:
            logger.warning(
                f"Investigation timeout after subprocess analysis: "
                f"{elapsed:.1f}s > {self.investigation_timeout}s"
            )
            return self._create_timeout_evidence(elapsed)

        io_blocking = self.analyze_io_blocking()

        # Check timeout after third analysis
        elapsed = time.time() - start_time
        if elapsed > self.investigation_timeout:
            logger.warning(
                f"Investigation timeout after io_blocking analysis: "
                f"{elapsed:.1f}s > {self.investigation_timeout}s"
            )
            return self._create_timeout_evidence(elapsed)

        # Classify hang based on collected evidence
        evidence = self.classify_hang(process_state, subprocess_info, io_blocking)

        logger.info(
            f"Investigation complete: classification={evidence.classification.value}, "
            f"confidence={evidence.confidence:.2f}, action={evidence.action_recommended}"
        )

        # Log investigation complete event
        if session_id and self.task_id is not None:
            # Build evidence dict from collected data
            evidence_dict = {}
            if process_state:
                evidence_dict["process_state"] = process_state.state
                evidence_dict["wchan"] = process_state.wchan
                evidence_dict["cpu_time"] = process_state.cpu_time
                evidence_dict["threads"] = process_state.threads
            if subprocess_info:
                evidence_dict["zombie_count"] = subprocess_info.zombie_count
                evidence_dict["orphaned_waits"] = subprocess_info.orphaned_waits
                evidence_dict["subprocess_count"] = len(subprocess_info.subprocess_pids)
            if io_blocking:
                evidence_dict["blocked_on_io"] = io_blocking.blocked_on_io
                evidence_dict["open_pipes"] = io_blocking.open_pipes
                evidence_dict["open_sockets"] = io_blocking.open_sockets
                if io_blocking.blocking_file:
                    evidence_dict["blocking_file"] = str(io_blocking.blocking_file)
            # Add classification details
            evidence_dict.update(evidence.details)

            self.production_logger.log_hang_investigation_complete(
                session_id=session_id,
                task_id=self.task_id,
                pid=self.pid,
                classification=evidence.classification.value,
                confidence=evidence.confidence,
                action_recommended=evidence.action_recommended,
                evidence=evidence_dict,
            )

        return evidence

    def analyze_process_state(self) -> ProcessStateInfo | None:
        """Analyze process state from /proc or psutil.

        Extracts:
        - Process state (R/S/D/Z/T)
        - wchan (kernel function where sleeping)
        - CPU time (user + system)
        - Thread count
        - Open file descriptor count

        Returns:
            ProcessStateInfo or None if analysis fails

        Example:
            >>> info = investigator.analyze_process_state()
            >>> print(info.state)  # "S"
            >>> print(info.wchan)  # "wait4"
            >>> print(info.cpu_time)  # 45.2
        """
        if not self._psutil_available:
            logger.debug("Cannot analyze process state - psutil unavailable")
            return None

        try:
            import psutil

            process = psutil.Process(self.pid)

            # Get process state
            state = process.status()
            # Map psutil status to single-char state
            # Build state_map dynamically to handle version differences
            state_map = {}
            if hasattr(psutil, "STATUS_RUNNING"):
                state_map[psutil.STATUS_RUNNING] = "R"
            if hasattr(psutil, "STATUS_SLEEPING"):
                state_map[psutil.STATUS_SLEEPING] = "S"
            if hasattr(psutil, "STATUS_DISK_SLEEP"):
                state_map[psutil.STATUS_DISK_SLEEP] = "D"
            if hasattr(psutil, "STATUS_ZOMBIE"):
                state_map[psutil.STATUS_ZOMBIE] = "Z"
            if hasattr(psutil, "STATUS_STOPPED"):
                state_map[psutil.STATUS_STOPPED] = "T"
            if hasattr(psutil, "STATUS_TRACING_STOP"):
                state_map[psutil.STATUS_TRACING_STOP] = "T"
            if hasattr(psutil, "STATUS_DEAD"):
                state_map[psutil.STATUS_DEAD] = "X"
            if hasattr(psutil, "STATUS_WAKING"):
                state_map[psutil.STATUS_WAKING] = "W"
            if hasattr(psutil, "STATUS_IDLE"):
                state_map[psutil.STATUS_IDLE] = "I"
            if hasattr(psutil, "STATUS_LOCKED"):
                state_map[psutil.STATUS_LOCKED] = "L"
            if hasattr(psutil, "STATUS_WAITING"):
                state_map[psutil.STATUS_WAITING] = "W"
            if hasattr(psutil, "STATUS_PARKED"):
                state_map[psutil.STATUS_PARKED] = "P"

            state_char = state_map.get(state, "?")

            # Get CPU time
            cpu_times = process.cpu_times()
            cpu_time = cpu_times.user + cpu_times.system

            # Get thread count
            try:
                threads = process.num_threads()
            except (psutil.AccessDenied, AttributeError):
                threads = 1

            # Get open files count
            try:
                open_files = len(process.open_files())
            except (psutil.AccessDenied, OSError):
                open_files = 0

            # Try to get wchan from /proc (Linux only)
            wchan = None
            if self._has_proc_fs:
                try:
                    wchan_path = Path(f"/proc/{self.pid}/wchan")
                    wchan = wchan_path.read_text().strip()
                    if wchan == "0":
                        wchan = None
                except (OSError, PermissionError):
                    pass

            info = ProcessStateInfo(
                pid=self.pid,
                state=state_char,
                wchan=wchan,
                cpu_time=cpu_time,
                threads=threads,
                open_files=open_files,
            )

            logger.debug(
                f"Process state: state={state_char}, wchan={wchan}, "
                f"cpu_time={cpu_time:.2f}s, threads={threads}, open_files={open_files}"
            )

            return info

        except psutil.NoSuchProcess:
            logger.warning(f"Process {self.pid} no longer exists")
            return None
        except psutil.AccessDenied as e:
            logger.warning(f"Access denied to process {self.pid}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to analyze process state: {e}", exc_info=True)
            return None

    def analyze_subprocess_tree(self) -> SubprocessInfo:
        """Analyze subprocess tree for zombie children and orphaned waits.

        Detects:
        - Zombie child processes
        - Processes waiting on orphaned/zombie children
        - All subprocess PIDs in tree

        Returns:
            SubprocessInfo with subprocess analysis

        Example:
            >>> info = investigator.analyze_subprocess_tree()
            >>> print(info.zombie_count)  # 2
            >>> print(info.orphaned_waits)  # [12346]
        """
        info = SubprocessInfo()

        if not self._psutil_available:
            logger.debug("Cannot analyze subprocess tree - psutil unavailable")
            return info

        try:
            import psutil

            process = psutil.Process(self.pid)

            # Get all child processes
            children = process.children(recursive=True)

            # Collect zombie processes and all subprocess PIDs
            zombies: list[int] = []
            for child in children:
                info.subprocess_pids.append(child.pid)
                try:
                    if child.status() == psutil.STATUS_ZOMBIE:
                        zombies.append(child.pid)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

            info.zombie_count = len(zombies)

            # Detect orphaned waits - parent waiting on zombie child
            # Check if main process is in S state with wchan indicating wait
            if zombies:
                process_state = process.status()
                if process_state == psutil.STATUS_SLEEPING:
                    # Try to check wchan for wait-related syscalls
                    if self._has_proc_fs:
                        try:
                            wchan_path = Path(f"/proc/{self.pid}/wchan")
                            wchan = wchan_path.read_text().strip()
                            wait_syscalls = {"wait4", "waitpid", "do_wait", "wait_consider_task"}
                            if wchan in wait_syscalls:
                                info.orphaned_waits.append(self.pid)
                                logger.debug(
                                    f"Detected orphaned wait: PID {self.pid} waiting on zombie children"
                                )
                        except (OSError, PermissionError):
                            pass

            logger.debug(
                f"Subprocess tree: children={len(info.subprocess_pids)}, "
                f"zombies={info.zombie_count}, orphaned_waits={len(info.orphaned_waits)}"
            )

            return info

        except psutil.NoSuchProcess:
            logger.warning(f"Process {self.pid} no longer exists")
            return info
        except psutil.AccessDenied as e:
            logger.warning(f"Access denied to process {self.pid}: {e}")
            return info
        except Exception as e:
            logger.error(f"Failed to analyze subprocess tree: {e}", exc_info=True)
            return info

    def analyze_io_blocking(self) -> IOBlockingInfo:
        """Analyze I/O blocking using lsof and psutil.

        Detects:
        - Process blocked on I/O (D state)
        - Open pipes and sockets
        - Specific file causing block (if identifiable)

        Returns:
            IOBlockingInfo with I/O analysis

        Example:
            >>> info = investigator.analyze_io_blocking()
            >>> print(info.blocked_on_io)  # True
            >>> print(info.blocking_file)  # Path("/tmp/slow_disk.dat")
        """
        info = IOBlockingInfo()

        if not self._psutil_available:
            logger.debug("Cannot analyze I/O blocking - psutil unavailable")
            return info

        try:
            import psutil

            process = psutil.Process(self.pid)

            # Check if process in D state (uninterruptible sleep - I/O)
            state = process.status()
            info.blocked_on_io = state == psutil.STATUS_DISK_SLEEP

            # Count open pipes and sockets
            try:
                connections = process.connections(kind="all")
                info.open_sockets = len(connections)
            except (psutil.AccessDenied, OSError):
                pass

            # Check for pipes in open files
            try:
                open_files = process.open_files()
                for file_info in open_files:
                    file_path = Path(file_info.path)
                    # Count pipes (typically have "pipe:" prefix or in /proc/self/fd/)
                    if "pipe:" in str(file_path) or "/proc/" in str(file_path):
                        info.open_pipes += 1
                    # Check if file might be on slow I/O
                    # (heuristic: files on network mounts, external drives)
                    if info.blocked_on_io and not info.blocking_file:
                        # Simple heuristic: non-local paths
                        if any(
                            prefix in str(file_path) for prefix in ["/mnt/", "/media/", "/net/"]
                        ):
                            info.blocking_file = file_path
            except (psutil.AccessDenied, OSError):
                pass

            # Try using lsof for more detailed I/O analysis (Linux/macOS)
            if info.blocked_on_io and not info.blocking_file:
                info.blocking_file = self._try_lsof_blocking_file()

            logger.debug(
                f"I/O blocking: blocked={info.blocked_on_io}, "
                f"pipes={info.open_pipes}, sockets={info.open_sockets}, "
                f"blocking_file={info.blocking_file}"
            )

            return info

        except psutil.NoSuchProcess:
            logger.warning(f"Process {self.pid} no longer exists")
            return info
        except psutil.AccessDenied as e:
            logger.warning(f"Access denied to process {self.pid}: {e}")
            return info
        except Exception as e:
            logger.error(f"Failed to analyze I/O blocking: {e}", exc_info=True)
            return info

    def _try_lsof_blocking_file(self) -> Path | None:
        """Attempt to use lsof to identify blocking file.

        Returns:
            Path to blocking file or None if not found
        """
        try:
            # Run lsof to get open files for process
            # MONITORING EXEMPTION: Diagnostic lsof call (<2s typical, 5s timeout)
            result = subprocess.run(
                ["lsof", "-p", str(self.pid)],
                check=False, capture_output=True,
                text=True,
                timeout=5,
            )

            if result.returncode == 0:
                # Parse lsof output for files (skip headers)
                lines = result.stdout.strip().split("\n")[1:]
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 9:
                        file_path = " ".join(parts[8:])
                        # Look for regular files (not sockets/pipes)
                        if parts[4] == "REG" and Path(file_path).exists():
                            return Path(file_path)

        except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
            # lsof not available or failed - not critical
            pass

        return None

    def classify_hang(
        self,
        process_state: ProcessStateInfo | None,
        subprocess_info: SubprocessInfo,
        io_blocking: IOBlockingInfo,
    ) -> HangEvidence:
        """Classify hang type based on collected evidence.

        Classification logic:
        1. REAL_HANG (high confidence):
           - Zombie children + parent waiting (orphaned wait)
           - Process in S/D state with no progress indicators

        2. SLOW_PROGRESS (medium confidence):
           - Active CPU time delta
           - Normal process state (R/S without blocking)
           - No zombie children

        3. EXTERNAL_BLOCKING (medium confidence):
           - Process in D state (I/O wait)
           - Open network connections
           - Blocking file identified

        4. UNKNOWN (low confidence):
           - Insufficient evidence
           - Conflicting indicators

        Args:
            process_state: Process state information
            subprocess_info: Subprocess tree information
            io_blocking: I/O blocking information

        Returns:
            HangEvidence with classification, confidence, and recommended action

        Example:
            >>> evidence = investigator.classify_hang(state, subprocess, io)
            >>> print(evidence.classification)  # HangClassification.REAL_HANG
            >>> print(evidence.confidence)  # 0.95
            >>> print(evidence.action_recommended)  # "kill"
        """
        evidence = HangEvidence(
            process_state=process_state,
            subprocess_info=subprocess_info,
            io_blocking=io_blocking,
        )

        # Rule 1: Orphaned wait on zombie child = REAL_HANG (highest confidence)
        if subprocess_info.zombie_count >= self.zombie_threshold and subprocess_info.orphaned_waits:
            evidence.classification = HangClassification.REAL_HANG
            evidence.confidence = 0.95
            evidence.action_recommended = "kill"
            evidence.details = {
                "reason": "orphaned_wait_on_zombie",
                "zombie_count": subprocess_info.zombie_count,
                "waiting_pids": subprocess_info.orphaned_waits,
            }
            logger.info(
                f"Classified as REAL_HANG: orphaned wait on {subprocess_info.zombie_count} zombie children"
            )
            return evidence

        # Rule 2: I/O blocking = EXTERNAL_BLOCKING (high confidence if blocking file identified)
        if io_blocking.blocked_on_io:
            evidence.classification = HangClassification.EXTERNAL_BLOCKING
            evidence.confidence = 0.85 if io_blocking.blocking_file else 0.65
            evidence.action_recommended = "extend"
            evidence.details = {
                "reason": "io_wait",
                "blocking_file": (
                    str(io_blocking.blocking_file) if io_blocking.blocking_file else None
                ),
                "open_sockets": io_blocking.open_sockets,
            }
            logger.info(
                f"Classified as EXTERNAL_BLOCKING: I/O wait on {io_blocking.blocking_file or 'unknown file'}"
            )
            return evidence

        # Rule 3: Process state indicates hang
        if process_state:
            # Sleeping state with wchan indicating wait = potential hang
            if process_state.state == "S" and process_state.wchan:
                wait_syscalls = {"wait4", "waitpid", "do_wait", "wait_consider_task"}
                if process_state.wchan in wait_syscalls:
                    # Waiting without zombie children = might be legitimate
                    if subprocess_info.zombie_count == 0:
                        evidence.classification = HangClassification.SLOW_PROGRESS
                        evidence.confidence = 0.60
                        evidence.action_recommended = "extend"
                        evidence.details = {
                            "reason": "waiting_on_subprocess",
                            "wchan": process_state.wchan,
                            "subprocess_count": len(subprocess_info.subprocess_pids),
                        }
                        logger.info("Classified as SLOW_PROGRESS: waiting on active subprocess")
                        return evidence

            # Running state = likely making progress
            if process_state.state == "R":
                evidence.classification = HangClassification.SLOW_PROGRESS
                evidence.confidence = 0.75
                evidence.action_recommended = "extend"
                evidence.details = {
                    "reason": "process_running",
                    "cpu_time": process_state.cpu_time,
                }
                logger.info("Classified as SLOW_PROGRESS: process in running state")
                return evidence

        # Rule 4: No strong evidence = UNKNOWN (low confidence)
        evidence.classification = HangClassification.UNKNOWN
        evidence.confidence = 0.30
        evidence.action_recommended = "investigate"
        evidence.details = {
            "reason": "insufficient_evidence",
            "process_available": process_state is not None,
            "subprocess_count": len(subprocess_info.subprocess_pids),
            "zombie_count": subprocess_info.zombie_count,
        }
        logger.info("Classified as UNKNOWN: insufficient evidence for confident classification")
        return evidence

    def _create_timeout_evidence(self, elapsed_time: float) -> HangEvidence:
        """Create HangEvidence for investigation timeout.

        Args:
            elapsed_time: Time elapsed before timeout (seconds)

        Returns:
            HangEvidence with UNKNOWN classification and investigate action
        """
        evidence = HangEvidence(
            classification=HangClassification.UNKNOWN,
            confidence=0.0,
            action_recommended="investigate",
            details={
                "reason": "investigation_timeout",
                "elapsed_time": elapsed_time,
                "timeout_threshold": self.investigation_timeout,
                "message": f"Investigation aborted after {elapsed_time:.1f}s (timeout: {self.investigation_timeout}s)",
            },
        )
        return evidence
