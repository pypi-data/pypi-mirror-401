"""Beta tester feedback collection system.

This module provides a robust, privacy-respecting feedback system for beta testers
to report bugs, request features, and provide general feedback.

Key Features:
- Multiple privacy levels (full, standard, minimal)
- Automatic system information collection
- Qualitative free-text feedback
- Local draft storage before submission
- Frictionless CLI interface

Privacy Design:
- Users choose what data to share
- Prompts/commands can be truncated or omitted
- Personal data (email) is optional
- All data is encrypted in transit

Example:
    from obra.feedback import FeedbackCollector, PrivacyLevel

    collector = FeedbackCollector(privacy_level=PrivacyLevel.STANDARD)
    report = collector.create_bug_report(
        summary="Orchestrator crashes with spaces in project name",
        steps_to_reproduce="1. Create project with spaces\\n2. Run obra derive",
        expected_behavior="Should handle spaces",
        actual_behavior="Crashes with ValueError",
    )
    result = collector.submit(report)
"""

from obra.feedback.collector import FeedbackCollector
from obra.feedback.models import (
    BugReport,
    FeatureRequest,
    FeedbackComment,
    FeedbackReport,
    FeedbackType,
    PrivacyLevel,
    ReportMetadata,
    Severity,
    SystemInfo,
)
from obra.feedback.observability import ObservabilityCollector
from obra.feedback.sanitizer import DataSanitizer
from obra.feedback.session_logger import (
    SessionConsoleLogger,
    session_logging,
    start_session_logging,
    stop_session_logging,
)

__all__ = [
    # Models
    "BugReport",
    "DataSanitizer",
    "FeatureRequest",
    "FeedbackCollector",
    "FeedbackComment",
    "FeedbackReport",
    "FeedbackType",
    "ObservabilityCollector",
    "PrivacyLevel",
    "ReportMetadata",
    "SessionConsoleLogger",
    "Severity",
    "SystemInfo",
    # Session logging utilities
    "session_logging",
    "start_session_logging",
    "stop_session_logging",
]
