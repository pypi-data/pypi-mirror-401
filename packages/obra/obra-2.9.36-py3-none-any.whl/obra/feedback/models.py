"""Data models for beta tester feedback system.

This module defines the core data structures for feedback collection,
following industry standards for bug tracking and user feedback systems.

Design Principles:
- Explicit privacy levels for user control
- Separation of required vs optional fields
- Structured data for automated processing
- Human-readable descriptions for UX
"""

import platform
import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class PrivacyLevel(str, Enum):
    """Privacy level for feedback submission.

    Determines how much data is collected and shared.

    Levels:
        FULL: Maximum data for debugging (prompts, commands, full logs)
        STANDARD: Balanced data (truncated prompts, error messages, system info)
        MINIMAL: Essential data only (summary, category, basic system info)
    """
    FULL = "full"
    STANDARD = "standard"
    MINIMAL = "minimal"

    @property
    def description(self) -> str:
        """Human-readable description of what data is collected."""
        descriptions = {
            PrivacyLevel.FULL: (
                "Maximum diagnostic data: full prompts, commands, logs, "
                "error traces, and system configuration. Best for complex bugs."
            ),
            PrivacyLevel.STANDARD: (
                "Balanced data: truncated prompts (first/last 500 chars), "
                "error messages, system info, and anonymized context."
            ),
            PrivacyLevel.MINIMAL: (
                "Essential data only: summary, category, Obra version, "
                "and OS type. No prompts or personal project information."
            ),
        }
        return descriptions[self]


class FeedbackType(str, Enum):
    """Type of feedback being submitted."""
    BUG = "bug"
    FEATURE = "feature"
    COMMENT = "comment"
    QUESTION = "question"
    PRAISE = "praise"  # Positive feedback helps too!


class Severity(str, Enum):
    """Bug severity levels (aligned with industry standards)."""
    CRITICAL = "critical"  # App crashes, data loss, security issue
    HIGH = "high"          # Major feature broken, significant impact
    MEDIUM = "medium"      # Feature partially broken, workaround exists
    LOW = "low"            # Minor issue, cosmetic, edge case

    @property
    def description(self) -> str:
        """Human-readable description for user selection."""
        descriptions = {
            Severity.CRITICAL: "App crashes, data loss, or security vulnerability",
            Severity.HIGH: "Major feature broken, can't complete task",
            Severity.MEDIUM: "Feature partially works, workaround exists",
            Severity.LOW: "Minor issue, cosmetic problem, or edge case",
        }
        return descriptions[self]


@dataclass
class SystemInfo:
    """Automatically collected system information.

    This data helps diagnose environment-specific issues.
    Collection respects privacy level settings.
    """
    # Always collected (minimal level)
    obra_version: str = ""
    os_type: str = ""  # "linux", "darwin", "windows"

    # Standard level
    os_version: str = ""
    python_version: str = ""
    terminal_type: str = ""  # "wsl2", "native", "ssh", etc.
    installation_method: str = ""  # "pip", "pipx", "source"

    # Full level
    shell: str = ""
    locale: str = ""
    environment_vars: dict[str, str] = field(default_factory=dict)
    llm_provider: str = ""  # "claude", "codex", "gemini", "ollama"
    llm_model: str = ""

    @classmethod
    def collect(cls, privacy_level: PrivacyLevel = PrivacyLevel.STANDARD) -> "SystemInfo":
        """Collect system information respecting privacy level."""
        import os
        import shutil

        from obra import __version__

        info = cls()

        # Always collect (minimal)
        info.obra_version = __version__
        info.os_type = platform.system().lower()

        if privacy_level == PrivacyLevel.MINIMAL:
            return info

        # Standard level additions
        info.os_version = platform.release()
        info.python_version = platform.python_version()

        # Detect terminal type
        if os.environ.get("WSL_DISTRO_NAME"):
            info.terminal_type = "wsl2"
        elif os.environ.get("SSH_CONNECTION"):
            info.terminal_type = "ssh"
        elif os.environ.get("TERM_PROGRAM"):
            info.terminal_type = os.environ.get("TERM_PROGRAM", "unknown")
        else:
            info.terminal_type = "native"

        # Detect installation method
        try:
            import importlib.metadata
            dist = importlib.metadata.distribution("obra")
            installer = dist.read_text("INSTALLER") if dist else ""
            if "pipx" in installer.lower():
                info.installation_method = "pipx"
            elif dist:
                info.installation_method = "pip"
            else:
                info.installation_method = "source"
        except Exception:
            info.installation_method = "unknown"

        if privacy_level == PrivacyLevel.STANDARD:
            return info

        # Full level additions
        info.shell = os.environ.get("SHELL", "unknown")
        info.locale = os.environ.get("LANG", os.environ.get("LC_ALL", "unknown"))

        # Collect relevant environment variables (filtered for privacy)
        safe_env_vars = [
            "TERM", "COLORTERM", "EDITOR", "VISUAL",
            "PYTHONUTF8", "PYTHONIOENCODING",
        ]
        info.environment_vars = {
            k: os.environ.get(k, "")
            for k in safe_env_vars
            if os.environ.get(k)
        }

        # Detect LLM provider from available CLIs
        for provider, cmd in [("claude", "claude"), ("codex", "codex"), ("gemini", "gemini")]:
            if shutil.which(cmd):
                info.llm_provider = provider
                break

        return info

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary, excluding empty values."""
        result = {}
        for key, value in self.__dict__.items():
            if value:  # Skip empty strings, dicts, etc.
                if isinstance(value, dict):
                    if value:  # Only include non-empty dicts
                        result[key] = value
                else:
                    result[key] = value
        return result


@dataclass
class ReportMetadata:
    """Metadata for all feedback reports."""
    report_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    submitted_at: str | None = None
    privacy_level: PrivacyLevel = PrivacyLevel.STANDARD

    # User identity (optional)
    user_id: str | None = None  # Firebase UID if logged in
    email: str | None = None    # Optional contact email
    anonymous: bool = True      # True if no identifying info provided

    # Submission status
    submitted: bool = False
    server_report_id: str | None = None  # ID assigned by server

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "submitted_at": self.submitted_at,
            "privacy_level": self.privacy_level.value,
            "user_id": self.user_id,
            "email": self.email,
            "anonymous": self.anonymous,
            "submitted": self.submitted,
            "server_report_id": self.server_report_id,
        }


@dataclass
class FeedbackReport:
    """Base class for all feedback reports."""
    metadata: ReportMetadata = field(default_factory=ReportMetadata)
    system_info: SystemInfo = field(default_factory=SystemInfo)
    feedback_type: FeedbackType = FeedbackType.COMMENT

    # Core content (always collected)
    summary: str = ""  # One-line summary
    description: str = ""  # Detailed description

    # Session context (if available)
    session_id: str | None = None
    project_name: str | None = None  # Anonymized if privacy < FULL

    # Attachments (paths to local files, contents collected on submit)
    attachment_paths: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "metadata": self.metadata.to_dict(),
            "system_info": self.system_info.to_dict(),
            "feedback_type": self.feedback_type.value,
            "summary": self.summary,
            "description": self.description,
            "session_id": self.session_id,
            "project_name": self.project_name,
            "attachment_paths": self.attachment_paths,
        }


@dataclass
class BugReport(FeedbackReport):
    """Bug report with structured reproduction steps."""
    feedback_type: FeedbackType = field(default=FeedbackType.BUG)

    # Bug-specific fields
    severity: Severity = Severity.MEDIUM

    # Reproduction information
    steps_to_reproduce: str = ""
    expected_behavior: str = ""
    actual_behavior: str = ""

    # Error context (privacy-level dependent)
    error_message: str = ""
    error_traceback: str = ""  # Full level only

    # Command/prompt context (privacy-level dependent)
    command_used: str = ""  # The obra command that was run
    objective: str = ""      # The task objective (truncated based on privacy)
    prompt_excerpt: str = ""  # Truncated prompt (standard) or full (full level)

    # Observability data (privacy-level dependent)
    # Events from hybrid.jsonl and server session events
    observability_events: list[dict[str, Any]] = field(default_factory=list)
    # Console output log (auto-captured from session)
    console_log: str = ""

    # Workaround (helps prioritize)
    workaround: str = ""

    # Frequency
    frequency: str = ""  # "always", "sometimes", "once"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        base = super().to_dict()
        base.update({
            "severity": self.severity.value,
            "steps_to_reproduce": self.steps_to_reproduce,
            "expected_behavior": self.expected_behavior,
            "actual_behavior": self.actual_behavior,
            "error_message": self.error_message,
            "error_traceback": self.error_traceback,
            "command_used": self.command_used,
            "objective": self.objective,
            "prompt_excerpt": self.prompt_excerpt,
            "observability_events": self.observability_events,
            "console_log": self.console_log,
            "workaround": self.workaround,
            "frequency": self.frequency,
        })
        return base


@dataclass
class FeatureRequest(FeedbackReport):
    """Feature request with use case description."""
    feedback_type: FeedbackType = field(default=FeedbackType.FEATURE)

    # Feature-specific fields
    feature_title: str = ""
    use_case: str = ""  # Why do you need this?
    current_workaround: str = ""  # How do you handle this now?

    # Priority indicators
    business_impact: str = ""  # How would this help your work?
    frequency_of_need: str = ""  # "daily", "weekly", "monthly", "occasionally"

    # Reference (optional)
    similar_tools: str = ""  # Have you seen this in other tools?

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        base = super().to_dict()
        base.update({
            "feature_title": self.feature_title,
            "use_case": self.use_case,
            "current_workaround": self.current_workaround,
            "business_impact": self.business_impact,
            "frequency_of_need": self.frequency_of_need,
            "similar_tools": self.similar_tools,
        })
        return base


@dataclass
class FeedbackComment(FeedbackReport):
    """General feedback, question, or comment."""
    feedback_type: FeedbackType = field(default=FeedbackType.COMMENT)

    # Comment-specific fields
    category: str = ""  # "documentation", "ux", "performance", "other"
    suggestion: str = ""  # Optional improvement suggestion

    # For questions
    question: str = ""
    answered: bool = False
    answer: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        base = super().to_dict()
        base.update({
            "category": self.category,
            "suggestion": self.suggestion,
            "question": self.question,
            "answered": self.answered,
            "answer": self.answer,
        })
        return base
