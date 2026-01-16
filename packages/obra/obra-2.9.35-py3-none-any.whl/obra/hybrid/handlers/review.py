"""Review handler for Hybrid Orchestrator.

This module handles the REVIEW action from the server. It deploys review agents
to analyze executed code for quality, security, testing, and documentation.

The review process:
    1. Receive ReviewRequest with item_id and agents to run
    2. Deploy each specified review agent via AgentDeployer
    3. Agents analyze code using LLM when invoker is provided
    4. Collect agent reports (issues, scores, execution time)
    5. Return AgentReports to report to server

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 2
    - obra/api/protocol.py
    - obra/hybrid/orchestrator.py
    - obra/agents/ (S9 implementation)
"""

from __future__ import annotations

import json
import logging
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path
from time import perf_counter
from typing import Any, cast

from obra.agents import AgentDeployer
from obra.api.protocol import AgentType, ReviewRequest
from obra.config import get_review_agent_timeout
from obra.display import print_error, print_info, print_warning
from obra.review.config import ALLOWED_AGENTS, ReviewConfig
from obra.review.constants import (
    COMPLEXITY_THRESHOLDS,
    has_security_pattern,
    has_test_pattern,
)
from obra.security import PromptSanitizer

logger = logging.getLogger(__name__)


class ReviewHandler:
    """Handler for REVIEW action.

    Deploys review agents to analyze executed code and collects their reports.
    Each agent analyzes different dimensions: security, testing, docs, code quality.

    ## Architecture Context (ADR-027)

    This handler is part of the hybrid client-server architecture where:
    - **Server**: Provides orchestration decisions and specifies which agents to run
    - **Client**: Deploys agents locally and collects reports

    **Current Implementation**:
    1. Server sends ReviewRequest with item_id and agents to run
    2. Client deploys each specified review agent locally via AgentDeployer
    3. Agents analyze code using LLM when llm_config is provided
    4. Client collects agent reports (issues, scores)
    5. Client reports aggregated results back to server for validation

    When llm_config is provided, agents perform LLM-powered semantic analysis.
    Without llm_config, agents return empty results (no findings).

    ## Privacy Protection

    Tactical context (code to review, file contents, git messages) never sent to server.
    Only aggregated review reports (issues summary, scores) is transmitted.

    See: docs/decisions/ADR-027-two-tier-prompting-architecture.md

    Example:
        >>> handler = ReviewHandler(Path("/path/to/project"), llm_config=llm_config)
        >>> request = ReviewRequest(
        ...     item_id="T1",
        ...     agents_to_run=["security", "testing"]
        ... )
        >>> result = handler.handle(request)
        >>> print(result["agent_reports"])
    """

    def __init__(
        self,
        working_dir: Path,
        *,
        llm_config: dict[str, Any] | None = None,
        review_config: ReviewConfig | None = None,
        log_event: Callable[..., None] | None = None,
        trace_id: str | None = None,
        parent_span_id: str | None = None,
    ) -> None:
        """Initialize ReviewHandler.

        Args:
            working_dir: Working directory for file access
            llm_config: Optional LLM configuration dict for CLI-based code analysis.
                       When provided, review agents use LLM for semantic analysis.
                       When None, agents return empty results.
            review_config: Review selection and modifier configuration
            log_event: Optional callback for logging session events
            trace_id: Optional trace ID for observability
            parent_span_id: Optional parent span ID for observability
        """
        self._working_dir = working_dir
        self._deployer = AgentDeployer(working_dir, llm_config=llm_config)
        self._sanitizer = PromptSanitizer()
        self._config = review_config or ReviewConfig()
        self._log_event = log_event
        self._trace_id = trace_id
        self._parent_span_id = parent_span_id

    def _log_info(self, message: str) -> None:
        """Print info messages unless quiet mode is enabled."""
        if not self._config.quiet:
            print_info(message)

    def _log_warning(self, message: str) -> None:
        """Print warning messages unless quiet mode is enabled."""
        if not self._config.quiet:
            print_warning(message)

    def _log_error(self, message: str) -> None:
        """Print error messages unless quiet mode is enabled."""
        if not self._config.quiet:
            print_error(message)

    def handle(self, request: ReviewRequest) -> dict[str, Any]:
        """Handle REVIEW action.

        Falls back to local complexity detection when the server does not provide
        agents to run. Emits per-agent progress, counts, and a summary with tier metadata.

        Args:
            request: ReviewRequest from server

        Returns:
            Dict with agent_reports list, total issue counts, and failed agent count.
        """
        logger.info(f"Starting review for item: {request.item_id}")

        output_format = self._resolve_output_format(request.format)
        is_json_output = output_format == "json"
        emit_text_output = not is_json_output

        if emit_text_output:
            self._log_info(f"Running review agents for: {request.item_id}")

        agent_reports: list[dict[str, Any]] = []
        agent_runs: list[dict[str, Any]] = []
        json_output: dict[str, Any] | None = None
        complexity_tier: str | None = request.complexity

        if self._config.skip_review:
            if emit_text_output:
                self._log_info("Review skipped by configuration")

            if is_json_output:
                json_output = self._emit_json_output(
                    agent_runs=agent_runs,
                    agent_reports=agent_reports,
                    complexity_tier=complexity_tier,
                    total_elapsed_ms=0,
                )

            result: dict[str, Any] = {
                "item_id": request.item_id,
                "agent_reports": agent_reports,
                "total_issues": 0,
                "failed_agents": 0,
            }
            if json_output is not None:
                result["review_output"] = json_output
            return result

        agents_from_request = request.agents_to_run or []
        selection: dict[str, Any] | None = None
        changed_files: list[str] | None = None

        if agents_from_request:
            changed_files = self._get_changed_files()
            logger.info("Using server-provided review agents: %s", agents_from_request)
        else:
            selection = self._detect_complexity()
            changed_files = selection.get("changed_files")
            complexity_tier = complexity_tier or selection.get("complexity")
            logger.info(
                "Using local review agent selection (%s): %s",
                selection.get("complexity", "unknown"),
                selection["agents"],
            )

        resolved_agents = self._config.resolve_agents(
            detected_agents=selection["agents"] if selection else None,
            server_agents=agents_from_request,
        )
        if logger.isEnabledFor(logging.DEBUG):
            baseline_agents = agents_from_request or (
                selection["agents"] if selection else []
            )
            removed_agents = [agent for agent in baseline_agents if agent not in resolved_agents]
            added_agents = [agent for agent in resolved_agents if agent not in baseline_agents]
            logger.debug(
                "Review agents resolved: %s (baseline=%s, added=%s, removed=%s, "
                "full_review=%s, skip_review=%s, explicit_agents=%s)",
                resolved_agents,
                baseline_agents,
                added_agents,
                removed_agents,
                self._config.full_review,
                self._config.skip_review,
                self._config.explicit_agents,
            )

        if not resolved_agents:
            if emit_text_output:
                self._log_info("No review agents selected after configuration overrides")

            if is_json_output:
                json_output = self._emit_json_output(
                    agent_runs=agent_runs,
                    agent_reports=agent_reports,
                    complexity_tier=complexity_tier,
                    total_elapsed_ms=0,
                )

            result = {
                "item_id": request.item_id,
                "agent_reports": agent_reports,
                "total_issues": 0,
                "failed_agents": 0,
            }
            if json_output is not None:
                result["review_output"] = json_output
            return result

        files_for_agents = changed_files or None

        for agent_name in resolved_agents:
            try:
                agent_type = AgentType(agent_name)
            except ValueError:
                logger.warning(f"Unknown agent type: {agent_name}, skipping")
                continue

            budget = request.agent_budgets.get(agent_name, {})
            timeout_ms = self._resolve_timeout_ms(agent_name, budget)

            if emit_text_output and not self._config.quiet and not self._config.summary_only:
                print_info(f"[{agent_type.value}] running...")

            start_time = perf_counter()

            report = self._deploy_agent(
                item_id=request.item_id,
                agent_type=agent_type,
                changed_files=files_for_agents,
                timeout_ms=timeout_ms,
            )
            agent_reports.append(report)

            elapsed_seconds = perf_counter() - start_time
            elapsed_ms = max(int(elapsed_seconds * 1000), 0)

            status = str(report.get("status", "unknown")).lower()
            issues = report.get("issues", [])
            issue_count = len(issues) if isinstance(issues, list) else 0
            error_message = report.get("error")

            agent_runs.append(
                {
                    "agent": agent_type.value,
                    "status": status,
                    "issue_count": issue_count,
                    "elapsed_ms": elapsed_ms,
                    "error": error_message or None,
                }
            )

            completion_message, log_fn = self._build_completion_message(
                agent_type.value,
                status,
                issue_count,
                elapsed_seconds,
                error_message,
            )
            if emit_text_output:
                log_fn(completion_message)

        total_issues = sum(run["issue_count"] for run in agent_runs)
        failed_agents = [
            run for run in agent_runs if run["status"] in ("error", "timeout")
        ]
        complexity_display = (complexity_tier or "unknown").lower()
        agent_count = len(agent_runs)
        summary_line = (
            f"Review summary ({agent_count} {'agent' if agent_count == 1 else 'agents'}, "
            f"{complexity_display} task): "
            f"{total_issues} {'finding' if total_issues == 1 else 'findings'}"
        )

        if emit_text_output:
            if failed_agents:
                summary_line = f"{summary_line}, {len(failed_agents)} failed"
                self._log_warning(summary_line)
            else:
                self._log_info(summary_line)

            if self._should_show_full_review_hint(agent_runs, complexity_display):
                self._log_info("Run with --full-review for comprehensive analysis.")

        logger.info(
            "Review complete: %s agents ran, %s failed, %s total issues (complexity=%s)",
            len(agent_runs),
            len(failed_agents),
            total_issues,
            complexity_display,
        )

        if is_json_output:
            total_elapsed_ms = sum(run["elapsed_ms"] for run in agent_runs)
            json_output = self._emit_json_output(
                agent_runs=agent_runs,
                agent_reports=agent_reports,
                complexity_tier=complexity_display,
                total_elapsed_ms=total_elapsed_ms,
            )

        result = {
            "item_id": request.item_id,
            "agent_reports": agent_reports,
            "total_issues": total_issues,
            "failed_agents": len(failed_agents),  # Add for upstream tracking
        }
        if json_output is not None:
            result["review_output"] = json_output
        return result

    def _build_completion_message(
        self,
        agent: str,
        status: str,
        issue_count: int,
        elapsed_seconds: float,
        error_message: Any,
    ) -> tuple[str, Callable[[str], None]]:
        """Return formatted completion message and logger based on status."""
        elapsed_text = f"{elapsed_seconds:.1f}s"
        findings_label = "finding" if issue_count == 1 else "findings"

        if status == "complete":
            return (
                f"[{agent}] done ({elapsed_text}) - {issue_count} {findings_label}",
                self._log_info,
            )

        if status == "timeout":
            return (f"[{agent}] timed out after {elapsed_text}", self._log_warning)

        if status == "error":
            detail = str(error_message) if error_message else "error"
            return (
                f"[{agent}] error after {elapsed_text}: {detail}",
                self._log_error,
            )

        return (
            f"[{agent}] {status} after {elapsed_text}",
            self._log_warning,
        )

    def _resolve_output_format(self, request_format: str | None) -> str:
        """Resolve effective output format using config override or request payload."""
        if self._config.output_format:
            return str(self._config.output_format)

        if request_format:
            normalized = str(request_format).strip().lower()
            if normalized in ("text", "json"):
                return normalized

        return "text"

    def _emit_json_output(
        self,
        *,
        agent_runs: Sequence[dict[str, Any]],
        agent_reports: Sequence[dict[str, Any]],
        complexity_tier: str | None,
        total_elapsed_ms: int,
    ) -> dict[str, Any]:
        """Build and print structured JSON review output."""
        payload = self._build_json_output(
            agent_runs=agent_runs,
            agent_reports=agent_reports,
            complexity_tier=complexity_tier,
            total_elapsed_ms=total_elapsed_ms,
        )

        if not self._config.quiet:
            print(json.dumps(payload, sort_keys=True))

        return payload

    def _build_json_output(
        self,
        *,
        agent_runs: Sequence[dict[str, Any]],
        agent_reports: Sequence[dict[str, Any]],
        complexity_tier: str | None,
        total_elapsed_ms: int,
    ) -> dict[str, Any]:
        """Construct JSON-friendly review summary for --review-format=json."""
        agents_output: list[dict[str, Any]] = []
        for run in agent_runs:
            agent_entry = {
                "agent": run.get("agent"),
                "status": run.get("status", "unknown"),
                "issue_count": int(run.get("issue_count", 0)),
                "elapsed_ms": int(run.get("elapsed_ms", 0)),
            }
            if run.get("error"):
                agent_entry["error"] = run["error"]
            agents_output.append(agent_entry)

        findings_by_agent: dict[str, Any] = {}
        for report in agent_reports:
            agent_name = str(report.get("agent_type") or report.get("agent") or "").strip()
            if not agent_name:
                continue

            issues = report.get("issues", [])
            issues_list = issues if isinstance(issues, list) else []
            priorities: dict[str, int] = {"p1": 0, "p2": 0, "p3": 0}
            for issue in issues_list:
                if not isinstance(issue, dict):
                    continue

                priority_value = issue.get("priority")
                if priority_value is None:
                    continue

                key = str(priority_value).lower()
                if key in priorities:
                    priorities[key] += 1
                elif key.startswith("p") and key[1:].isdigit():
                    priorities[key] = priorities.get(key, 0) + 1

            findings_by_agent[agent_name] = {
                "issue_count": len(issues_list),
                "priorities": priorities,
            }

        failed_agents = [
            run for run in agent_runs if run.get("status") in ("error", "timeout")
        ]
        totals = {
            "agents": len(agent_runs),
            "issue_count": sum(run.get("issue_count", 0) for run in agent_runs),
            "failed_agents": len(failed_agents),
            "elapsed_ms": total_elapsed_ms,
        }

        return {
            "agents_run": agents_output,
            "complexity_tier": (complexity_tier or "unknown").lower(),
            "findings_by_agent": findings_by_agent,
            "totals": totals,
        }

    def _should_show_full_review_hint(
        self, agent_runs: Sequence[dict[str, Any]], complexity_tier: str | None
    ) -> bool:
        """Return True when the run is minimal enough to suggest full review."""
        if self._config.quiet:
            return False

        if self._config.full_review or self._config.explicit_agents is not None:
            return False

        if not agent_runs:
            return False

        normalized_tier = (complexity_tier or "").lower()
        if normalized_tier == "simple":
            return True

        if len(agent_runs) == 1:
            return True

        return len(agent_runs) < len(ALLOWED_AGENTS)

    def _resolve_timeout_ms(self, agent_name: str, budget: dict[str, Any] | None) -> int:
        """Resolve timeout in milliseconds using config override or agent budget."""
        if self._config.timeout_seconds is not None:
            return int(self._config.timeout_seconds * 1000)

        timeout_ms = None
        if isinstance(budget, dict):
            timeout_ms = budget.get("timeout_ms")

        if isinstance(timeout_ms, (int, float)) and timeout_ms > 0:
            return int(timeout_ms)

        logger.debug(
            "Using default timeout for %s agent (config unset, budget invalid): %s",
            agent_name,
            timeout_ms,
        )
        return get_review_agent_timeout() * 1000

    def _deploy_agent(
        self,
        item_id: str,
        agent_type: AgentType,
        changed_files: list[str] | None,
        timeout_ms: int | None = None,
    ) -> dict[str, Any]:
        """Deploy a review agent using AgentDeployer.

        Args:
            item_id: Plan item ID being reviewed
            agent_type: Type of review agent
            timeout_ms: Timeout in milliseconds (None = use config default)

        Returns:
            Agent report dictionary
        """
        # Resolve timeout from config if not provided
        if timeout_ms is None:
            timeout_ms = get_review_agent_timeout() * 1000

        logger.debug(f"Deploying {agent_type.value} agent for {item_id}")

        # Use the deployer to run the agent
        result = self._deployer.run_agent(
            agent_type=agent_type,
            item_id=item_id,
            changed_files=changed_files,
            timeout_ms=timeout_ms,
            log_event=self._log_event,
            trace_id=self._trace_id,
            parent_span_id=self._parent_span_id,
        )

        # Convert AgentResult to dict for API serialization
        report = cast(dict[str, Any], result.to_dict())
        report["item_id"] = item_id

        return report

    def _get_changed_files(self) -> list[str] | None:
        """Collect changed files from git status when available.

        Returns:
            List of changed file paths relative to working_dir when git is available.
            Returns None when git is unavailable or the status command fails.
        """
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain", "--untracked-files=all"],
                cwd=self._working_dir,
                check=False,
                capture_output=True,
                text=True,
                timeout=2,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
            logger.debug("Failed to read git status: %s", exc)
            return None

        if result.returncode != 0:
            logger.debug(
                "git status returned %s for %s: %s",
                result.returncode,
                self._working_dir,
                result.stderr.strip(),
            )
            return None

        files: list[str] = []
        for line in result.stdout.splitlines():
            if not line or len(line) < 4:
                continue

            path = line[3:]
            if "->" in path:
                path = path.split("->", 1)[1]
            path = path.strip()

            if path.startswith('"') and path.endswith('"'):
                path = path[1:-1]

            if path:
                files.append(path)

        return files

    def _count_lines_added(self, files: list[str] | None) -> int:
        """Count total lines added across the provided files using git numstat.

        Args:
            files: List of files to include. If None or empty, returns 0.

        Returns:
            Total lines added. Returns 0 when git is unavailable or parsing fails.
        """
        if not files:
            return 0

        command = ["git", "diff", "--numstat", "HEAD", "--", *files]
        try:
            result = subprocess.run(
                command,
                cwd=self._working_dir,
                check=False,
                capture_output=True,
                text=True,
                timeout=3,
            )
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as exc:
            logger.debug("Failed to run git diff --numstat: %s", exc)
            return 0

        if result.returncode != 0:
            logger.debug(
                "git diff --numstat returned %s for %s: %s",
                result.returncode,
                self._working_dir,
                result.stderr.strip(),
            )
            return 0

        lines_added = 0
        for line in result.stdout.splitlines():
            if not line:
                continue

            parts = line.split("\t")
            if len(parts) < 2:
                continue

            added = parts[0].strip()
            if added in ("", "-"):
                continue

            try:
                lines_added += int(added)
            except ValueError:
                continue

        return lines_added

    def _has_security_sensitive_files(self, files: Sequence[str] | None) -> bool:
        """Return True when any file path matches known security-sensitive patterns."""
        if not files:
            return False

        return any(has_security_pattern(path) for path in files)

    def _has_test_files(self, files: Sequence[str] | None) -> bool:
        """Return True when any file path points to a test file or directory."""
        if not files:
            return False

        return any(has_test_pattern(path) for path in files)

    def _detect_complexity(self) -> dict[str, Any]:
        """Select review agents using local change signals and shared thresholds."""
        changed_files = self._get_changed_files()

        if changed_files is None:
            agents = [
                AgentType.CODE_QUALITY.value,
                AgentType.SECURITY.value,
                AgentType.TESTING.value,
                AgentType.DOCS.value,
                AgentType.TEST_EXECUTION.value,
            ]
            return {
                "agents": agents,
                "complexity": "complex",
                "changed_files": None,
                "lines_added": 0,
                "files_changed": None,
            }

        lines_added = self._count_lines_added(changed_files)
        files_changed = len(changed_files)

        simple_threshold = COMPLEXITY_THRESHOLDS["simple"]
        medium_threshold = COMPLEXITY_THRESHOLDS["medium"]

        if (
            files_changed <= simple_threshold["max_files"]
            and lines_added <= simple_threshold["max_lines"]
        ):
            complexity = "simple"
            agents = [AgentType.CODE_QUALITY.value]
        elif (
            files_changed <= medium_threshold["max_files"]
            and lines_added <= medium_threshold["max_lines"]
        ):
            complexity = "medium"
            agents = [AgentType.CODE_QUALITY.value, AgentType.SECURITY.value]
        else:
            complexity = "complex"
            agents = [
                AgentType.CODE_QUALITY.value,
                AgentType.SECURITY.value,
                AgentType.TESTING.value,
                AgentType.DOCS.value,
                AgentType.TEST_EXECUTION.value,
            ]

        if (
            self._has_security_sensitive_files(changed_files)
            and AgentType.SECURITY.value not in agents
        ):
            agents.insert(0, AgentType.SECURITY.value)

        if (
            self._has_test_files(changed_files)
            and AgentType.TESTING.value not in agents
        ):
            agents.append(AgentType.TESTING.value)

        return {
            "agents": agents,
            "complexity": complexity,
            "changed_files": changed_files,
            "lines_added": lines_added,
            "files_changed": files_changed,
        }


__all__ = ["ReviewHandler"]
