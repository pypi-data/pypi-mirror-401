"""Intent completion verification module.

This module provides verification functionality to check completion
against intent acceptance criteria. Generates verification reports
saved to ~/.obra/completion/{project}/.

Verification Flow:
    1. Load active intent
    2. Evaluate each acceptance criterion
    3. Generate verification report
    4. Archive intent if all criteria pass

Storage Location:
    ~/.obra/completion/{project}/{intent-id}_VERIFICATION.md

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - obra/intent/storage.py
    - obra/intent/models.py
"""

import logging
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from obra.intent.models import IntentModel, IntentStatus
from obra.intent.storage import IntentStorage

logger = logging.getLogger(__name__)

# Default completion root
DEFAULT_COMPLETION_ROOT = Path.home() / ".obra" / "completion"


class VerificationStatus(str, Enum):
    """Status of verification result."""

    PASSED = "passed"
    FAILED = "failed"
    PARTIAL = "partial"
    SKIPPED = "skipped"


class CriterionResult(BaseModel):
    """Result of verifying a single acceptance criterion.

    Attributes:
        criterion: The acceptance criterion text
        passed: Whether the criterion was met
        evidence: Optional evidence or explanation
        notes: Additional notes about verification
    """

    criterion: str = Field(..., description="The acceptance criterion text")
    passed: bool = Field(..., description="Whether the criterion was met")
    evidence: str | None = Field(
        default=None, description="Optional evidence or explanation"
    )
    notes: str | None = Field(default=None, description="Additional notes")

    model_config = {"extra": "forbid"}


class VerificationReport(BaseModel):
    """Verification report for intent completion.

    Attributes:
        intent_id: Intent ID that was verified
        project: Project identifier
        verified_at: Verification timestamp (ISO-8601)
        status: Overall verification status
        results: List of criterion verification results
        summary: Optional summary of verification
        metadata: Optional metadata for extensibility
    """

    intent_id: str = Field(..., description="Intent ID that was verified")
    project: str = Field(..., description="Project identifier")
    verified_at: str = Field(..., description="Verification timestamp (ISO-8601)")
    status: VerificationStatus = Field(..., description="Overall verification status")
    results: list[CriterionResult] = Field(
        default_factory=list, description="List of criterion verification results"
    )
    summary: str | None = Field(default=None, description="Optional summary")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Optional metadata"
    )

    model_config = {"extra": "forbid"}

    @property
    def passed(self) -> bool:
        """Check if verification passed (all criteria met)."""
        return self.status == VerificationStatus.PASSED

    @property
    def total_criteria(self) -> int:
        """Get total number of criteria."""
        return len(self.results)

    @property
    def passed_criteria(self) -> int:
        """Get number of criteria that passed."""
        return sum(1 for r in self.results if r.passed)

    @property
    def failed_criteria(self) -> int:
        """Get number of criteria that failed."""
        return sum(1 for r in self.results if not r.passed)


def verify_completion(
    intent: IntentModel,
    project_dir: Path | None = None,
    auto_verify: bool = False,
) -> VerificationReport:
    """Verify completion against intent acceptance criteria.

    This function evaluates each acceptance criterion from the intent.
    In auto_verify mode, it performs basic file/directory checks.
    Otherwise, it returns a report template for manual verification.

    Args:
        intent: IntentModel to verify against
        project_dir: Optional project directory for file checks
        auto_verify: Whether to perform automatic verification checks

    Returns:
        VerificationReport with verification results

    Example:
        >>> storage = IntentStorage()
        >>> intent = storage.load_active("my-app")
        >>> report = verify_completion(intent, auto_verify=False)
        >>> print(report.status)
        'partial'
    """
    logger.info(
        "Verifying completion for intent %s (auto_verify=%s)",
        intent.id,
        auto_verify,
    )

    results: list[CriterionResult] = []

    if not intent.acceptance_criteria:
        # No criteria to verify
        logger.warning("Intent %s has no acceptance criteria", intent.id)
        return VerificationReport(
            intent_id=intent.id,
            project=intent.project,
            verified_at=datetime.now(UTC).isoformat(),
            status=VerificationStatus.SKIPPED,
            summary="No acceptance criteria defined",
        )

    for criterion in intent.acceptance_criteria:
        if auto_verify and project_dir:
            # Attempt automatic verification
            passed = _auto_verify_criterion(criterion, project_dir)
            results.append(
                CriterionResult(
                    criterion=criterion,
                    passed=passed,
                    notes="Auto-verified" if passed else "Failed auto-verification",
                )
            )
        else:
            # Manual verification template (user must fill in)
            results.append(
                CriterionResult(
                    criterion=criterion,
                    passed=False,  # Default to false for manual review
                    notes="Pending manual verification",
                )
            )

    # Determine overall status
    passed_count = sum(1 for r in results if r.passed)
    total_count = len(results)

    if passed_count == total_count:
        status = VerificationStatus.PASSED
        summary = f"All {total_count} acceptance criteria met"
    elif passed_count == 0:
        status = VerificationStatus.FAILED
        summary = f"None of {total_count} acceptance criteria met"
    else:
        status = VerificationStatus.PARTIAL
        summary = f"{passed_count}/{total_count} acceptance criteria met"

    return VerificationReport(
        intent_id=intent.id,
        project=intent.project,
        verified_at=datetime.now(UTC).isoformat(),
        status=status,
        results=results,
        summary=summary,
    )


def _auto_verify_criterion(criterion: str, project_dir: Path) -> bool:
    """Attempt automatic verification of a criterion.

    This is a best-effort heuristic-based check. Not reliable for
    all criterion types, but useful for basic file existence checks.

    Args:
        criterion: Acceptance criterion text
        project_dir: Project directory path

    Returns:
        True if criterion appears to be met, False otherwise
    """
    criterion_lower = criterion.lower()

    # Check for file/directory existence patterns
    if "file" in criterion_lower or "exists" in criterion_lower:
        # Look for file path patterns in the criterion
        # This is a simple heuristic - not comprehensive
        words = criterion.split()
        for word in words:
            if "/" in word or "\\" in word:
                file_path = project_dir / word.strip("'\"")
                if file_path.exists():
                    return True

    # For other criteria, cannot auto-verify
    logger.debug("Cannot auto-verify criterion: %s", criterion)
    return False


def save_verification_report(
    report: VerificationReport,
    root: Path | None = None,
) -> Path:
    """Save verification report to disk.

    Reports are saved to ~/.obra/completion/{project}/{intent-id}_VERIFICATION.md

    Args:
        report: VerificationReport to save
        root: Optional custom root directory (default: ~/.obra/completion/)

    Returns:
        Path to saved report file

    Example:
        >>> report = verify_completion(intent)
        >>> path = save_verification_report(report)
        >>> print(path)
        ~/.obra/completion/my-app/20260110T1200-add-auth_VERIFICATION.md
    """
    completion_root = root or DEFAULT_COMPLETION_ROOT
    project_dir = completion_root / report.project
    project_dir.mkdir(parents=True, exist_ok=True)

    file_path = project_dir / f"{report.intent_id}_VERIFICATION.md"

    # Render report to markdown
    content = _render_verification_markdown(report)
    file_path.write_text(content, encoding="utf-8")

    logger.info("Saved verification report to %s", file_path)
    return file_path


def _render_verification_markdown(report: VerificationReport) -> str:
    """Render verification report as markdown.

    Args:
        report: VerificationReport to render

    Returns:
        Markdown content string
    """
    status_emoji = {
        VerificationStatus.PASSED: "✓",
        VerificationStatus.FAILED: "✗",
        VerificationStatus.PARTIAL: "⚠",
        VerificationStatus.SKIPPED: "○",
    }

    lines = [
        f"# Verification Report: {report.intent_id}",
        "",
        f"**Project**: {report.project}",
        f"**Verified**: {report.verified_at}",
        f"**Status**: {status_emoji.get(report.status, '?')} {report.status.value.upper()}",
        "",
    ]

    if report.summary:
        lines.extend(["## Summary", "", report.summary, ""])

    if report.results:
        lines.extend(["## Acceptance Criteria", ""])
        for result in report.results:
            check = "x" if result.passed else " "
            lines.append(f"- [{check}] {result.criterion}")
            if result.evidence:
                lines.append(f"  - Evidence: {result.evidence}")
            if result.notes:
                lines.append(f"  - Notes: {result.notes}")
            lines.append("")

    lines.extend(
        [
            "## Statistics",
            "",
            f"- Total Criteria: {report.total_criteria}",
            f"- Passed: {report.passed_criteria}",
            f"- Failed: {report.failed_criteria}",
            f"- Pass Rate: {report.passed_criteria}/{report.total_criteria}",
            "",
        ]
    )

    lines.extend(
        [
            "---",
            "_Generated by Obra verification system_",
            f"_File: ~/.obra/completion/{report.project}/{report.intent_id}_VERIFICATION.md_",
        ]
    )

    return "\n".join(lines)


def archive_intent(intent_id: str, project: str, storage: IntentStorage | None = None) -> bool:
    """Archive an intent after successful verification.

    Changes intent status to ARCHIVED. The intent file remains
    in storage but is no longer active.

    Args:
        intent_id: Intent ID to archive
        project: Project identifier
        storage: Optional IntentStorage instance (creates new if None)

    Returns:
        True if archived successfully, False otherwise

    Example:
        >>> archive_intent("20260110T1200-add-auth", "my-app")
        True
    """
    storage = storage or IntentStorage()

    # Load the intent
    intent = storage.load(intent_id, project)
    if not intent:
        logger.error("Cannot archive - intent not found: %s", intent_id)
        return False

    # Update status to archived
    intent.status = IntentStatus.ARCHIVED

    # Save updated intent
    storage.save(intent)

    # Clear active intent if this was the active one
    active_intent = storage.load_active(project)
    if active_intent and active_intent.id == intent_id:
        storage._update_index(project, "", IntentStatus.ARCHIVED)  # Clear active
        logger.info("Cleared active intent for project %s", project)

    logger.info("Archived intent %s for project %s", intent_id, project)
    return True


# Convenience exports
__all__ = [
    "CriterionResult",
    "VerificationReport",
    "VerificationStatus",
    "archive_intent",
    "save_verification_report",
    "verify_completion",
]
