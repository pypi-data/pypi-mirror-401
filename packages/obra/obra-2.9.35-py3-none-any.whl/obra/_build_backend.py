"""Custom build backend that enforces package isolation.

This module wraps setuptools.build_meta and adds a mandatory check
that prevents building wheels containing imports from src/.

CLAUDE.md Rule 21: The obra/ package must be 100% self-contained.
Any 'from src.' or 'import src.' statements will cause the build to fail.

This check is DETERMINISTIC and UN-BYPASSABLE:
- Runs on every `python -m build` invocation
- Cannot be skipped or worked around
- Fails fast with clear error message

See: ISSUE-SAAS-042, ADR for package isolation
"""

import ast
import sys
from pathlib import Path

# Re-export everything from setuptools.build_meta for PEP 517 compliance
from setuptools.build_meta import *  # noqa: F403
from setuptools.build_meta import build_wheel as _original_build_wheel


def _find_src_imports(file_path: Path) -> list[str]:
    """Find all imports from src in a Python file.

    Returns list of violation descriptions. Empty list means clean.

    NOTE: Unlike the test file, this does NOT allow try/except exceptions.
    Per CLAUDE.md Rule 21: "NEVER add try/except fallbacks for graceful degradation"
    """
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content)
    except (SyntaxError, UnicodeDecodeError):
        return []

    violations = []

    for node in ast.walk(tree):
        # Check: import src or import src.foo
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == "src" or alias.name.startswith("src."):
                    violations.append(f"Line {node.lineno}: import {alias.name}")

        # Check: from src import foo or from src.bar import baz
        elif isinstance(node, ast.ImportFrom):
            if node.module and (node.module == "src" or node.module.startswith("src.")):
                names = ", ".join(a.name for a in node.names)
                violations.append(f"Line {node.lineno}: from {node.module} import {names}")

    return violations


def _check_package_isolation() -> dict[str, list[str]]:
    """Check all obra package files for src imports.

    Returns dict mapping file paths to their violations.
    Empty dict means all clean.
    """
    # Find the obra package root (parent of this file)
    obra_root = Path(__file__).parent

    all_violations = {}

    for py_file in obra_root.rglob("*.py"):
        # Skip test files (not distributed)
        if "/tests/" in str(py_file) or py_file.name.startswith("test_"):
            continue

        # Skip build artifacts
        if "/build/" in str(py_file) or "/dist/" in str(py_file):
            continue

        # Skip this file itself
        if py_file.name == "_build_backend.py":
            continue

        violations = _find_src_imports(py_file)
        if violations:
            # Use relative path for cleaner output
            rel_path = py_file.relative_to(obra_root)
            all_violations[str(rel_path)] = violations

    return all_violations


def _print_violation_report(violations: dict[str, list[str]]) -> None:
    """Print a clear, actionable violation report."""
    print("\n" + "=" * 70, file=sys.stderr)
    print("BUILD FAILED: Package isolation check detected src/ imports", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(file=sys.stderr)
    print("The obra package must be 100% self-contained (CLAUDE.md Rule 21).", file=sys.stderr)
    print("The following files contain imports from src/:", file=sys.stderr)
    print(file=sys.stderr)

    for file_path, file_violations in sorted(violations.items()):
        print(f"  {file_path}:", file=sys.stderr)
        for v in file_violations:
            print(f"    - {v}", file=sys.stderr)

    print(file=sys.stderr)
    print("Fix options:", file=sys.stderr)
    print("  1. Move the required code INTO obra/ (preferred)", file=sys.stderr)
    print("  2. Duplicate the minimal required code", file=sys.stderr)
    print("  3. Remove the import if not needed", file=sys.stderr)
    print(file=sys.stderr)
    print("DO NOT use try/except fallbacks - they mask the problem.", file=sys.stderr)
    print("=" * 70 + "\n", file=sys.stderr)


def build_wheel(wheel_directory, config_settings=None, metadata_directory=None):
    """Build wheel after validating package isolation.

    This is the main entry point called by `python -m build --wheel`.
    The isolation check runs BEFORE any wheel building occurs.
    """
    violations = _check_package_isolation()

    if violations:
        _print_violation_report(violations)
        # Exit with error - do not proceed to build
        sys.exit(1)

    # All clean - proceed with normal build
    return _original_build_wheel(wheel_directory, config_settings, metadata_directory)


def build_sdist(sdist_directory, config_settings=None):
    """Block sdist builds entirely.

    Per IP protection policy, we only distribute wheels (compiled bytecode),
    never source distributions. This prevents source code from being
    published to PyPI.
    """
    print("\n" + "=" * 70, file=sys.stderr)
    print("BUILD FAILED: Source distributions (sdist) are not allowed", file=sys.stderr)
    print("=" * 70, file=sys.stderr)
    print(file=sys.stderr)
    print("The obra package is proprietary and must be distributed as", file=sys.stderr)
    print("wheel-only to protect source code.", file=sys.stderr)
    print(file=sys.stderr)
    print("Use: python -m build --wheel", file=sys.stderr)
    print("Not:  python -m build  (builds both sdist and wheel)", file=sys.stderr)
    print("=" * 70 + "\n", file=sys.stderr)
    sys.exit(1)
