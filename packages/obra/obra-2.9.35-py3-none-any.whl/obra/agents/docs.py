"""Documentation review agent for documentation quality analysis.

This module provides DocsAgent, which analyzes code for documentation
quality, including docstring coverage, README completeness, and API
documentation using LLM-powered semantic analysis.

Checks Performed:
    - Module/file documentation presence
    - Function/class docstring coverage
    - Parameter and return documentation
    - README file presence and completeness
    - API documentation quality
    - Test result verification (when test results provided)

Scoring Dimensions:
    - docstring_coverage: Percentage of public items with documentation
    - readme_complete: README file presence and completeness
    - api_documented: Public API documentation quality

Test Result Verification:
    - When test_results parameter is provided, DocsAgent verifies
      documentation claims against actual test execution results
    - No test results -> test_status: "unknown"
    - Test failures -> test_status: "failed" with failure count
    - All tests pass -> test_status: "passed"

Related:
    - obra/agents/base.py
    - obra/agents/registry.py
    - obra/agents/prompts/docs_analysis.txt
    - obra/agents/test_execution.py
"""

import logging
import time
from pathlib import Path

from obra.agents.base import AgentIssue, AgentResult, BaseAgent
from obra.agents.registry import register_agent
from obra.agents.tier_config import load_agent_tier_config
from obra.api.protocol import AgentType, Priority
from obra.config.llm import resolve_tier_config

logger = logging.getLogger(__name__)

# Prompt template directory
PROMPTS_DIR = Path(__file__).parent / "prompts"


def _load_prompt_template(name: str) -> str:
    """Load a prompt template from the prompts directory.

    Args:
        name: Template filename (e.g., "docs_analysis.txt")

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template doesn't exist
    """
    template_path = PROMPTS_DIR / name
    return template_path.read_text(encoding="utf-8")


# Required sections for a complete README (with alternative phrasings)
# Each entry is a tuple of (canonical_name, list_of_patterns)
README_REQUIRED_SECTIONS = [
    (
        "installation",
        [
            "install",
            "installation",
            "installing",
            "setup",
            "getting started",
            "quick start",
            "quickstart",
        ],
    ),
    ("usage", ["usage", "how to use", "using", "basic usage", "example", "examples"]),
]

README_OPTIONAL_SECTIONS = [
    ("contributing", ["contributing", "contribute", "development", "how to contribute"]),
    ("license", ["license", "licensing"]),
    ("requirements", ["requirements", "prerequisites", "dependencies", "deps"]),
    ("features", ["features", "capabilities", "what it does"]),
    ("api", ["api", "api reference", "reference", "documentation", "docs"]),
]


@register_agent(AgentType.DOCS)
class DocsAgent(BaseAgent):
    """Documentation review agent with LLM-powered analysis.

    Uses LLM-based analysis for comprehensive documentation quality review.
    Works with any programming language (Python, JavaScript, Go, etc.).

    When no LLM config is provided, returns empty result with warning.

    Test Result Verification:
        Pass test_results from TestExecutionAgent to verify documentation
        claims against actual test execution. The agent will include
        test_status in metadata:
        - "unknown": No test results provided
        - "passed": All tests passed
        - "failed": Some tests failed (includes failure_count)

    Example:
        >>> agent = DocsAgent(Path("/workspace"), llm_config=llm_config)
        >>> result = agent.analyze(
        ...     item_id="T1",
        ...     changed_files=["src/auth.py"],
        ...     timeout_ms=60000
        ... )
        >>> print(f"Docstring coverage: {result.scores['docstring_coverage']}")
        >>> print(f"Test status: {result.metadata.get('test_status')}")
    """

    agent_type = AgentType.DOCS

    def __init__(
        self,
        working_dir: Path,
        llm_config=None,
        log_event=None,
        test_results: AgentResult | None = None,
    ) -> None:
        """Initialize documentation review agent.

        Args:
            working_dir: Working directory containing code to analyze
            llm_config: Optional LLM configuration dict for CLI-based analysis
            log_event: Optional callback for event logging
            test_results: Optional test execution results from TestExecutionAgent.
                         When provided, DocsAgent verifies documentation claims
                         against actual test outcomes.
        """
        super().__init__(working_dir, llm_config=llm_config, log_event=log_event)
        self._test_results = test_results

    def get_test_status(self) -> dict[str, str | int]:
        """Query test execution status from provided test results.

        Returns a dictionary with test status information based on
        TestExecutionAgent results:
        - No results: {"status": "unknown"}
        - Failures: {"status": "failed", "failure_count": N}
        - All pass: {"status": "passed"}

        Returns:
            Dictionary with test status and optional failure count
        """
        if self._test_results is None:
            return {"status": "unknown"}

        # Check if test results are from TEST_EXECUTION agent type
        if self._test_results.agent_type != AgentType.TEST_EXECUTION:
            logger.warning(
                f"Test results are from {self._test_results.agent_type.value}, "
                "expected TEST_EXECUTION"
            )
            return {"status": "unknown"}

        # Check test execution status
        if self._test_results.status != "complete":
            # Test execution didn't complete (timeout, error, pending)
            return {"status": "unknown", "reason": self._test_results.status}

        # Check for test failures
        metadata = self._test_results.metadata or {}
        if metadata.get("tests_passed") is True:
            return {"status": "passed"}

        # Tests failed - count failures
        failure_count = metadata.get("failure_count", len(self._test_results.issues))
        return {"status": "failed", "failure_count": failure_count}

    def _build_test_verification_metadata(self) -> dict[str, str | int]:
        """Build test verification metadata for result.

        Returns metadata dict with test_status and optionally failure_count.
        This metadata is included in all successful DocsAgent results to
        inform downstream consumers about test verification status.

        Returns:
            Dictionary with test verification fields
        """
        test_status = self.get_test_status()

        result: dict[str, str | int] = {"test_status": test_status["status"]}

        # Include failure count if tests failed
        if test_status["status"] == "failed" and "failure_count" in test_status:
            result["test_failure_count"] = test_status["failure_count"]

        # Include reason if test status is unknown due to incomplete execution
        if test_status["status"] == "unknown" and "reason" in test_status:
            result["test_status_reason"] = test_status["reason"]

        return result

    def analyze(
        self,
        item_id: str,
        changed_files: list[str] | None = None,
        timeout_ms: int | None = None,
    ) -> AgentResult:
        """Analyze code for documentation quality.

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
            AgentResult with documentation issues and scores
        """
        # Resolve timeout from config if not provided
        timeout_ms = self._resolve_timeout_ms(timeout_ms)

        # Validate parameters (ADR-042)
        self._validate_analyze_params(item_id, timeout_ms)

        start_time = time.time()
        logger.info(f"DocsAgent analyzing {item_id}")

        # Get files to analyze - use blocklist approach for language-agnostic analysis
        files = self.get_files_to_analyze(changed_files=changed_files)
        logger.debug(f"Analyzing {len(files)} files for documentation")

        # Use LLM-based analysis if config is available
        if self._llm_config:
            return self._analyze_with_llm(
                item_id=item_id,
                files=files,
                start_time=start_time,
                timeout_ms=timeout_ms,
            )

        # Fallback: No config available, return empty result with warning
        logger.warning("DocsAgent: No LLM config available, skipping analysis")
        execution_time = int((time.time() - start_time) * 1000)

        # Build metadata with test verification
        metadata: dict[str, str | int] = {
            "files_analyzed": 0,
            "mode": "no_invoker",
        }
        metadata.update(self._build_test_verification_metadata())

        return AgentResult(
            agent_type=self.agent_type,
            status="complete",
            issues=[],
            scores={
                "docstring_coverage": 1.0,
                "readme_complete": 1.0,
                "api_documented": 1.0,
            },
            execution_time_ms=execution_time,
            metadata=metadata,
        )

    def _analyze_with_llm(
        self,
        item_id: str,
        files: list[Path],
        start_time: float,
        timeout_ms: int,
    ) -> AgentResult:
        """Perform LLM-based documentation analysis.

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
        tier_config = load_agent_tier_config("docs")
        start_tier = tier_config.get("start_tier", "fast")

        # Load prompt template
        try:
            docs_template = _load_prompt_template("docs_analysis.txt")
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

        # Check README (quick, non-LLM based)
        readme_issues, readme_score = self._check_readme(deadline)
        all_issues.extend(readme_issues)

        # Collect file contents for analysis with diagnostic counters
        files_content: dict[str, str] = {}
        excluded_count = 0
        test_file_count = 0
        init_file_count = 0
        read_fail_count = 0
        timeout_during_collection = False

        for file_path in files:
            if time.time() > deadline:
                logger.warning("DocsAgent timed out during file collection")
                timeout_during_collection = True
                break

            # Skip test files, __init__.py, and infrastructure files
            if self.is_test_file(file_path):
                test_file_count += 1
                continue
            if file_path.name == "__init__.py":
                init_file_count += 1
                continue
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
            # No files to analyze with LLM, but README may have issues
            # Use "skipped" if no README issues either, "complete" if README was analyzed
            has_readme_findings = len(all_issues) > 0
            status = "complete" if has_readme_findings else "skipped"

            if not has_readme_findings:
                logger.warning(
                    "DocsAgent: No analyzable files and no README findings. "
                    "working_dir=%s, files_scanned=%d, test_files=%d, init_files=%d, "
                    "excluded=%d, read_failed=%d, timeout=%s",
                    self._working_dir,
                    len(files),
                    test_file_count,
                    init_file_count,
                    excluded_count,
                    read_fail_count,
                    timeout_during_collection,
                )
            else:
                logger.info(
                    "DocsAgent: No files for LLM analysis, but README check found %d issues.",
                    len(all_issues),
                )

            execution_time = int((time.time() - start_time) * 1000)

            # Build metadata with test verification and diagnostic info
            metadata: dict[str, str | int | bool] = {
                "files_analyzed": 0,
                "mode": "llm",
                "skip_reason": "no_files_after_filter",
                "readme_checked": True,
                "readme_findings": len(all_issues),
                "working_dir": str(self._working_dir),
                "files_scanned": len(files),
                "files_test": test_file_count,
                "files_init": init_file_count,
                "files_excluded": excluded_count,
                "files_read_failed": read_fail_count,
                "timeout_during_collection": timeout_during_collection,
            }
            metadata.update(self._build_test_verification_metadata())

            return AgentResult(
                agent_type=self.agent_type,
                status=status,
                issues=all_issues,
                scores={
                    "docstring_coverage": 1.0,
                    "readme_complete": readme_score,
                    "api_documented": 1.0,
                },
                execution_time_ms=execution_time,
                metadata=metadata,
            )

        # Format code content for prompt
        code_content = self._format_code_for_prompt(files_content)

        # Run LLM analysis
        logger.info(f"Running docs analysis with {llm_config['provider']}/{llm_config['model']}")
        analysis_prompt = docs_template.format(code_content=code_content)

        try:
            response_text = self._invoke_cli(
                call_site="docs_analysis",
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
            issues = self.parse_structured_response(response_text, prefix="DOC")
            all_issues.extend(issues)
            logger.info(f"Found {len(issues)} documentation issues from LLM")

        except Exception as e:
            logger.exception(f"Documentation analysis failed: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                status="error",
                error=f"Analysis failed: {e}",
                execution_time_ms=int((time.time() - start_time) * 1000),
            )

        # Calculate scores based on findings
        scores = self._calculate_scores_from_issues(all_issues, readme_score)

        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"DocsAgent complete: {len(all_issues)} issues found in {execution_time}ms")

        # Build metadata with test verification
        metadata: dict = {
            "files_analyzed": len(files_content),
            "mode": "llm",
            "provider": llm_config["provider"],
            "model": llm_config["model"],
            # Observability fields (ADR-043)
            "issues_found": len(all_issues),
            "scores": scores,
        }
        metadata.update(self._build_test_verification_metadata())

        return AgentResult(
            agent_type=self.agent_type,
            status="complete",
            issues=all_issues,
            scores=scores,
            execution_time_ms=execution_time,
            metadata=metadata,
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

    def _check_readme(
        self,
        deadline: float,
    ) -> tuple[list[AgentIssue], float]:
        """Check README file presence and completeness.

        Args:
            deadline: Timeout deadline

        Returns:
            Tuple of (issues, score)
        """
        issues: list[AgentIssue] = []
        issue_index = 0

        # Look for README
        readme_files = list(self._working_dir.glob("README*"))
        if not readme_files:
            issues.append(
                AgentIssue(
                    id=self._generate_issue_id("DOC", issue_index + 1),
                    title="Missing README file",
                    description="Project should have a README.md file with installation and usage instructions.",
                    priority=Priority.P1,
                    dimension="readme_complete",
                    suggestion="Create README.md with project description, installation, and usage sections",
                )
            )
            return issues, 0.0

        readme_files_sorted = sorted(
            readme_files,
            key=lambda path: (path.name.lower() != "readme.md", path.name.lower()),
        )
        readme_path = readme_files_sorted[0]
        content = self.read_file(readme_path).lower()

        # Check required sections using fuzzy matching
        found_sections: set[str] = set()
        for section_name, patterns in README_REQUIRED_SECTIONS:
            for pattern in patterns:
                if pattern in content:
                    found_sections.add(section_name)
                    break

        # Find missing required sections
        required_section_names = {name for name, _ in README_REQUIRED_SECTIONS}
        missing_sections = required_section_names - found_sections
        for section in missing_sections:
            issue_index += 1
            issues.append(
                AgentIssue(
                    id=self._generate_issue_id("DOC", issue_index),
                    title=f"README missing '{section}' section",
                    description=f"README should include a '{section}' section.",
                    priority=Priority.P2,
                    file_path="README.md",
                    dimension="readme_complete",
                    suggestion=f"Add a '{section}' section to README.md",
                )
            )

        # Calculate score
        required_found = len(found_sections)
        required_total = len(README_REQUIRED_SECTIONS)

        # Check optional sections for bonus using fuzzy matching
        optional_found = 0
        for _, patterns in README_OPTIONAL_SECTIONS:
            if any(pattern in content for pattern in patterns):
                optional_found += 1
        optional_bonus = min(optional_found / len(README_OPTIONAL_SECTIONS) * 0.2, 0.2)

        score = (required_found / required_total * 0.8) + optional_bonus

        return issues, score

    def _calculate_scores_from_issues(
        self,
        issues: list[AgentIssue],
        readme_score: float,
    ) -> dict[str, float]:
        """Calculate dimension scores based on issues.

        Args:
            issues: All issues found
            readme_score: README completeness score from _check_readme

        Returns:
            Dict of dimension scores
        """
        docstring_issues = 0
        api_issues = 0

        for issue in issues:
            dim = issue.dimension
            if dim == "docstring_coverage":
                docstring_issues += 1
            elif dim == "api_documented":
                api_issues += 1
            elif dim == "readme_complete":
                # README issues counted via readme_score
                pass
            else:
                # Map priority to dimension for LLM issues without explicit dimension
                if issue.priority in (Priority.P0, Priority.P1):
                    docstring_issues += 1
                else:
                    api_issues += 1

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
            "docstring_coverage": score(docstring_issues),
            "readme_complete": round(readme_score, 2),
            "api_documented": score(api_issues),
        }


__all__ = ["DocsAgent"]
