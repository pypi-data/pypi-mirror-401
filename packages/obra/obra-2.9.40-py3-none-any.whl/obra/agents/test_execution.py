"""Test execution agent for running actual pytest tests.

This module provides TestExecutionAgent, which executes pytest tests
synchronously and reports failures as issues.

Unlike TestingAgent (which analyzes test coverage using LLM), this agent
actually runs tests and reports concrete failures.

Checks Performed:
    - Executes pytest with configurable arguments
    - Parses pytest output for failures
    - Reports failed tests as issues with test name and error message
    - Supports configurable timeout

Execution Modes:
    - Synchronous: Runs pytest and waits for completion (default)
    - Asynchronous: Returns immediately with pending status (for LLM orchestration)

Related:
    - obra/agents/base.py
    - obra/agents/registry.py
    - obra/agents/testing.py (LLM-based coverage analysis)
    - BUG-76536c57: Fixed signature to match BaseAgent (llm_config parameter)
"""

import logging
import re
import subprocess
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

from obra.agents.base import AgentIssue, AgentResult, BaseAgent
from obra.agents.registry import register_agent
from obra.api.protocol import AgentType, Priority

logger = logging.getLogger(__name__)


@register_agent(AgentType.TEST_EXECUTION)
class TestExecutionAgent(BaseAgent):
    """Test execution agent that runs actual pytest tests.

    This agent executes pytest synchronously and reports test failures
    as concrete issues. It does not use LLM - it reports actual test failures.

    Execution Modes:
        - Synchronous (default): Runs pytest and waits for completion
        - Asynchronous: Returns immediately with pending status

    Example:
        >>> agent = TestExecutionAgent(Path("/workspace"))
        >>> result = agent.analyze(
        ...     item_id="T1",
        ...     timeout_ms=60000
        ... )
        >>> for issue in result.issues:
        ...     print(f"{issue.title}: {issue.description}")
    """

    agent_type = AgentType.TEST_EXECUTION

    def __init__(
        self,
        working_dir: Path,
        llm_config: dict[str, Any] | None = None,
        log_event: Callable[..., None] | None = None,
        async_mode: bool = False,
        pytest_args: list[str] | None = None,
    ) -> None:
        """Initialize test execution agent.

        Args:
            working_dir: Working directory containing tests
            llm_config: Optional LLM configuration dict (unused - test execution doesn't need LLM)
            log_event: Optional callback for event logging
            async_mode: If True, returns immediately with pending status
            pytest_args: Custom pytest arguments (default: ["tests/", "-v", "--tb=short"])

        Note:
            This agent doesn't use LLM (it runs pytest directly), so llm_config is
            ignored. Parameter exists to match BaseAgent signature for registry compatibility.
        """
        super().__init__(working_dir, llm_config=llm_config, log_event=log_event)
        self._async_mode = async_mode
        self._pytest_args = pytest_args or ["tests/", "-v", "--tb=short"]

    def analyze(
        self,
        item_id: str,
        changed_files: list[str] | None = None,
        timeout_ms: int | None = None,
    ) -> AgentResult:
        """Execute pytest tests and report failures.

        Parameter Contracts (ADR-042):
            item_id: MUST be non-empty string. Typically matches [A-Z]+-[0-9]+ format.
            changed_files: If None, runs all tests.
                          If provided, runs tests for specified files.
            timeout_ms: If None, uses config-based timeout.
                       If provided, MUST be positive integer.

        Args:
            item_id: Plan item ID being reviewed
            changed_files: List of files that changed (unused - runs all tests)
            timeout_ms: Maximum execution time (None = use config default)

        Returns:
            AgentResult with test failure issues
        """
        # Resolve timeout from config if not provided
        timeout_ms = self._resolve_timeout_ms(timeout_ms)

        # Validate parameters (ADR-042)
        self._validate_analyze_params(item_id, timeout_ms)

        start_time = time.time()
        logger.info(f"TestExecutionAgent analyzing {item_id}")

        # Async mode: return immediately with pending status
        if self._async_mode:
            logger.info("TestExecutionAgent running in async mode (returning pending)")
            return AgentResult(
                agent_type=self.agent_type,
                status="pending",
                issues=[],
                scores={},
                execution_time_ms=0,
                metadata={
                    "mode": "async",
                    "item_id": item_id,
                },
            )

        # Synchronous mode: run pytest and wait
        return self._execute_pytest_sync(item_id, start_time, timeout_ms)

    def _execute_pytest_sync(
        self,
        item_id: str,
        start_time: float,
        timeout_ms: int,
    ) -> AgentResult:
        """Execute pytest synchronously and parse results.

        Args:
            item_id: Plan item ID
            start_time: Analysis start time
            timeout_ms: Maximum execution time in milliseconds

        Returns:
            AgentResult with issues from test failures
        """
        pytest_args = self._pytest_args
        timeout_s = timeout_ms / 1000

        logger.info(f"Running pytest with args: {pytest_args}")
        logger.debug(f"Timeout: {timeout_s}s")

        try:
            # Execute pytest
            # MONITORING EXEMPTION: Test execution with explicit timeout
            result = subprocess.run(
                ["pytest", *pytest_args],
                cwd=self._working_dir,
                capture_output=True,
                text=True,
                timeout=timeout_s,
            )

            execution_time = int((time.time() - start_time) * 1000)

            # Parse pytest output for failures
            issues = self._parse_pytest_output(result.stdout, result.stderr)

            # Success if no failures
            if result.returncode == 0:
                logger.info(f"All tests passed ({execution_time}ms)")
                return AgentResult(
                    agent_type=self.agent_type,
                    status="complete",
                    issues=[],
                    scores={"tests_passed": 1.0},
                    execution_time_ms=execution_time,
                    metadata={
                        "mode": "sync",
                        "exit_code": 0,
                        "tests_passed": True,
                    },
                )

            # Tests failed - return issues
            logger.info(f"Found {len(issues)} test failures ({execution_time}ms)")
            return AgentResult(
                agent_type=self.agent_type,
                status="complete",
                issues=issues,
                scores={"tests_passed": 0.0},
                execution_time_ms=execution_time,
                metadata={
                    "mode": "sync",
                    "exit_code": result.returncode,
                    "tests_passed": False,
                    "failure_count": len(issues),
                },
            )

        except subprocess.TimeoutExpired:
            execution_time = int((time.time() - start_time) * 1000)
            logger.warning(f"Pytest timed out after {timeout_s}s")
            return AgentResult(
                agent_type=self.agent_type,
                status="timeout",
                issues=[],
                scores={},
                execution_time_ms=execution_time,
                error="Pytest execution timed out",
                metadata={
                    "mode": "sync",
                    "timeout_ms": timeout_ms,
                },
            )

        except FileNotFoundError:
            execution_time = int((time.time() - start_time) * 1000)
            logger.error("pytest command not found")
            return AgentResult(
                agent_type=self.agent_type,
                status="error",
                issues=[],
                scores={},
                execution_time_ms=execution_time,
                error="pytest command not found in PATH",
                metadata={
                    "mode": "sync",
                },
            )

        except Exception as e:
            execution_time = int((time.time() - start_time) * 1000)
            logger.exception(f"Pytest execution failed: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                status="error",
                issues=[],
                scores={},
                execution_time_ms=execution_time,
                error=f"Pytest execution failed: {e}",
                metadata={
                    "mode": "sync",
                },
            )

    def _parse_pytest_output(self, stdout: str, stderr: str) -> list[AgentIssue]:
        """Parse pytest output to extract test failures.

        Parses pytest verbose output format to extract:
        - Test name (file::class::method or file::function)
        - Error message
        - File path and line number

        Args:
            stdout: Pytest stdout output
            stderr: Pytest stderr output

        Returns:
            List of AgentIssue objects for each failed test
        """
        issues: list[AgentIssue] = []

        # Combine stdout and stderr for parsing
        full_output = stdout + "\n" + stderr

        # Pattern for pytest failure lines: "FAILED tests/test_foo.py::test_bar - AssertionError: ..."
        # Also handles: "FAILED tests/test_foo.py::TestClass::test_method - ..."
        # Capture file path (stop at first ::), then everything until " - ", then error message
        failure_pattern = re.compile(
            r"FAILED\s+([^:]+\.\w+)::(.*?)\s+-\s+(.+?)(?=\nFAILED|\n={3,}|$)",
            re.DOTALL,
        )

        matches = failure_pattern.findall(full_output)
        for idx, (file_path, test_name, error_msg) in enumerate(matches):
            # Clean up error message (remove leading/trailing whitespace)
            error_msg = error_msg.strip()

            # Extract just the error summary (first line usually)
            error_summary = error_msg.split("\n")[0][:200]

            issues.append(
                AgentIssue(
                    id=self._generate_issue_id("TEST", idx + 1),
                    title=f"Test failure: {test_name}",
                    description=f"Test {test_name} failed with:\n{error_summary}",
                    priority=Priority.P1,  # Test failures are high priority
                    file_path=file_path,
                    line_number=None,  # pytest doesn't always include line numbers
                    dimension="test_execution",
                    suggestion=f"Fix the failing test in {file_path}::{test_name}",
                    metadata={
                        "test_name": test_name,
                        "full_error": error_msg[:1000],  # Truncate for storage
                    },
                )
            )

        return issues


__all__ = ["TestExecutionAgent"]
