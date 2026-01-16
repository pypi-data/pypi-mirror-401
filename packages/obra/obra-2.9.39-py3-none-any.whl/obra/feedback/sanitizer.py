"""Privacy-aware data sanitization for feedback reports.

This module provides utilities to sanitize sensitive data before
submission, respecting user-chosen privacy levels.

Security Design:
- File paths are normalized to relative paths
- Email addresses in text are redacted
- API keys and tokens are detected and removed
- User names in paths are anonymized
- Project names can be optionally anonymized
"""

import re
from pathlib import Path

from obra.feedback.models import PrivacyLevel


class DataSanitizer:
    """Sanitizes data based on privacy level before submission.

    This class provides methods to redact, truncate, and anonymize
    sensitive information while preserving diagnostic value.
    """

    # Patterns for sensitive data detection
    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    # API_KEY_PATTERN captures prefix in group 1, secret in group 2
    API_KEY_PATTERN = re.compile(r'((?:api[_-]?key|token|secret|password)["\']?\s*[:=]\s*["\']?)([A-Za-z0-9_\-]{20,})', re.IGNORECASE)
    JWT_PATTERN = re.compile(r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+")
    UUID_PATTERN = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.IGNORECASE)

    # Additional secret patterns (S4.T3: Enhanced redaction)
    AWS_KEY_PATTERN = re.compile(r"AKIA[0-9A-Z]{16}")
    GITHUB_TOKEN_PATTERN = re.compile(r"gh[pousr]_[A-Za-z0-9_]{36,}")
    ENV_SECRET_PATTERN = re.compile(r"([A-Z_]+_(?:KEY|TOKEN|SECRET|PASSWORD))=[\S]+")

    # Home directory patterns for different OSes
    HOME_PATTERNS = [
        re.compile(r"/home/[^/\s]+"),          # Linux
        re.compile(r"/Users/[^/\s]+"),          # macOS
        re.compile(r"C:\\Users\\[^\\]+", re.IGNORECASE),  # Windows
        re.compile(r"/mnt/c/Users/[^/\s]+", re.IGNORECASE),  # WSL
    ]

    def __init__(self, privacy_level: PrivacyLevel = PrivacyLevel.STANDARD):
        """Initialize sanitizer with privacy level.

        Args:
            privacy_level: Level of data sanitization to apply
        """
        self.privacy_level = privacy_level

    def sanitize_text(self, text: str, preserve_errors: bool = True) -> str:
        """Sanitize free-form text based on privacy level.

        Args:
            text: Text to sanitize
            preserve_errors: Whether to preserve error messages (useful for debugging)

        Returns:
            Sanitized text
        """
        if not text:
            return text

        if self.privacy_level == PrivacyLevel.FULL:
            # Full level: only redact obvious secrets
            return self._redact_secrets(text)

        if self.privacy_level == PrivacyLevel.MINIMAL:
            # Minimal level: aggressive sanitization
            text = self._redact_secrets(text)
            text = self._redact_emails(text)
            text = self._anonymize_paths(text)
            text = self._truncate(text, max_length=500)
            return text

        # Standard level: balanced sanitization
        text = self._redact_secrets(text)
        text = self._redact_emails(text)
        text = self._anonymize_paths(text)
        return text

    def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize a prompt or command based on privacy level.

        Args:
            prompt: The prompt or command to sanitize

        Returns:
            Sanitized prompt (may be truncated or empty)
        """
        if not prompt:
            return ""

        if self.privacy_level == PrivacyLevel.FULL:
            # Full level: keep entire prompt, just redact secrets
            return self._redact_secrets(prompt)

        if self.privacy_level == PrivacyLevel.MINIMAL:
            # Minimal level: always return truncation message, never actual content
            return f"[Prompt truncated - {len(prompt)} chars total]"

        # Standard level: truncate to first/last 500 chars
        return self._truncate_prompt(prompt, first_chars=500, last_chars=200)

    def sanitize_traceback(self, traceback: str) -> str:
        """Sanitize a Python traceback.

        Args:
            traceback: The traceback string

        Returns:
            Sanitized traceback (empty for minimal level)
        """
        if not traceback:
            return ""

        if self.privacy_level == PrivacyLevel.MINIMAL:
            # Extract just the final exception line
            lines = traceback.strip().split("\n")
            for line in reversed(lines):
                if line.strip() and not line.startswith(" "):
                    return self._anonymize_paths(line)
            return "[Traceback omitted]"

        if self.privacy_level == PrivacyLevel.STANDARD:
            # Anonymize paths but keep structure
            traceback = self._anonymize_paths(traceback)
            # Limit to last 20 lines
            lines = traceback.split("\n")
            if len(lines) > 20:
                traceback = "\n".join(["[... truncated ...]"] + lines[-20:])
            return traceback

        # Full level: anonymize paths only
        return self._anonymize_paths(traceback)

    def sanitize_path(self, path: str) -> str:
        """Sanitize a file path.

        Args:
            path: File path to sanitize

        Returns:
            Sanitized path (relative, anonymized)
        """
        if not path:
            return ""

        # Convert to relative path if possible
        try:
            path_obj = Path(path)
            cwd = Path.cwd()
            if path_obj.is_relative_to(cwd):
                path = str(path_obj.relative_to(cwd))
        except (ValueError, OSError):
            pass

        return self._anonymize_paths(path)

    def sanitize_log_content(self, content: str, max_lines: int | None = None) -> str:
        """Sanitize log file content.

        Args:
            content: Log file content
            max_lines: Maximum number of lines to include (from end)

        Returns:
            Sanitized log content
        """
        if not content:
            return ""

        # Apply line limit based on privacy level
        if max_lines is None:
            max_lines = {
                PrivacyLevel.FULL: 500,
                PrivacyLevel.STANDARD: 100,
                PrivacyLevel.MINIMAL: 20,
            }[self.privacy_level]

        lines = content.split("\n")
        if len(lines) > max_lines:
            content = "\n".join([f"[... {len(lines) - max_lines} lines truncated ...]"] + lines[-max_lines:])

        # Apply standard sanitization
        content = self._redact_secrets(content)
        if self.privacy_level != PrivacyLevel.FULL:
            content = self._anonymize_paths(content)
            content = self._redact_emails(content)

        return content

    def sanitize_objective(self, objective: str) -> str:
        """Sanitize task objective based on privacy level.

        Args:
            objective: The task objective

        Returns:
            Sanitized objective
        """
        if not objective:
            return ""

        if self.privacy_level == PrivacyLevel.MINIMAL:
            # Return only generic description
            return f"[Task objective - {len(objective.split())} words]"

        # Standard and Full: apply text sanitization
        return self.sanitize_text(objective)

    def sanitize_project_name(self, name: str) -> str:
        """Sanitize project name.

        Args:
            name: Project name

        Returns:
            Sanitized project name
        """
        if not name:
            return ""

        if self.privacy_level == PrivacyLevel.MINIMAL:
            return "[project]"

        if self.privacy_level == PrivacyLevel.STANDARD:
            # Hash the project name for correlation without revealing it
            import hashlib
            hash_val = hashlib.sha256(name.encode()).hexdigest()[:8]
            return f"project-{hash_val}"

        return name

    def _redact_secrets(self, text: str) -> str:
        """Redact API keys, tokens, and other secrets."""
        # Redact JWTs first (before generic token pattern)
        text = self.JWT_PATTERN.sub("[JWT_REDACTED]", text)
        # Redact AWS keys (S4.T3)
        text = self.AWS_KEY_PATTERN.sub("[REDACTED_AWS_KEY]", text)
        # Redact GitHub tokens (S4.T3)
        text = self.GITHUB_TOKEN_PATTERN.sub("[REDACTED_GITHUB_TOKEN]", text)
        # Redact API keys and tokens (group 1 = prefix, group 2 = secret)
        text = self.API_KEY_PATTERN.sub(r"\1[REDACTED]", text)
        # Redact environment variable secrets (S4.T3)
        text = self.ENV_SECRET_PATTERN.sub(r"\1=[REDACTED]", text)
        return text

    def _redact_emails(self, text: str) -> str:
        """Redact email addresses."""
        return self.EMAIL_PATTERN.sub("[email]", text)

    def _anonymize_paths(self, text: str) -> str:
        """Anonymize home directory paths."""
        for pattern in self.HOME_PATTERNS:
            text = pattern.sub("~", text)
        return text

    def _truncate(self, text: str, max_length: int) -> str:
        """Truncate text to max length with indicator."""
        if len(text) <= max_length:
            return text
        return text[:max_length] + f"... [{len(text) - max_length} chars truncated]"

    def _truncate_prompt(self, prompt: str, first_chars: int, last_chars: int) -> str:
        """Truncate prompt keeping first and last parts."""
        if len(prompt) <= first_chars + last_chars:
            return self._redact_secrets(self._anonymize_paths(prompt))

        first_part = prompt[:first_chars]
        last_part = prompt[-last_chars:] if last_chars > 0 else ""
        truncated_count = len(prompt) - first_chars - last_chars

        result = f"{first_part}\n\n[... {truncated_count} characters truncated ...]\n\n{last_part}"
        return self._redact_secrets(self._anonymize_paths(result))

    def get_privacy_summary(self) -> dict[str, str]:
        """Get a summary of what data will be collected at current privacy level.

        Returns:
            Dictionary mapping data categories to collection status
        """
        return {
            PrivacyLevel.FULL: {
                "system_info": "Full OS, Python, shell, locale, environment variables",
                "prompts": "Complete prompts and commands",
                "tracebacks": "Full stack traces with anonymized paths",
                "logs": "Up to 500 lines of log content",
                "project_info": "Project name and working directory",
                "session_info": "Session ID and iteration details",
            },
            PrivacyLevel.STANDARD: {
                "system_info": "OS, Python version, terminal type, Obra version",
                "prompts": "First 500 + last 200 characters only",
                "tracebacks": "Last 20 lines with anonymized paths",
                "logs": "Up to 100 lines of log content",
                "project_info": "Hashed project identifier",
                "session_info": "Session ID only",
            },
            PrivacyLevel.MINIMAL: {
                "system_info": "OS type and Obra version only",
                "prompts": "Word count only, no content",
                "tracebacks": "Final error line only",
                "logs": "Up to 20 lines of log content",
                "project_info": "Generic placeholder",
                "session_info": "None",
            },
        }[self.privacy_level]
