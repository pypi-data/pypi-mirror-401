"""Shared review thresholds, patterns, and helper utilities."""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import PurePath

# Complexity tiers for review agent selection.
# - simple: words<=20, files<=2, lines<=50
# - medium: files<=5, lines<=200
# - complex: everything else
COMPLEXITY_THRESHOLDS: dict[str, dict[str, int]] = {
    "simple": {"max_words": 20, "max_files": 2, "max_lines": 50},
    "medium": {"max_files": 5, "max_lines": 200},
    "complex": {},
}

# Filenames that typically warrant security-focused review.
SECURITY_FILENAME_PATTERNS: list[str] = [
    "auth",
    "security",
    "crypto",
    "password",
    "secret",
    "key",
    "token",
    "credential",
    "api",
    "handler",
    "route",
    "endpoint",
    "middleware",
]

# Filenames and directories commonly used for tests.
TEST_FILENAME_PATTERNS: list[str] = [
    "test_",
    "_test",
    "tests",
    "spec",
    "conftest",
]

TEST_DIRECTORY_PATTERNS: list[str] = [
    "tests/",
    "test/",
    "spec/",
    "__tests__/",
]


def _matches_pattern(name: str, patterns: Iterable[str]) -> bool:
    """Return True when the lowercased name contains any given pattern."""
    lowered = name.lower()
    return any(pattern in lowered for pattern in patterns)


def has_security_pattern(filename: str) -> bool:
    """Check if the filename looks security sensitive (case-insensitive)."""
    return _matches_pattern(PurePath(filename).name, SECURITY_FILENAME_PATTERNS)


def has_test_pattern(filepath: str) -> bool:
    """Check if a filepath points to a test file or directory (case-insensitive)."""
    path = PurePath(filepath)
    if _matches_pattern(path.name, TEST_FILENAME_PATTERNS):
        return True

    directory_patterns = [pattern.rstrip("/").lower() for pattern in TEST_DIRECTORY_PATTERNS]
    return any(
        _matches_pattern(part, directory_patterns) for part in path.parts[:-1]
    )
