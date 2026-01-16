"""Security review agent for vulnerability detection.

This module provides SecurityAgent, which analyzes code for security
vulnerabilities using LLM-powered semantic analysis.

Two-Tier Review:
    - Tier 1 (fast): Broad sweep to catch obvious issues
    - Tier 2 (high): Deep analysis of flagged regions for subtle vulnerabilities

Checks Performed:
    - Hardcoded credentials and secrets
    - SQL injection vulnerabilities
    - XSS vulnerabilities
    - Command injection
    - Path traversal
    - Insecure cryptography
    - Authorization boundary issues (Tier 2)
    - Race conditions (Tier 2)
    - Confused-deputy issues (Tier 2)

Scoring Dimensions:
    - vulnerability_free: No known vulnerabilities
    - secure_defaults: Uses secure defaults
    - input_validation: Proper input validation

Related:
    - obra/agents/base.py
    - obra/agents/registry.py
    - obra/agents/prompts/security_sweep.txt
    - obra/agents/prompts/security_deep.txt
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


@register_agent(AgentType.SECURITY)
class SecurityAgent(BaseAgent):
    """Security review agent with LLM-powered vulnerability detection.

    Uses two-tier review for comprehensive security analysis:
    - Tier 1 (fast): Quick sweep for common vulnerabilities
    - Tier 2 (high): Deep analysis for auth, race conditions, logic flaws

    When no LLM config is provided, returns empty results (no findings).

    Example:
        >>> agent = SecurityAgent(Path("/workspace"), llm_config=llm_config)
        >>> result = agent.analyze(
        ...     item_id="T1",
        ...     changed_files=["src/auth.py"],
        ...     timeout_ms=60000
        ... )
        >>> print(f"Found {len(result.issues)} security issues")
    """

    agent_type = AgentType.SECURITY

    def analyze(
        self,
        item_id: str,
        changed_files: list[str] | None = None,
        timeout_ms: int | None = None,
    ) -> AgentResult:
        """Analyze code for security vulnerabilities.

        Uses LLM-based analysis when invoker is available. Implements
        two-tier review: Tier 1 (fast) for broad sweep, Tier 2 (high)
        for deep analysis of flagged regions.

        Args:
            item_id: Plan item ID being reviewed
            changed_files: List of files that changed
            timeout_ms: Maximum execution time (None = use config default)

        Returns:
            AgentResult with security issues and scores
        """
        # Resolve timeout from config if not provided
        timeout_ms = self._resolve_timeout_ms(timeout_ms)

        # Validate parameters (ADR-042)
        self._validate_analyze_params(item_id, timeout_ms)

        start_time = time.time()
        logger.info(f"SecurityAgent analyzing {item_id}")

        # Get files to analyze - use blocklist approach to analyze ALL file types
        files = self.get_files_to_analyze(changed_files=changed_files)
        logger.debug(f"Analyzing {len(files)} files for security issues")

        # Use LLM-based analysis if config is available
        if self._llm_config:
            return self._analyze_with_llm(
                item_id=item_id,
                files=files,
                start_time=start_time,
                timeout_ms=timeout_ms,
            )

        # Fallback: No config available, return empty result with warning
        logger.warning("SecurityAgent: No LLM config available, skipping analysis")
        execution_time = int((time.time() - start_time) * 1000)
        return AgentResult(
            agent_type=self.agent_type,
            status="complete",
            issues=[],
            scores={
                "vulnerability_free": 1.0,
                "input_validation": 1.0,
                "secure_defaults": 1.0,
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
        """Perform LLM-based security analysis with two-tier review.

        Tier 1 (fast): Broad sweep for obvious vulnerabilities
        Tier 2 (high): Deep analysis for flagged regions

        Args:
            item_id: Plan item ID
            files: List of files to analyze
            start_time: Analysis start time
            timeout_ms: Maximum execution time

        Returns:
            AgentResult with merged issues from both tiers
        """
        deadline = start_time + (timeout_ms / 1000)
        all_issues: list[AgentIssue] = []

        # Load tier configuration
        tier_config = load_agent_tier_config("security")
        start_tier = tier_config.get("start_tier", "fast")
        escalate_tier = tier_config.get("escalate_tier", "high")

        # Load prompt templates (ISSUE-009: Use centralized loader)
        try:
            sweep_template = load_prompt("security_sweep")
            deep_template = load_prompt("security_deep")
        except FileNotFoundError as e:
            logger.error(f"Failed to load prompt template: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                status="error",
                error=f"Missing prompt template: {e}",
                execution_time_ms=int((time.time() - start_time) * 1000),
            )

        # Resolve LLM configs for both tiers
        fast_config = resolve_tier_config(start_tier, role="implementation")
        deep_config = resolve_tier_config(escalate_tier, role="implementation") if escalate_tier else None

        # Collect file contents for analysis with diagnostic counters
        files_content: dict[str, str] = {}
        excluded_count = 0
        read_fail_count = 0
        timeout_during_collection = False

        for file_path in files:
            if time.time() > deadline:
                logger.warning("SecurityAgent timed out during file collection")
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
                "SecurityAgent: No analyzable files. "
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
                    "vulnerability_free": 1.0,
                    "input_validation": 1.0,
                    "secure_defaults": 1.0,
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

        # TIER 1: Fast sweep
        logger.info(f"Running Tier 1 (fast) security sweep with {fast_config['provider']}/{fast_config['model']}")
        sweep_prompt = sweep_template.format(code_content=code_content)

        try:
            tier1_response = self._invoke_cli(
                call_site="security_tier1",
                prompt=sweep_prompt,
                timeout_ms=timeout_ms,
            )

            if not tier1_response:
                logger.warning("Tier 1 LLM invocation returned empty response")
                return AgentResult(
                    agent_type=self.agent_type,
                    status="error",
                    error="Tier 1 LLM invocation returned empty response",
                    execution_time_ms=int((time.time() - start_time) * 1000),
                )

            # Parse Tier 1 results
            tier1_issues = self.parse_structured_response(tier1_response, prefix="SEC")
            all_issues.extend(tier1_issues)
            logger.info(f"Tier 1 found {len(tier1_issues)} issues")

        except Exception as e:
            logger.exception(f"Tier 1 analysis failed: {e}")
            return AgentResult(
                agent_type=self.agent_type,
                status="error",
                error=f"Tier 1 analysis failed: {e}",
                execution_time_ms=int((time.time() - start_time) * 1000),
            )

        # Check if Tier 2 is needed
        needs_tier2 = False
        flagged_files: set[str] = set()

        # Check for NEEDS_DEEP_REVIEW flags
        for issue in tier1_issues:
            if issue.metadata.get("needs_deep_review"):
                needs_tier2 = True
                if issue.file_path:
                    flagged_files.add(issue.file_path)

        # Check for sensitive code paths
        for file_path, content in files_content.items():
            if self._needs_escalation(file_path=file_path, content=content):
                needs_tier2 = True
                flagged_files.add(file_path)

        # TIER 2: Deep analysis (if needed and configured)
        if needs_tier2 and deep_config and time.time() < deadline:
            logger.info(f"Running Tier 2 (deep) analysis on {len(flagged_files)} files with {deep_config['provider']}/{deep_config['model']}")

            # Emit tier_escalation event for observability
            if self._log_event:
                self._log_event(
                    "tier_escalation",
                    agent_type="security",
                    from_tier=start_tier,
                    to_tier=escalate_tier,
                    flagged_files_count=len(flagged_files),
                    reason="sensitive_code_or_deep_review_flag",
                )

            # Build content for deep analysis
            deep_content = {fp: files_content[fp] for fp in flagged_files if fp in files_content}
            if deep_content:
                deep_code = self._format_code_for_prompt(deep_content)

                # Format sweep findings for context
                sweep_findings = self._format_findings_for_deep(tier1_issues, flagged_files)

                deep_prompt = deep_template.format(
                    sweep_findings=sweep_findings,
                    code_content=deep_code,
                )

                try:
                    tier2_response = self._invoke_cli(
                        call_site="security_tier2",
                        prompt=deep_prompt,
                        timeout_ms=timeout_ms,
                    )

                    if tier2_response:
                        tier2_issues = self.parse_structured_response(tier2_response, prefix="SEC-DEEP")
                        # Deduplicate against Tier 1 findings
                        new_issues = self._dedupe_issues(tier2_issues, tier1_issues)
                        all_issues.extend(new_issues)
                        logger.info(f"Tier 2 found {len(new_issues)} additional issues")
                    else:
                        logger.warning("Tier 2 invocation returned empty response")

                except Exception as e:
                    logger.warning(f"Tier 2 analysis failed (non-fatal): {e}")

        # Calculate scores based on findings
        scores = self._calculate_scores_from_issues(all_issues)

        # Calculate severity breakdown for observability
        severity_breakdown = {
            "critical": sum(1 for i in all_issues if i.priority == Priority.P0),
            "high": sum(1 for i in all_issues if i.priority == Priority.P1),
            "medium": sum(1 for i in all_issues if i.priority == Priority.P2),
            "low": sum(1 for i in all_issues if i.priority == Priority.P3),
        }

        # Determine which tier was ultimately used
        tier_used = escalate_tier if needs_tier2 and deep_config else start_tier

        execution_time = int((time.time() - start_time) * 1000)
        logger.info(f"SecurityAgent complete: {len(all_issues)} issues found in {execution_time}ms")

        return AgentResult(
            agent_type=self.agent_type,
            status="complete",
            issues=all_issues,
            scores=scores,
            execution_time_ms=execution_time,
            metadata={
                "files_analyzed": len(files_content),
                "mode": "llm",
                "tier2_triggered": needs_tier2,
                "tier1_provider": fast_config["provider"],
                "tier1_model": fast_config["model"],
                "tier2_provider": deep_config["provider"] if deep_config else None,
                "tier2_model": deep_config["model"] if deep_config else None,
                # Observability fields (ADR-043)
                "issues_found": len(all_issues),
                "severity_breakdown": severity_breakdown,
                "tier_used": tier_used,
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

    def _format_findings_for_deep(
        self,
        issues: list[AgentIssue],
        flagged_files: set[str],
    ) -> str:
        """Format Tier 1 findings for Tier 2 deep analysis.

        Args:
            issues: Tier 1 issues
            flagged_files: Files flagged for deep review

        Returns:
            Formatted findings summary
        """
        relevant_issues = [i for i in issues if i.file_path in flagged_files]
        if not relevant_issues:
            return "No specific issues flagged - analyzing sensitive code paths."

        parts = []
        for issue in relevant_issues:
            parts.append(
                f"- {issue.id} ({issue.file_path}:{issue.line_number}): "
                f"{issue.title} - {issue.priority.value}"
            )
        return "\n".join(parts)

    def _dedupe_issues(
        self,
        new_issues: list[AgentIssue],
        existing_issues: list[AgentIssue],
    ) -> list[AgentIssue]:
        """Remove duplicate issues based on file and line.

        Args:
            new_issues: Issues to filter
            existing_issues: Already found issues

        Returns:
            Deduplicated new issues
        """
        existing_locations = {
            (i.file_path, i.line_number) for i in existing_issues
        }
        return [
            i for i in new_issues
            if (i.file_path, i.line_number) not in existing_locations
        ]

    def _calculate_scores_from_issues(self, issues: list[AgentIssue]) -> dict[str, float]:
        """Calculate dimension scores based on issues.

        Args:
            issues: All issues found

        Returns:
            Dict of dimension scores
        """
        vulnerabilities = 0
        input_issues = 0
        default_issues = 0

        for issue in issues:
            dim = issue.dimension
            if dim == "vulnerability_free":
                vulnerabilities += 1
            elif dim == "input_validation":
                input_issues += 1
            elif dim == "secure_defaults":
                default_issues += 1
            else:
                # Map priority to dimension for LLM issues without explicit dimension
                if issue.priority in (Priority.P0, Priority.P1):
                    vulnerabilities += 1
                else:
                    default_issues += 1

        def score(issue_count: int) -> float:
            if issue_count == 0:
                return 1.0
            if issue_count == 1:
                return 0.7
            if issue_count == 2:
                return 0.5
            if issue_count <= 5:
                return 0.3
            return 0.1

        return {
            "vulnerability_free": score(vulnerabilities),
            "input_validation": score(input_issues),
            "secure_defaults": score(default_issues),
        }


__all__ = ["SecurityAgent"]
