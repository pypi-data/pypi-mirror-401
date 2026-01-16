"""Testing review agent for test coverage analysis.

This module provides TestingAgent, which analyzes code for testing
quality, coverage gaps, and testing best practices using LLM-powered
semantic analysis.

Checks Performed:
    - Test file presence for source files
    - Test function coverage
    - Edge case handling
    - Mock usage patterns
    - Assertion quality
    - Test isolation

Scoring Dimensions:
    - test_coverage: Presence of tests for source files
    - test_quality: Quality of test assertions and patterns
    - edge_cases: Coverage of edge cases and error paths

Related:
    - obra/agents/base.py
    - obra/agents/registry.py
    - obra/agents/prompts/testing_coverage.txt
"""

import logging
import time
from pathlib import Path

from obra.agents.base import AgentIssue, AgentResult, BaseAgent
from obra.agents.prompts import load_prompt
from obra.agents.registry import register_agent
from obra.agents.tier_config import load_agent_tier_config
from obra.api.protocol import AgentType, Priority
from obra.config.llm import resolve_tier_config

logger = logging.getLogger(__name__)


@register_agent(AgentType.TESTING)
class TestingAgent(BaseAgent):
    """Testing review agent with LLM-powered coverage analysis.

    Uses LLM-based analysis for comprehensive test coverage review.
    Works with any programming language (Python, JavaScript, Go, etc.).

    When no LLM config is provided, returns empty result with warning.

    Example:
        >>> agent = TestingAgent(Path("/workspace"), llm_config=llm_config)
        >>> result = agent.analyze(
        ...     item_id="T1",
        ...     changed_files=["src/auth.py"],
        ...     timeout_ms=60000
        ... )
        >>> print(f"Test coverage score: {result.scores['test_coverage']}")
    """

    agent_type = AgentType.TESTING

    def analyze(
        self,
        item_id: str,
        changed_files: list[str] | None = None,
        timeout_ms: int | None = None,
    ) -> AgentResult:
        """Analyze code for testing quality and coverage gaps.

        Uses LLM-based analysis when invoker is available. Analyzes
        any programming language, not just Python.

        Parameter Contracts (ADR-042):
            item_id: MUST be non-empty string. Typically matches [A-Z]+-[0-9]+ format.
            changed_files: If None, analyzes all files in working_dir.
                          If provided, only analyzes specified files.
                          Uses blocklist approach to analyze all code files.
            timeout_ms: If None, uses config-based timeout via get_review_agent_timeout().
                       If provided, MUST be positive integer. Typical range: [5000-300000].

        Args:
            item_id: Plan item ID being reviewed
            changed_files: List of files that changed
            timeout_ms: Maximum execution time (None = use config default)

        Returns:
            AgentResult with testing issues and scores
        """
        # Resolve timeout from config if not provided
        timeout_ms = self._resolve_timeout_ms(timeout_ms)

        # Validate parameters (ADR-042)
        self._validate_analyze_params(item_id, timeout_ms)

        start_time = time.time()
        logger.info(f"TestingAgent analyzing {item_id}")

        # Get files to analyze - use blocklist approach for language-agnostic analysis
        files = self.get_files_to_analyze(changed_files=changed_files)
        logger.debug(f"Analyzing {len(files)} files for test coverage")

        # Use LLM-based analysis if config is available
        if self._llm_config:
            return self._analyze_with_llm(
                item_id=item_id,
                files=files,
                start_time=start_time,
                timeout_ms=timeout_ms,
            )

        # Fallback: No config available, return empty result with warning
        logger.warning("TestingAgent: No LLM config available, skipping analysis")
        execution_time = int((time.time() - start_time) * 1000)
        return AgentResult(
            agent_type=self.agent_type,
            status="complete",
            issues=[],
            scores={
                "test_coverage": 1.0,
                "test_quality": 1.0,
                "edge_cases": 1.0,
            },
            execution_time_ms=execution_time,
            metadata={
                "files_analyzed": 0,
                "mode": "no_invoker",
            },
        )

    def _analyze_with_llm(
        self,
        item_id: str,
        files: list[Path],
        start_time: float,
        timeout_ms: int,
    ) -> AgentResult:
        """Perform LLM-based test coverage analysis.

        Args:
            item_id: Plan item ID
            files: List of files to analyze
            start_time: Analysis start time
            timeout_ms: Maximum execution time

        Returns:
            AgentResult with issues from LLM analysis
        """
        deadline = start_time + (timeout_ms / 1000)
        all_issues: list[AgentIssue] = []

        # Load tier configuration
        tier_config = load_agent_tier_config("testing")
        start_tier = tier_config.get("start_tier", "fast")

        # Load prompt template (ISSUE-009: Use centralized loader)
        try:
            coverage_template = load_prompt("testing_coverage")
        except FileNotFoundError as e:
            logger.error(f"Failed to load prompt template: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                status="error",
                error=f"Missing prompt template: {e}",
                execution_time_ms=int((time.time() - start_time) * 1000),
            )

        # Resolve LLM config
        llm_config = resolve_tier_config(start_tier, role="implementation")

        # Collect file contents for analysis with diagnostic counters
        files_content: dict[str, str] = {}
        excluded_count = 0
        read_fail_count = 0
        timeout_during_collection = False

        for file_path in files:
            if time.time() > deadline:
                logger.warning("TestingAgent timed out during file collection")
                timeout_during_collection = True
                break

            if self.is_excluded_file(file_path):
                excluded_count += 1
                continue

            content = self.read_file(file_path)
            if content:
                try:
                    rel_path = str(file_path.relative_to(self._working_dir))
                except ValueError:
                    rel_path = str(file_path)
                files_content[rel_path] = content
            else:
                read_fail_count += 1

        if not files_content:
            logger.warning(
                "TestingAgent: No analyzable files. "
                "working_dir=%s, files_scanned=%d, excluded=%d, read_failed=%d, timeout=%s",
                self._working_dir,
                len(files),
                excluded_count,
                read_fail_count,
                timeout_during_collection,
            )
            execution_time = int((time.time() - start_time) * 1000)
            return AgentResult(
                agent_type=self.agent_type,
                status="skipped",  # Not "complete" - no analysis was performed
                issues=[],
                scores={
                    "test_coverage": 1.0,
                    "test_quality": 1.0,
                    "edge_cases": 1.0,
                },
                execution_time_ms=execution_time,
                metadata={
                    "files_analyzed": 0,
                    "mode": "llm",
                    "skip_reason": "no_files_after_filter",
                    "working_dir": str(self._working_dir),
                    "files_scanned": len(files),
                    "files_excluded": excluded_count,
                    "files_read_failed": read_fail_count,
                    "timeout_during_collection": timeout_during_collection,
                },
            )

        # Format code content for prompt
        code_content = self._format_code_for_prompt(files_content)

        # Run LLM analysis
        logger.info(f"Running test coverage analysis with {llm_config['provider']}/{llm_config['model']}")
        analysis_prompt = coverage_template.format(code_content=code_content)

        try:
            response_text = self._invoke_cli(
                call_site="testing_analysis",
                prompt=analysis_prompt,
                timeout_ms=timeout_ms,
            )

            if not response_text:
                logger.warning("LLM invocation returned empty response")
                return AgentResult(
                    agent_type=self.agent_type,
                    status="error",
                    error="LLM invocation returned empty response",
                    execution_time_ms=int((time.time() - start_time) * 1000),
                )

            # Parse results
            issues = self.parse_structured_response(response_text, prefix="TEST")
            all_issues.extend(issues)
            logger.info(f"Found {len(issues)} test coverage issues")

        except Exception as e:
            logger.exception(f"Test coverage analysis failed: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                status="error",
                error=f"Analysis failed: {e}",
                execution_time_ms=int((time.time() - start_time) * 1000),
            )

        # Calculate scores based on findings
        scores = self._calculate_scores_from_issues(all_issues)

        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"TestingAgent complete: {len(all_issues)} issues found in {execution_time}ms")

        return AgentResult(
            agent_type=self.agent_type,
            status="complete",
            issues=all_issues,
            scores=scores,
            execution_time_ms=execution_time,
            metadata={
                "files_analyzed": len(files_content),
                "mode": "llm",
                "provider": llm_config["provider"],
                "model": llm_config["model"],
                # Observability fields (ADR-043)
                "issues_found": len(all_issues),
                "scores": scores,
            },
        )

    def _format_code_for_prompt(self, files_content: dict[str, str]) -> str:
        """Format file contents for LLM prompt.

        Args:
            files_content: Dict mapping file paths to contents

        Returns:
            Formatted string with file headers
        """
        parts = []
        for file_path, content in files_content.items():
            # Limit content size to avoid token limits
            if len(content) > 50000:
                content = content[:50000] + "\n... (truncated)"
            numbered = "\n".join(
                f"{line_no:>4}: {line}"
                for line_no, line in enumerate(content.splitlines(), start=1)
            )
            parts.append(f"=== FILE: {file_path} ===\n{numbered}")
        return "\n\n".join(parts)

    def _calculate_scores_from_issues(self, issues: list[AgentIssue]) -> dict[str, float]:
        """Calculate dimension scores based on issues.

        Args:
            issues: All issues found

        Returns:
            Dict of dimension scores
        """
        coverage_issues = 0
        quality_issues = 0
        edge_case_issues = 0

        for issue in issues:
            dim = issue.dimension
            if dim == "test_coverage":
                coverage_issues += 1
            elif dim == "test_quality":
                quality_issues += 1
            elif dim == "edge_cases":
                edge_case_issues += 1
            else:
                # Map priority to dimension for LLM issues without explicit dimension
                if issue.priority in (Priority.P0, Priority.P1):
                    coverage_issues += 1
                else:
                    edge_case_issues += 1

        def score(issue_count: int) -> float:
            if issue_count == 0:
                return 1.0
            if issue_count == 1:
                return 0.8
            if issue_count == 2:
                return 0.6
            if issue_count <= 5:
                return 0.4
            return 0.2

        return {
            "test_coverage": score(coverage_issues),
            "test_quality": score(quality_issues),
            "edge_cases": score(edge_case_issues),
        }


__all__ = ["TestingAgent"]
