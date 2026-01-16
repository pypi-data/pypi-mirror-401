"""Base class and types for review agents.

This module defines the BaseAgent abstract class and AgentResult dataclass
that all review agents must implement.

Agent Architecture:
    - Agents are lightweight, stateless workers
    - Each agent runs as a subprocess for isolation
    - Agents analyze code and return structured results
    - Results include issues (with priority) and dimension scores

Related:
    - obra/agents/deployer.py
    - obra/api/protocol.py
"""

import logging
import subprocess
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from obra.api.protocol import AgentType, Priority
from obra.config import build_llm_args, build_subprocess_env, get_llm_cli, get_review_agent_timeout
from obra.hybrid.json_utils import extract_usage_from_cli_response

logger = logging.getLogger(__name__)


# Files that should be excluded from most agent analysis
# These are infrastructure/config files, not application code
EXCLUDED_FILES = {
    # Pytest infrastructure
    "conftest.py",
    # Build/packaging
    "setup.py",
    "setup.cfg",
    "pyproject.toml",
    # Noxfile/tox
    "noxfile.py",
    "toxfile.py",
    # Type stubs
    "py.typed",
}

# Patterns for files that should be excluded (checked with fnmatch)
EXCLUDED_PATTERNS = [
    # Migration files
    "**/migrations/*.py",
    "**/alembic/versions/*.py",
    # Auto-generated
    "**/*_pb2.py",  # protobuf
    "**/*_pb2_grpc.py",
]

# Binary and generated file extensions that should be excluded from analysis.
# These are not source code and cannot be meaningfully analyzed by review agents.
# Use blocklist approach: exclude known binary types, allow all other files.
BINARY_EXTENSIONS: frozenset[str] = frozenset({
    # Python bytecode/packaging
    ".pyc",
    ".pyo",
    ".pyd",
    ".egg",
    ".whl",
    # Coverage/testing artifacts
    ".coverage",
    # Compiled binaries
    ".exe",
    ".dll",
    ".so",
    ".dylib",
    ".o",
    ".a",
    ".lib",
    # Archives
    ".tar",
    ".gz",
    ".zip",
    ".rar",
    ".7z",
    ".bz2",
    ".xz",
    # Images
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ico",
    ".bmp",
    ".svg",
    ".webp",
    # Fonts
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
    ".eot",
    # Media
    ".mp3",
    ".mp4",
    ".wav",
    ".avi",
    ".mov",
    ".webm",
    # Documents (binary)
    ".pdf",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
    ".ppt",
    ".pptx",
    # Database
    ".db",
    ".sqlite",
    ".sqlite3",
    # Lock files (not useful to analyze)
    ".lock",
    # Minified files (not readable)
    ".min.js",
    ".min.css",
})


@dataclass
class AgentIssue:
    """Issue found by a review agent.

    Attributes:
        id: Unique issue identifier
        title: Short description of the issue
        description: Detailed description
        priority: Issue priority (P0-P3)
        file_path: File where issue was found (if applicable)
        line_number: Line number (if applicable)
        dimension: Quality dimension (security, testing, docs, maintainability)
        suggestion: Suggested fix
        metadata: Additional metadata
    """

    id: str
    title: str
    description: str
    priority: Priority
    file_path: str | None = None
    line_number: int | None = None
    dimension: str = ""
    suggestion: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.value,
            "file_path": self.file_path,
            "line_number": self.line_number,
            "dimension": self.dimension,
            "suggestion": self.suggestion,
            "metadata": self.metadata,
        }


@dataclass
class AgentResult:
    """Result from agent execution.

    Attributes:
        agent_type: Type of agent that produced this result
        status: Execution status (complete, timeout, error)
        issues: List of issues found
        scores: Dimension scores (0.0 - 1.0)
        execution_time_ms: Time taken in milliseconds
        error: Error message if status is error
        metadata: Additional metadata
    """

    agent_type: AgentType
    status: str  # complete, timeout, error
    issues: list[AgentIssue] = field(default_factory=list)
    scores: dict[str, float] = field(default_factory=dict)
    execution_time_ms: int = 0
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API serialization."""
        return {
            "agent_type": self.agent_type.value,
            "status": self.status,
            "issues": [issue.to_dict() for issue in self.issues],
            "scores": self.scores,
            "execution_time_ms": self.execution_time_ms,
            "error": self.error,
            "metadata": self.metadata,
        }


class BaseAgent(ABC):
    """Abstract base class for review agents.

    All review agents must implement this interface. Agents analyze code
    in a workspace and return structured results with issues and scores.

    Implementing a new agent:
        1. Subclass BaseAgent
        2. Implement analyze() method
        3. Register with AgentRegistry
        4. Add to obra/agents/__init__.py

    See also:
        docs/guides/parameter-validation-guide.md - Parameter validation patterns (ADR-042)

    Example:
        >>> class MyAgent(BaseAgent):
        ...     agent_type = AgentType.SECURITY
        ...
        ...     def analyze(self, item_id, changed_files, timeout_ms):
        ...         issues = self._check_for_issues(changed_files)
        ...         scores = self._calculate_scores(changed_files)
        ...         return AgentResult(
        ...             agent_type=self.agent_type,
        ...             status="complete",
        ...             issues=issues,
        ...             scores=scores
        ...         )
    """

    # Subclasses must set this
    agent_type: AgentType

    # Directories to ignore when scanning for files.
    # These are infrastructure/build directories that should not be analyzed.
    # Used by get_files_to_analyze() and should be used by any agent doing rglob().
    IGNORE_DIRS: frozenset[str] = frozenset({
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".coverage",
        "dist",
        "build",
        "eggs",
        "*.egg-info",
        ".eggs",
        "site-packages",
        ".nox",
        ".cache",
        "htmlcov",
    })

    def __init__(
        self,
        working_dir: Path,
        llm_config: dict[str, Any] | None = None,
        log_event: Callable[..., None] | None = None,
    ) -> None:
        """Initialize agent.

        Args:
            working_dir: Working directory containing code to analyze
            llm_config: Optional LLM configuration dict for CLI-based analysis.
                       If None, agent returns empty results (no analysis performed).
            log_event: Optional callback for event logging (observability)
        """
        self._working_dir = working_dir
        self._llm_config = llm_config
        self._log_event = log_event
        logger.debug(f"Initialized {self.__class__.__name__} for {working_dir}")

    @property
    def working_dir(self) -> Path:
        """Get working directory."""
        return self._working_dir

    def _invoke_cli(
        self,
        call_site: str,
        prompt: str,
        timeout_ms: int | None = None,
    ) -> str:
        """Invoke LLM via CLI subprocess for analysis.

        This method replaces _invoke_with_logging() and uses CLI subprocess
        invocation instead of LLMInvoker, following the execute handler pattern.

        Args:
            call_site: Identifier for where the LLM is being called from
                      (e.g., "security_tier1", "testing_analysis")
            prompt: The prompt to send to the LLM
            timeout_ms: Maximum execution time in milliseconds (None = use config default)

        Returns:
            Response text from the LLM

        Raises:
            subprocess.TimeoutExpired: If invocation exceeds timeout
            subprocess.CalledProcessError: If CLI invocation fails
            Exception: If invocation fails
        """
        if not self._llm_config:
            logger.warning(f"{call_site}: No LLM config available, returning empty response")
            return ""

        # Resolve timeout (convert ms to seconds for subprocess)
        timeout_s = (timeout_ms or (get_review_agent_timeout() * 1000)) / 1000

        # Build CLI command and args from llm_config
        provider = self._llm_config.get("provider", "anthropic")
        cli_command = get_llm_cli(provider)
        # Use mode="text" for review agents (--print with JSON output, no file writes)
        cli_args = build_llm_args(self._llm_config, mode="text")

        cmd = [cli_command, *cli_args]

        # GIT-HARD-001: Add --skip-git-repo-check for OpenAI Codex when configured
        git_config = self._llm_config.get("git", {})
        skip_git_check = git_config.get("skip_check", False)
        if skip_git_check and provider == "openai":
            cmd.append("--skip-git-repo-check")
            logger.debug(f"{call_site}: Adding --skip-git-repo-check for Codex")

        # Build subprocess environment with auth-aware API key handling
        auth_method = self._llm_config.get("auth_method", "oauth")
        env = build_subprocess_env(
            auth_method=auth_method,
            extra_env={"PYTHONIOENCODING": "utf-8:backslashreplace"},
        )

        logger.debug(f"{call_site}: Running CLI: {' '.join(cmd[:3])}...")

        import time

        start_time = time.time()

        try:
            # Execute subprocess with prompt via stdin
            result = subprocess.run(
                cmd,
                cwd=self._working_dir,
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="backslashreplace",
                timeout=timeout_s,
                env=env,
            )

            duration_ms = int((time.time() - start_time) * 1000)

            if result.returncode != 0:
                logger.error(
                    f"{call_site}: CLI invocation failed (exit code {result.returncode}): "
                    f"{result.stderr[:200]}"
                )
                return ""

            # Extract token usage from CLI response before processing
            usage = extract_usage_from_cli_response(result.stdout)
            total_tokens = usage["input_tokens"] + usage["output_tokens"]

            response_text = result.stdout.strip()

            # Display token usage to stdout (SIM-FIX-001 continuation)
            # Show tokens even in non-verbose mode so users can track consumption
            if total_tokens > 0:
                from obra.display import print_info

                input_tokens = usage["input_tokens"]
                output_tokens = usage["output_tokens"]
                source = "CLI" if (input_tokens > 0 or output_tokens > 0) else "estimated"
                print_info(
                    f"Agent tokens ({call_site}): {total_tokens:,} "
                    f"(in: {input_tokens:,}, out: {output_tokens:,}) [{source}]"
                )

            # Emit llm_call event if log_event callback is available
            if self._log_event:
                self._log_event(
                    "llm_call",
                    call_site=call_site,
                    provider=provider,
                    model=self._llm_config.get("model", "default"),
                    tokens_used=total_tokens,
                    thinking_tokens=0,
                    duration_ms=duration_ms,
                    success=True,
                )

            return response_text

        except subprocess.TimeoutExpired:
            logger.error(f"{call_site}: CLI invocation timed out after {timeout_s}s")
            return ""
        except Exception as e:
            logger.error(f"{call_site}: CLI invocation failed: {e}")
            return ""

    def _validate_analyze_params(
        self,
        item_id: str,
        timeout_ms: int,
    ) -> None:
        """Validate analyze() parameters (ADR-042 Contract 3).

        Agent implementations SHOULD call this at the start of their
        analyze() method to ensure parameter contracts are enforced.

        Args:
            item_id: Plan item ID to validate
            timeout_ms: Timeout value to validate

        Raises:
            ValueError: If item_id is empty or timeout_ms is invalid
        """
        if not item_id or not item_id.strip():
            msg = "item_id must be non-empty string"
            raise ValueError(msg)

        if timeout_ms <= 0:
            msg = f"timeout_ms must be positive, got {timeout_ms}"
            raise ValueError(msg)

    def _resolve_timeout_ms(self, timeout_ms: int | None) -> int:
        """Resolve timeout_ms to a concrete value.

        Uses config-based timeout from get_review_agent_timeout() if None provided.

        Args:
            timeout_ms: Explicit timeout in milliseconds, or None to use config default

        Returns:
            Timeout in milliseconds (config default converted from seconds if None was passed)
        """
        if timeout_ms is None:
            return get_review_agent_timeout() * 1000
        return timeout_ms

    def _is_ignored_path(self, path: Path) -> bool:
        """Check if a path should be ignored based on IGNORE_DIRS.

        Use this method when doing manual rglob() scans to ensure consistent
        filtering across all agents. Prevents scanning into virtual environments,
        node_modules, build directories, and other infrastructure paths.

        Only checks paths RELATIVE to working_dir. Parent directories outside
        the working directory do not affect filtering. This prevents incorrectly
        filtering all files when the working directory itself is named "build",
        ".cache", etc. (ISSUE-001).

        Args:
            path: Path to check (can be relative or absolute)

        Returns:
            True if any path component (relative to working_dir) matches an ignored directory name
        """
        try:
            # Only check relative path components within working_dir
            rel_path = path.relative_to(self._working_dir)
            return any(part in self.IGNORE_DIRS for part in rel_path.parts)
        except ValueError:
            # Path is outside working_dir, don't filter
            return False

    @abstractmethod
    def analyze(
        self,
        item_id: str,
        changed_files: list[str] | None = None,
        timeout_ms: int | None = None,
    ) -> AgentResult:
        """Analyze code and return results.

        This is the main entry point for agent execution. Agents should
        analyze the code in working_dir and return issues and scores.

        Parameter Contracts (ADR-042):
            item_id: MUST be non-empty string. Typically matches [A-Z]+-[0-9]+ format.
            changed_files: If None, analyzes all files in working_dir.
                          If empty list, returns empty result.
                          If non-empty, only analyzes specified files.
                          Files are passed to get_files_to_analyze() which respects
                          agent-specific extensions filtering.
            timeout_ms: If None, uses config-based timeout via get_review_agent_timeout().
                       If provided, MUST be positive integer. Typical range: [5000-300000].
                       Applies to entire analysis, not per-file.

        Parameter Interactions:
            - changed_files paths are resolved relative to working_dir
            - Extensions filtering (agent-specific) applies to changed_files
            - timeout_ms enforced by agent implementation (may vary)
            - When timeout_ms is None, resolved via orchestration.timeouts.review_agent_s config

        Args:
            item_id: Plan item ID being reviewed
            changed_files: List of files that changed (optional, for focused review)
            timeout_ms: Maximum execution time in milliseconds (None = use config default)

        Returns:
            AgentResult with issues and scores

        Raises:
            ValueError: If item_id is empty or timeout_ms <= 0
            TimeoutError: If analysis exceeds timeout_ms
            Exception: If analysis fails
        """

    def get_files_to_analyze(
        self,
        changed_files: list[str] | None = None,
        extensions: list[str] | None = None,
        exclude_binary: bool = True,
    ) -> list[Path]:
        """Get list of files to analyze.

        Parameter Contracts (ADR-042):
            changed_files: If None, scans entire working_dir recursively.
                          If provided, only these files are considered (scope constraint).
                          Paths can be relative or absolute.
                          Non-existent files are silently skipped.
            extensions: DEPRECATED - use exclude_binary instead.
                       If None, uses blocklist approach (exclude binary files).
                       If provided (e.g., [".py", ".js"]), uses allowlist approach.
                       MUST be applied in BOTH changed_files and directory scan paths.
            exclude_binary: If True (default), excludes binary/generated files using
                           BINARY_EXTENSIONS blocklist. This allows all code file types
                           (.py, .js, .go, .yaml, Dockerfile, etc.) while filtering out
                           non-analyzable files (.pyc, .png, .exe, etc.).
                           Ignored if extensions is provided (allowlist takes precedence).

        Parameter Interactions:
            - When changed_files provided: constrains scope to those files only
            - When extensions provided: uses allowlist (legacy behavior)
            - When exclude_binary=True (default): uses blocklist approach
            - Filtering is consistent across all code paths (ISSUE-CLI-013 fix)

        Args:
            changed_files: If provided, only analyze these files (scope constraint)
            extensions: DEPRECATED. If provided, filter by file extensions (allowlist)
            exclude_binary: If True, exclude binary files using blocklist (default: True)

        Returns:
            List of file paths to analyze (all paths are absolute Path objects)
        """
        if changed_files is not None:
            # Short-circuit: empty list means no files to analyze
            if not changed_files:
                return []

            # Filter to existing files
            files = []
            for f in changed_files:
                path = self._working_dir / f if not Path(f).is_absolute() else Path(f)
                if path.exists() and path.is_file():
                    # Allowlist takes precedence (legacy behavior)
                    if extensions is not None:
                        if path.suffix not in extensions:
                            continue
                    # Otherwise use blocklist if enabled
                    elif exclude_binary and self._is_binary_file(path):
                        continue
                    files.append(path)
            return files

        # Scan all files in working directory
        # Short-circuit: empty extensions list means nothing matches
        if extensions is not None and not extensions:
            return []

        files = []

        for path in self._working_dir.rglob("*"):
            # Skip ignored directories (uses class constant IGNORE_DIRS)
            if self._is_ignored_path(path):
                continue

            if not path.is_file():
                continue

            # Allowlist takes precedence (legacy behavior)
            if extensions is not None:
                if path.suffix not in extensions:
                    continue
            # Otherwise use blocklist if enabled
            elif exclude_binary and self._is_binary_file(path):
                continue

            files.append(path)

        return files

    def _is_binary_file(self, path: Path) -> bool:
        """Check if a file should be excluded as binary/generated.

        Uses BINARY_EXTENSIONS blocklist to identify files that cannot be
        meaningfully analyzed by review agents.

        Args:
            path: Path to check

        Returns:
            True if file should be excluded (is binary/generated)
        """
        # Check suffix against blocklist
        suffix = path.suffix.lower()
        if suffix in BINARY_EXTENSIONS:
            return True

        # Check for compound extensions like .min.js, .min.css
        name_lower = path.name.lower()
        if name_lower.endswith(".min.js") or name_lower.endswith(".min.css"):
            return True

        return False

    def read_file(self, path: Path) -> str:
        """Read file contents safely.

        Args:
            path: Path to file

        Returns:
            File contents or empty string if unreadable
        """
        try:
            return path.read_text(encoding="utf-8")
        except Exception as e:
            logger.warning(f"Could not read {path}: {e}")
            return ""

    def _generate_issue_id(self, prefix: str, index: int) -> str:
        """Generate unique issue ID.

        Args:
            prefix: Agent prefix (e.g., "SEC", "TEST")
            index: Issue index

        Returns:
            Unique issue ID (e.g., "SEC-001")
        """
        return f"{prefix}-{index:03d}"

    def is_test_file(self, path: Path) -> bool:
        """Check if a file is a test file.

        Args:
            path: Path to check

        Returns:
            True if this is a test file
        """
        name = path.name
        # Standard pytest patterns
        if name.startswith("test_") or name.endswith("_test.py"):
            return True
        # Check if in a tests directory
        return bool("tests" in path.parts or "test" in path.parts)

    def is_excluded_file(self, path: Path) -> bool:
        """Check if a file should be excluded from analysis.

        Checks against common infrastructure files that shouldn't be
        analyzed as application code (conftest.py, setup.py, migrations, etc.)

        Args:
            path: Path to check

        Returns:
            True if file should be excluded
        """
        import fnmatch

        # Check exact filename matches
        if path.name in EXCLUDED_FILES:
            return True

        # Check patterns
        rel_path = str(path)
        return any(fnmatch.fnmatch(rel_path, pattern) for pattern in EXCLUDED_PATTERNS)

    def parse_structured_response(
        self,
        response: str,
        prefix: str = "ISSUE",
    ) -> list[AgentIssue]:
        """Parse LLM structured text response into AgentIssue list.

        Parses responses in the structured text format used by all agent prompts.
        The format uses `---` as delimiter between issues.

        Expected format per issue:
            ISSUE: <ID like SEC-001, TEST-002, etc.>
            FILE: <exact file path>
            LINE: <line number>
            SEVERITY: <S0=critical, S1=high, S2=medium, S3=low>
            CONFIDENCE: <high/medium/low>
            WHY_BUG: <explain why this is wrong>
            FAILING_SCENARIO: <concrete input, state, or sequence that triggers>
            SUGGESTED_FIX: <minimal code change or test>
            NEEDS_DEEP_REVIEW: <yes/no>
            ---

        Args:
            response: Raw LLM response text
            prefix: Issue ID prefix for fallback generation (e.g., "SEC", "TEST")

        Returns:
            List of AgentIssue objects. Empty list if response is empty or
            contains no parseable issues.
        """
        if not response or not response.strip():
            return []

        issues: list[AgentIssue] = []
        # Split by delimiter (--- on its own line)
        blocks = response.split("\n---")

        # Severity mapping
        severity_map = {
            "s0": Priority.P0,
            "critical": Priority.P0,
            "s1": Priority.P1,
            "high": Priority.P1,
            "s2": Priority.P2,
            "medium": Priority.P2,
            "s3": Priority.P3,
            "low": Priority.P3,
        }

        for idx, block in enumerate(blocks):
            block = block.strip()
            if not block:
                continue

            # Parse fields from block
            fields = self._parse_block_fields(block)

            # Skip blocks without minimum required fields
            if not fields.get("issue") and not fields.get("file"):
                continue

            # Map severity string to Priority enum
            severity_str = fields.get("severity", "s2").lower()
            priority = severity_map.get(severity_str, Priority.P2)

            # Parse line number safely
            line_num = None
            if fields.get("line"):
                try:
                    line_num = int(fields["line"])
                except (ValueError, TypeError):
                    pass

            # Generate issue ID if not provided
            issue_id = fields.get("issue") or self._generate_issue_id(prefix, idx + 1)

            # Build description from WHY_BUG if available
            description = fields.get("why_bug", "")
            if fields.get("failing_scenario"):
                description += f"\n\nFailing scenario: {fields['failing_scenario']}"

            issues.append(
                AgentIssue(
                    id=issue_id,
                    title=fields.get("why_bug", "Issue detected")[:100],
                    description=description,
                    priority=priority,
                    file_path=fields.get("file"),
                    line_number=line_num,
                    dimension=fields.get("dimension", ""),
                    suggestion=fields.get("suggested_fix", ""),
                    metadata={
                        "confidence": fields.get("confidence", "medium"),
                        "needs_deep_review": fields.get("needs_deep_review", "no").lower() == "yes",
                        "failing_scenario": fields.get("failing_scenario", ""),
                    },
                )
            )

        return issues

    def _parse_block_fields(self, block: str) -> dict[str, str]:
        """Parse key-value fields from a structured response block.

        Handles multi-line values by collecting text until the next field.

        Args:
            block: Single issue block text

        Returns:
            Dictionary of field name to value
        """
        fields: dict[str, str] = {}
        current_field: str | None = None
        current_value: list[str] = []

        # Known field names (case-insensitive)
        known_fields = {
            "issue", "file", "line", "severity", "confidence",
            "why_bug", "failing_scenario", "suggested_fix",
            "needs_deep_review", "dimension",
        }

        for line in block.split("\n"):
            line = line.strip()
            if not line:
                continue

            # Check if line starts a new field
            field_found = False
            for field_name in known_fields:
                # Match "FIELD:" or "FIELD :" patterns (case-insensitive)
                upper_field = field_name.upper()
                if line.upper().startswith(f"{upper_field}:") or line.upper().startswith(f"{upper_field} :"):
                    # Save previous field
                    if current_field:
                        fields[current_field] = " ".join(current_value).strip()

                    # Start new field
                    current_field = field_name
                    # Extract value after colon
                    colon_idx = line.find(":")
                    current_value = [line[colon_idx + 1:].strip()] if colon_idx >= 0 else []
                    field_found = True
                    break

            if not field_found and current_field:
                # Continue multi-line value
                current_value.append(line)

        # Save last field
        if current_field:
            fields[current_field] = " ".join(current_value).strip()

        return fields

    # Paths that indicate sensitive code requiring escalation
    ESCALATION_PATHS: frozenset[str] = frozenset({
        "auth",
        "authentication",
        "authorization",
        "payment",
        "payments",
        "billing",
        "tenant",
        "tenants",
        "migrations",
        "security",
        "crypto",
        "encryption",
    })

    # Keywords in content that indicate sensitive code
    ESCALATION_KEYWORDS: frozenset[str] = frozenset({
        # Authentication/Authorization
        "authenticate",
        "authorize",
        "authorization",
        "jwt",
        "oauth",
        "token",
        "session",
        "login",
        "logout",
        "password",
        "credential",
        # Payment/Financial
        "stripe",
        "paypal",
        "payment",
        "charge",
        "refund",
        "billing",
        "invoice",
        "credit_card",
        "creditcard",
        # Concurrency (race conditions)
        "asyncio.lock",
        "threading.lock",
        "multiprocessing.lock",
        "mutex",
        "semaphore",
        "atomic",
        "race_condition",
        # Security/Crypto
        "encrypt",
        "decrypt",
        "hash",
        "secret",
        "private_key",
        "privatekey",
        "api_key",
        "apikey",
        # Database migrations
        "alembic",
        "migrate",
        "migration",
        "schema",
        # Multi-tenancy
        "tenant_id",
        "tenant",
        "isolation",
    })

    def _needs_escalation(
        self,
        file_path: Path | str | None = None,
        content: str | None = None,
    ) -> bool:
        """Check if code requires escalation to higher-tier LLM.

        Detects sensitive code patterns that benefit from deeper analysis:
        - Authentication/authorization logic
        - Payment processing
        - Concurrency primitives (race condition risk)
        - Cryptographic operations
        - Multi-tenant isolation
        - Database migrations

        Args:
            file_path: File path to check (checks directory components)
            content: File content to check (scans for keywords)

        Returns:
            True if sensitive code detected, requiring escalation
        """
        # Check file path components
        if file_path:
            path = Path(file_path) if isinstance(file_path, str) else file_path
            # Check each path component
            for part in path.parts:
                if part.lower() in self.ESCALATION_PATHS:
                    logger.debug(f"Escalation triggered by path component: {part}")
                    return True

        # Check content for keywords
        if content:
            content_lower = content.lower()
            for keyword in self.ESCALATION_KEYWORDS:
                if keyword in content_lower:
                    logger.debug(f"Escalation triggered by keyword: {keyword}")
                    return True

        return False


__all__ = ["EXCLUDED_FILES", "EXCLUDED_PATTERNS", "AgentIssue", "AgentResult", "BaseAgent"]
