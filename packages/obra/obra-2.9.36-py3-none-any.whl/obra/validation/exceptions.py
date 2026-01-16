"""Custom exceptions for YAML validation in the obra package.

This module defines exceptions raised during YAML validation and sanitization,
providing detailed error context for debugging and user feedback.
"""



class YamlValidationError(ValueError):
    """Exception raised when YAML validation fails after all strategies.

    This exception is raised as the final step in the multi-strategy parsing
    pipeline when:
    1. Strategy 1 (direct parse) fails
    2. Strategy 2 (auto-sanitize) fails
    3. Strategy 3 (fail-fast) is triggered

    The exception provides comprehensive error context including:
    - File path where the error occurred
    - Line number (if available from PyYAML)
    - Original error message from PyYAML
    - Actionable suggestions from YamlSuggestionEngine
    - User guidance on next steps

    Attributes:
        file_path: Path to the YAML file that failed validation
        error_message: Descriptive error message (from PyYAML or custom)
        line_number: Line number where error occurred (None if not available)
        suggestions: List of actionable suggestions for fixing the error
        auto_fix_attempted: Whether auto-sanitization was attempted before failure
    """

    def __init__(
        self,
        file_path: str,
        error_message: str,
        line_number: int | None = None,
        suggestions: list[str] | None = None,
        auto_fix_attempted: bool = False,
    ) -> None:
        """Initialize YamlValidationError.

        Args:
            file_path: Path to the YAML file that failed validation
            error_message: Descriptive error message
            line_number: Line number where error occurred (optional)
            suggestions: List of actionable suggestions (optional)
            auto_fix_attempted: Whether auto-sanitization was attempted (default: False)
        """
        self.file_path = file_path
        self.error_message = error_message
        self.line_number = line_number
        self.suggestions = suggestions or []
        self.auto_fix_attempted = auto_fix_attempted

        # Build comprehensive exception message
        message = self._build_message()
        super().__init__(message)

    def _build_message(self) -> str:
        """Build comprehensive error message with all context.

        Returns:
            Formatted error message with file path, line number, error,
            suggestions, and user guidance
        """
        lines = []

        # Header
        lines.append("YAML validation failed")
        lines.append("")

        # File and location
        lines.append(f"File: {self.file_path}")
        if self.line_number is not None:
            lines.append(f"Line: {self.line_number}")
        lines.append("")

        # Error details
        lines.append("Error:")
        lines.append(f"  {self.error_message}")
        lines.append("")

        # Auto-fix context
        if self.auto_fix_attempted:
            lines.append("Auto-fix was attempted but could not resolve the issue.")
            lines.append("")

        # Suggestions
        if self.suggestions:
            lines.append("Suggestions:")
            for suggestion in self.suggestions:
                lines.append(f"  - {suggestion}")
            lines.append("")

        # User guidance
        lines.append("Next steps:")
        lines.append("  1. Fix the YAML syntax error(s) in the file and retry")
        lines.append("  2. OR provide a natural language prompt with full context instead of YAML")
        lines.append("")
        lines.append("For YAML syntax help, see: https://yaml.org/spec/1.2/spec.html")

        return "\n".join(lines)


__all__ = ["YamlValidationError"]
