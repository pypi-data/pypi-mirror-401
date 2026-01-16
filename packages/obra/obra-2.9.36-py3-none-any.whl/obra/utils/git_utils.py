"""Git utility functions for Obra SaaS CLI.

Provides git repository detection and validation for hybrid orchestration.
This module is duplicated from src/utils/git_utils.py per Rule 21 (Package Isolation).

GIT-HARD-001: Centralized git validation for SaaS CLI package.
"""

import logging
import subprocess
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


# Default .gitignore content for auto-initialized repositories
_DEFAULT_GITIGNORE = """\
# Environment and secrets
.env
.env.*

# Python bytecode
*.pyc
__pycache__/

# Obra logs and runtime
.obra/logs/
*.log

# OS-specific
.DS_Store
"""


def is_git_repository(path: Union[str, Path]) -> bool:
    """Check if path is within a git repository.

    Checks for .git directory in the given path or any parent directory.

    Args:
        path: Directory path to check

    Returns:
        True if path is within a git repository, False otherwise

    Example:
        >>> is_git_repository("/home/user/my-project")
        True  # if /home/user/my-project/.git exists
        >>> is_git_repository("/tmp/scratch")
        False  # no .git in path or parents
    """
    path = Path(path).resolve()

    # Check if .git exists in this directory
    if (path / ".git").exists():
        return True

    # Check parent directories
    for parent in path.parents:
        if (parent / ".git").exists():
            return True

    return False


def ensure_git_repository(
    path: Union[str, Path],
    auto_init: bool = False,
) -> bool:
    """Ensure path is or becomes a git repository.

    Checks if the path is a git repository. If not and auto_init is True,
    initializes a new git repository with a default .gitignore file.

    GIT-HARD-001: Provides centralized git validation for SaaS CLI.

    Args:
        path: Directory path to check/initialize
        auto_init: If True, auto-initialize git when not in a repository.
                   If False, raise GitValidationError when not in a repository.

    Returns:
        True if the path is (or became) a git repository

    Raises:
        GitValidationError: If not in a git repository and auto_init is False
        subprocess.CalledProcessError: If git init fails

    Example:
        >>> ensure_git_repository("/home/user/my-project", auto_init=True)
        True  # Initialized git and created .gitignore
        >>> ensure_git_repository("/home/user/git-project", auto_init=False)
        True  # Already a git repo
        >>> ensure_git_repository("/tmp/scratch", auto_init=False)
        GitValidationError  # Not a git repo, auto_init disabled
    """
    path = Path(path).resolve()

    # Check if already in a git repository
    if is_git_repository(path):
        logger.debug("Path is already a git repository: %s", path)
        return True

    # Not in a git repo - handle based on auto_init setting
    if not auto_init:
        raise GitValidationError(path)

    # Auto-initialize git repository
    logger.info("Auto-initializing git repository: %s", path)

    try:
        # Run git init
        result = subprocess.run(
            ["git", "init"],
            cwd=path,
            capture_output=True,
            text=True,
            check=True,
        )
        logger.debug("git init output: %s", result.stdout.strip())

        # Create default .gitignore if it doesn't exist
        gitignore_path = path / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text(_DEFAULT_GITIGNORE)
            logger.info("Created default .gitignore: %s", gitignore_path)

        logger.info("Git repository initialized successfully: %s", path)
        return True

    except subprocess.CalledProcessError as e:
        logger.error("Failed to initialize git repository: %s", e.stderr)
        raise


class GitValidationError(Exception):
    """Error raised when git repository validation fails.

    Provides clear error message following R7 template with actionable recovery steps.

    GIT-HARD-001: User-facing error for missing git repositories.
    """

    def __init__(self, path: Union[str, Path]):
        """Initialize GitValidationError.

        Args:
            path: Path that failed git validation
        """
        self.path = Path(path).resolve()

        # R7 template: Clear error with 3 fix options and help link
        message = (
            f"GitValidationError: Git repository required\n"
            f"  Location: {self.path}\n"
            f"\n"
            f"  To fix:\n"
            f"    1. Initialize git: cd {self.path} && git init\n"
            f"    2. Skip this session: obra run --skip-git-check \"your objective\"\n"
            f"    3. Skip always: Add 'llm.git.skip_check: true' to config\n"
            f"\n"
            f"  More info: obra help git"
        )
        super().__init__(message)
