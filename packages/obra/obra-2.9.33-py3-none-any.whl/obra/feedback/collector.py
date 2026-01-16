"""Feedback collection and submission system.

This module provides the main FeedbackCollector class that handles:
- Creating feedback reports with appropriate context
- Local draft storage for offline/interrupted submissions
- Submission to the Obra backend
- Attachment handling with size limits
"""

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

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

logger = logging.getLogger(__name__)


class FeedbackCollector:
    """Collects and submits beta tester feedback.

    This class provides a high-level interface for creating, storing,
    and submitting feedback reports while respecting privacy settings.

    Example:
        collector = FeedbackCollector(privacy_level=PrivacyLevel.STANDARD)

        # Create a bug report
        report = collector.create_bug_report(
            summary="Orchestrator crashes with spaces",
            severity=Severity.HIGH,
            steps_to_reproduce="1. Create project\\n2. Run deriva",
        )

        # Preview what will be sent
        preview = collector.preview_submission(report)

        # Submit
        result = collector.submit(report)
    """

    # Maximum attachment size (5MB)
    MAX_ATTACHMENT_SIZE = 5 * 1024 * 1024

    # Maximum total attachments size (10MB)
    MAX_TOTAL_ATTACHMENTS_SIZE = 10 * 1024 * 1024

    # Drafts directory
    DRAFTS_DIR = Path.home() / ".obra" / "feedback" / "drafts"

    def __init__(
        self,
        privacy_level: PrivacyLevel = PrivacyLevel.STANDARD,
        user_id: str | None = None,
        email: str | None = None,
    ):
        """Initialize feedback collector.

        Args:
            privacy_level: Level of data to collect and share
            user_id: Firebase user ID (if authenticated)
            email: User email for follow-up (optional)
        """
        self.privacy_level = privacy_level
        self.user_id = user_id
        self.email = email
        self.sanitizer = DataSanitizer(privacy_level)

        # Ensure drafts directory exists
        self.DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    def create_bug_report(
        self,
        summary: str,
        severity: Severity = Severity.MEDIUM,
        description: str = "",
        steps_to_reproduce: str = "",
        expected_behavior: str = "",
        actual_behavior: str = "",
        error_message: str = "",
        error_traceback: str = "",
        command_used: str = "",
        objective: str = "",
        prompt_excerpt: str = "",
        workaround: str = "",
        frequency: str = "",
        session_id: str | None = None,
        project_name: str | None = None,
        attachment_paths: list[str] | None = None,
        include_observability: bool = True,
    ) -> BugReport:
        """Create a bug report with automatic context collection.

        Args:
            summary: One-line bug summary (required)
            severity: Bug severity level
            description: Detailed description
            steps_to_reproduce: Steps to reproduce the bug
            expected_behavior: What should happen
            actual_behavior: What actually happens
            error_message: Error message if any
            error_traceback: Full traceback if available
            command_used: The obra command that triggered the bug
            objective: The task objective being worked on
            prompt_excerpt: Relevant prompt excerpt
            workaround: Known workaround if any
            frequency: How often the bug occurs
            session_id: Obra session ID if available
            project_name: Project name (will be sanitized)
            attachment_paths: Paths to files to attach
            include_observability: Whether to collect observability events (default True)

        Returns:
            BugReport instance ready for submission
        """
        # Collect observability data if enabled and privacy allows
        observability_events: list[dict[str, Any]] = []
        console_log: str = ""
        if include_observability and self.privacy_level != PrivacyLevel.MINIMAL:
            try:
                obs_collector = ObservabilityCollector(
                    privacy_level=self.privacy_level,
                    session_id=session_id,
                )
                observability_events = obs_collector.get_sanitized_events()
                console_log = obs_collector.get_session_console_log()
                logger.debug(
                    f"Collected {len(observability_events)} events, "
                    f"{len(console_log)} chars console log"
                )
            except Exception as e:
                logger.warning(f"Failed to collect observability data: {e}")

        report = BugReport(
            metadata=self._create_metadata(),
            system_info=SystemInfo.collect(self.privacy_level),
            summary=summary,
            description=self.sanitizer.sanitize_text(description),
            severity=severity,
            steps_to_reproduce=self.sanitizer.sanitize_text(steps_to_reproduce),
            expected_behavior=self.sanitizer.sanitize_text(expected_behavior),
            actual_behavior=self.sanitizer.sanitize_text(actual_behavior),
            error_message=self.sanitizer.sanitize_text(error_message),
            error_traceback=self.sanitizer.sanitize_traceback(error_traceback),
            command_used=self.sanitizer.sanitize_text(command_used),
            objective=self.sanitizer.sanitize_objective(objective),
            prompt_excerpt=self.sanitizer.sanitize_prompt(prompt_excerpt),
            observability_events=observability_events,
            console_log=console_log,
            workaround=self.sanitizer.sanitize_text(workaround),
            frequency=frequency,
            session_id=session_id if self.privacy_level != PrivacyLevel.MINIMAL else None,
            project_name=self.sanitizer.sanitize_project_name(project_name or ""),
            attachment_paths=attachment_paths or [],
        )

        # Auto-save draft
        self._save_draft(report)

        return report

    def create_feature_request(
        self,
        feature_title: str,
        use_case: str = "",
        description: str = "",
        current_workaround: str = "",
        business_impact: str = "",
        frequency_of_need: str = "",
        similar_tools: str = "",
    ) -> FeatureRequest:
        """Create a feature request.

        Args:
            feature_title: Short title for the feature (required)
            use_case: Why do you need this feature?
            description: Detailed description of the feature
            current_workaround: How do you handle this now?
            business_impact: How would this help your work?
            frequency_of_need: How often would you use this?
            similar_tools: Have you seen this in other tools?

        Returns:
            FeatureRequest instance ready for submission
        """
        report = FeatureRequest(
            metadata=self._create_metadata(),
            system_info=SystemInfo.collect(self.privacy_level),
            summary=feature_title,
            feature_title=feature_title,
            description=self.sanitizer.sanitize_text(description),
            use_case=self.sanitizer.sanitize_text(use_case),
            current_workaround=self.sanitizer.sanitize_text(current_workaround),
            business_impact=self.sanitizer.sanitize_text(business_impact),
            frequency_of_need=frequency_of_need,
            similar_tools=self.sanitizer.sanitize_text(similar_tools),
        )

        self._save_draft(report)
        return report

    def create_comment(
        self,
        summary: str,
        description: str = "",
        category: str = "",
        suggestion: str = "",
        feedback_type: FeedbackType = FeedbackType.COMMENT,
    ) -> FeedbackComment:
        """Create a general comment or question.

        Args:
            summary: One-line summary (required)
            description: Detailed description
            category: Category (documentation, ux, performance, other)
            suggestion: Improvement suggestion
            feedback_type: Type of feedback (comment, question, praise)

        Returns:
            FeedbackComment instance ready for submission
        """
        report = FeedbackComment(
            metadata=self._create_metadata(),
            system_info=SystemInfo.collect(self.privacy_level),
            feedback_type=feedback_type,
            summary=summary,
            description=self.sanitizer.sanitize_text(description),
            category=category,
            suggestion=self.sanitizer.sanitize_text(suggestion),
        )

        self._save_draft(report)
        return report

    def preview_submission(self, report: FeedbackReport) -> dict[str, Any]:
        """Preview what data will be submitted.

        Use this to show users exactly what will be sent before submission.

        Args:
            report: The report to preview

        Returns:
            Dictionary showing all data that will be submitted
        """
        data = report.to_dict()

        # Add attachment info without actual content
        if report.attachment_paths:
            attachments_info = []
            for path in report.attachment_paths:
                path_obj = Path(path)
                if path_obj.exists():
                    size = path_obj.stat().st_size
                    attachments_info.append({
                        "name": path_obj.name,
                        "size_bytes": size,
                        "will_include": size <= self.MAX_ATTACHMENT_SIZE,
                    })
                else:
                    attachments_info.append({
                        "name": path,
                        "error": "File not found",
                        "will_include": False,
                    })
            data["attachments_preview"] = attachments_info

        # Add privacy level info
        data["privacy_level_description"] = self.privacy_level.description
        data["data_collection_summary"] = self.sanitizer.get_privacy_summary()

        return data

    def submit(self, report: FeedbackReport) -> dict[str, Any]:
        """Submit feedback report to the Obra backend.

        Args:
            report: The report to submit

        Returns:
            Dictionary with submission result:
            - success: bool
            - report_id: str (server-assigned ID)
            - message: str
        """
        try:
            # Prepare submission data
            submission_data = self._prepare_submission(report)

            # Try to submit - use authenticated client if available, otherwise anonymous
            try:
                result = self._submit_to_server(submission_data)

                # Update report metadata
                report.metadata.submitted = True
                report.metadata.submitted_at = datetime.now(UTC).isoformat()
                report.metadata.server_report_id = result.get("report_id")

                # Remove draft
                self._remove_draft(report.metadata.report_id)

                return {
                    "success": True,
                    "report_id": result.get("report_id", report.metadata.report_id),
                    "message": "Feedback submitted successfully. Thank you!",
                }

            except Exception as api_error:
                logger.warning(f"API submission failed: {api_error}")
                # Fall back to local storage
                return self._store_locally(report, submission_data)

        except Exception as e:
            logger.error(f"Feedback submission failed: {e}")
            return {
                "success": False,
                "report_id": report.metadata.report_id,
                "message": f"Submission failed: {e}",
                "stored_locally": True,
            }

    def list_drafts(self) -> list[dict[str, Any]]:
        """List all saved draft reports.

        Returns:
            List of draft summaries
        """
        drafts = []
        for draft_file in self.DRAFTS_DIR.glob("*.json"):
            try:
                with open(draft_file, encoding="utf-8") as f:
                    data = json.load(f)
                    drafts.append({
                        "report_id": data.get("metadata", {}).get("report_id"),
                        "type": data.get("feedback_type"),
                        "summary": data.get("summary", "")[:80],
                        "created_at": data.get("metadata", {}).get("created_at"),
                        "path": str(draft_file),
                    })
            except Exception as e:
                logger.warning(f"Failed to read draft {draft_file}: {e}")
        return sorted(drafts, key=lambda x: x.get("created_at", ""), reverse=True)

    def load_draft(self, report_id: str) -> FeedbackReport | None:
        """Load a draft report by ID.

        Args:
            report_id: The report ID to load

        Returns:
            FeedbackReport instance or None if not found
        """
        draft_path = self.DRAFTS_DIR / f"{report_id}.json"
        if not draft_path.exists():
            return None

        try:
            with open(draft_path, encoding="utf-8") as f:
                data = json.load(f)
            return self._dict_to_report(data)
        except Exception as e:
            logger.error(f"Failed to load draft {report_id}: {e}")
            return None

    def delete_draft(self, report_id: str) -> bool:
        """Delete a draft report.

        Args:
            report_id: The report ID to delete

        Returns:
            True if deleted, False if not found
        """
        return self._remove_draft(report_id)

    def _submit_to_server(self, submission_data: dict[str, Any]) -> dict[str, Any]:
        """Submit feedback to server, preserving auth when possible.

        Strategy:
        1. Try fully authenticated submission via APIClient
        2. If auth setup fails, try with whatever token we have (let server decide)
        3. Fall back to anonymous only if no token available

        Args:
            submission_data: Prepared feedback data

        Returns:
            Server response dict with success, report_id, message

        Raises:
            Exception: If all submission attempts fail
        """
        import requests

        feedback_url = "https://us-central1-obra-205b0.cloudfunctions.net/feedback"

        # Try authenticated submission first
        try:
            from obra.api import APIClient
            client = APIClient.from_config()
            return client.submit_feedback(submission_data)
        except Exception as auth_error:
            logger.debug(f"APIClient auth failed: {auth_error}")

        # Auth setup failed - try with raw token from config (even if expired)
        # Server may still accept it or handle gracefully
        auth_token = self._get_raw_auth_token()
        headers = {"Content-Type": "application/json"}
        if auth_token:
            headers["Authorization"] = f"Bearer {auth_token}"
            logger.debug("Submitting feedback with raw token (may be expired)")
        else:
            logger.debug("No auth token available, submitting anonymously")

        try:
            response = requests.post(
                feedback_url,
                json=submission_data,
                headers=headers,
                timeout=60,
            )

            if response.status_code == 201:
                return response.json()
            if response.status_code == 429:
                raise Exception("Rate limit exceeded. Please try again later.")
            error_data = response.json() if response.text else {}
            raise Exception(
                error_data.get("error", f"Server returned {response.status_code}")
            )

        except requests.RequestException as e:
            raise Exception(f"Network error: {e}") from e

    def _get_raw_auth_token(self) -> str | None:
        """Get auth token from config without validation.

        Used for feedback submission when normal auth flow fails.
        Returns token even if expired - let server decide validity.
        """
        try:
            import yaml
            config_path = Path.home() / ".obra" / "client-config.yaml"
            if config_path.exists():
                with open(config_path, encoding="utf-8") as f:
                    config = yaml.safe_load(f) or {}
                return config.get("auth_token")
        except Exception as e:
            logger.debug(f"Failed to read auth token: {e}")
        return None

    def _create_metadata(self) -> ReportMetadata:
        """Create metadata for a new report."""
        return ReportMetadata(
            privacy_level=self.privacy_level,
            user_id=self.user_id,
            email=self.email,
            anonymous=not (self.user_id or self.email),
        )

    def _save_draft(self, report: FeedbackReport) -> None:
        """Save report as draft for later submission."""
        try:
            draft_path = self.DRAFTS_DIR / f"{report.metadata.report_id}.json"
            with open(draft_path, "w", encoding="utf-8") as f:
                json.dump(report.to_dict(), f, indent=2)
            logger.debug(f"Draft saved: {draft_path}")
        except Exception as e:
            logger.warning(f"Failed to save draft: {e}")

    def _remove_draft(self, report_id: str) -> bool:
        """Remove a draft file."""
        draft_path = self.DRAFTS_DIR / f"{report_id}.json"
        if draft_path.exists():
            try:
                draft_path.unlink()
                return True
            except Exception as e:
                logger.warning(f"Failed to remove draft: {e}")
        return False

    def _load_feedback_config(self) -> dict[str, Any]:
        """Load feedback configuration.

        Returns:
            Feedback config dictionary
        """
        # Load default config
        obra_root = Path(__file__).parent.parent
        default_config_path = obra_root / "config" / "defaults" / "feedback.yaml"

        if not default_config_path.exists():
            logger.warning(f"Default feedback config not found: {default_config_path}")
            return {"data_level": "minimal"}

        with open(default_config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f) or {}

        # Check for customer override
        customer_config_path = Path.cwd() / ".obra" / "config" / "feedback.yaml"
        if customer_config_path.exists():
            with open(customer_config_path, "r", encoding="utf-8") as f:
                customer_config = yaml.safe_load(f) or {}
                config.update(customer_config)

        return config

    def _filter_by_data_level(self, data: dict[str, Any]) -> dict[str, Any]:
        """Filter submission data based on data_level config (S4.T5).

        Args:
            data: Full report data dictionary

        Returns:
            Filtered data dictionary with only allowed fields
        """
        try:
            config = self._load_feedback_config()
            data_level = config.get("data_level", "minimal")
            allowed_fields = config.get("data_fields", {}).get(data_level, [])

            if not allowed_fields:
                # Fallback to minimal if config is missing
                allowed_fields = [
                    "feedback_type",
                    "description",
                    "obra_version",
                    "timestamp",
                    "platform",
                    "python_version",
                ]

            # Start with empty result
            filtered = {}

            # Map config field names to data structure
            field_mapping = {
                "feedback_type": ("feedback_type",),
                "description": ("description",),
                "obra_version": ("system_info", "obra_version"),
                "timestamp": ("metadata", "created_at"),
                "platform": ("system_info", "os_type"),
                "python_version": ("system_info", "python_version"),
                "session_id": ("session_id",),
                "stack_trace": ("error_traceback",),
                "environment": ("environment_info",),
                "recent_logs": ("log_excerpt",),
                "command_history": ("command_used",),
                "active_task_id": ("task_id",),
            }

            # Always include metadata and system_info structures
            filtered["metadata"] = data.get("metadata", {})
            filtered["system_info"] = {}

            # Add allowed fields
            for field in allowed_fields:
                if field in field_mapping:
                    path = field_mapping[field]
                    if len(path) == 1:
                        # Top-level field
                        key = path[0]
                        if key in data:
                            filtered[key] = data[key]
                    elif len(path) == 2:
                        # Nested field
                        section, key = path
                        if section in data and key in data[section]:
                            if section not in filtered:
                                filtered[section] = {}
                            filtered[section][key] = data[section][key]

            # Always include summary if present (for bugs)
            if "summary" in data:
                filtered["summary"] = data["summary"]

            return filtered

        except Exception as e:
            logger.warning(f"Data level filtering failed: {e}, using full data")
            return data

    def _prepare_submission(self, report: FeedbackReport) -> dict[str, Any]:
        """Prepare report data for submission including attachments."""
        data = report.to_dict()

        # Apply data_level filtering (S4.T5)
        data = self._filter_by_data_level(data)

        # Process attachments
        if report.attachment_paths:
            attachments = []
            total_size = 0

            for path_str in report.attachment_paths:
                path = Path(path_str)
                if not path.exists():
                    logger.warning(f"Attachment not found: {path}")
                    continue

                size = path.stat().st_size
                if size > self.MAX_ATTACHMENT_SIZE:
                    logger.warning(f"Attachment too large ({size} bytes): {path}")
                    continue

                if total_size + size > self.MAX_TOTAL_ATTACHMENTS_SIZE:
                    logger.warning(f"Total attachments size exceeded, skipping: {path}")
                    break

                try:
                    # Read and sanitize log content
                    content = path.read_text(encoding="utf-8", errors="replace")
                    if path.suffix in [".log", ".txt", ".json", ".yaml", ".yml"]:
                        content = self.sanitizer.sanitize_log_content(content)

                    attachments.append({
                        "name": path.name,
                        "content": content,
                        "size": len(content),
                        "type": path.suffix,
                    })
                    total_size += size
                except Exception as e:
                    logger.warning(f"Failed to read attachment {path}: {e}")

            data["attachments"] = attachments

        # Remove attachment paths (we've processed them)
        data.pop("attachment_paths", None)

        return data

    def _store_locally(
        self, report: FeedbackReport, submission_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Store feedback locally when API submission fails.

        This ensures feedback is never lost even if the server is unreachable.
        """
        try:
            pending_dir = Path.home() / ".obra" / "feedback" / "pending"
            pending_dir.mkdir(parents=True, exist_ok=True)

            pending_path = pending_dir / f"{report.metadata.report_id}.json"
            with open(pending_path, "w", encoding="utf-8") as f:
                json.dump(submission_data, f, indent=2)

            return {
                "success": True,
                "report_id": report.metadata.report_id,
                "message": "Feedback stored locally (will sync when online).",
                "stored_locally": True,
                "local_path": str(pending_path),
            }
        except Exception as e:
            return {
                "success": False,
                "report_id": report.metadata.report_id,
                "message": f"Failed to store feedback: {e}",
            }

    def _dict_to_report(self, data: dict[str, Any]) -> FeedbackReport:
        """Convert dictionary back to appropriate report type."""
        feedback_type = data.get("feedback_type", "comment")

        # Reconstruct metadata
        meta_data = data.get("metadata", {})
        metadata = ReportMetadata(
            report_id=meta_data.get("report_id", ""),
            created_at=meta_data.get("created_at", ""),
            submitted_at=meta_data.get("submitted_at"),
            privacy_level=PrivacyLevel(meta_data.get("privacy_level", "standard")),
            user_id=meta_data.get("user_id"),
            email=meta_data.get("email"),
            anonymous=meta_data.get("anonymous", True),
            submitted=meta_data.get("submitted", False),
            server_report_id=meta_data.get("server_report_id"),
        )

        # Reconstruct system info
        sys_data = data.get("system_info", {})
        system_info = SystemInfo(
            obra_version=sys_data.get("obra_version", ""),
            os_type=sys_data.get("os_type", ""),
            os_version=sys_data.get("os_version", ""),
            python_version=sys_data.get("python_version", ""),
            terminal_type=sys_data.get("terminal_type", ""),
            installation_method=sys_data.get("installation_method", ""),
            shell=sys_data.get("shell", ""),
            locale=sys_data.get("locale", ""),
            environment_vars=sys_data.get("environment_vars", {}),
            llm_provider=sys_data.get("llm_provider", ""),
            llm_model=sys_data.get("llm_model", ""),
        )

        if feedback_type == "bug":
            return BugReport(
                metadata=metadata,
                system_info=system_info,
                summary=data.get("summary", ""),
                description=data.get("description", ""),
                severity=Severity(data.get("severity", "medium")),
                steps_to_reproduce=data.get("steps_to_reproduce", ""),
                expected_behavior=data.get("expected_behavior", ""),
                actual_behavior=data.get("actual_behavior", ""),
                error_message=data.get("error_message", ""),
                error_traceback=data.get("error_traceback", ""),
                command_used=data.get("command_used", ""),
                objective=data.get("objective", ""),
                prompt_excerpt=data.get("prompt_excerpt", ""),
                observability_events=data.get("observability_events", []),
                console_log=data.get("console_log", ""),
                workaround=data.get("workaround", ""),
                frequency=data.get("frequency", ""),
                session_id=data.get("session_id"),
                project_name=data.get("project_name"),
                attachment_paths=data.get("attachment_paths", []),
            )

        if feedback_type == "feature":
            return FeatureRequest(
                metadata=metadata,
                system_info=system_info,
                summary=data.get("summary", ""),
                description=data.get("description", ""),
                feature_title=data.get("feature_title", ""),
                use_case=data.get("use_case", ""),
                current_workaround=data.get("current_workaround", ""),
                business_impact=data.get("business_impact", ""),
                frequency_of_need=data.get("frequency_of_need", ""),
                similar_tools=data.get("similar_tools", ""),
            )

        return FeedbackComment(
            metadata=metadata,
            system_info=system_info,
            feedback_type=FeedbackType(feedback_type),
            summary=data.get("summary", ""),
            description=data.get("description", ""),
            category=data.get("category", ""),
            suggestion=data.get("suggestion", ""),
            question=data.get("question", ""),
            answered=data.get("answered", False),
            answer=data.get("answer", ""),
        )

    def sync_pending(self) -> dict[str, Any]:
        """Attempt to sync any locally stored feedback.

        Call this periodically or when connectivity is restored.

        Returns:
            Dictionary with sync results
        """
        pending_dir = Path.home() / ".obra" / "feedback" / "pending"
        if not pending_dir.exists():
            return {"synced": 0, "failed": 0, "remaining": 0}

        synced = 0
        failed = 0
        remaining = 0

        try:
            from obra.api import APIClient
            client = APIClient.from_config()

            for pending_file in pending_dir.glob("*.json"):
                try:
                    with open(pending_file, encoding="utf-8") as f:
                        data = json.load(f)

                    result = client.submit_feedback(data)

                    if result.get("success"):
                        pending_file.unlink()
                        synced += 1
                    else:
                        failed += 1

                except Exception as e:
                    logger.warning(f"Failed to sync {pending_file}: {e}")
                    failed += 1

            remaining = len(list(pending_dir.glob("*.json")))

        except Exception as e:
            logger.warning(f"Sync failed (no API access): {e}")
            remaining = len(list(pending_dir.glob("*.json")))

        return {"synced": synced, "failed": failed, "remaining": remaining}
