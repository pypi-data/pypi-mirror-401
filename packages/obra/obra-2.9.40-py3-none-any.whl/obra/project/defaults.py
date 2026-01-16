"""Default file templates for Obra projects.

This module provides templates and utilities for initializing Obra-managed
projects with the correct configuration files.
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Default CLAUDE.md template for Obra-managed projects
# Source: docs/design/briefs/CUSTOMER_CLAUDE_META_FILE_STRATEGY_BRIEF.md
DEFAULT_OBRA_CLAUDE_MD = """# Obra Operational Requirements

This Claude session is orchestrated by Obra. These rules ensure predictable,
safe, autonomous operation across all Obra installations.

---

## Tool Behavior (Critical)

You MUST NOT use:
- AskUserQuestion or any interactive question tools
- EnterPlanMode - describe plans in plain text instead

Instead:
- Ask clarifying questions in plain text
- Present options as numbered lists (user replies with number or text)
- Make autonomous decisions from task context
- If truly blocked, explain what's needed in your response

## Execution Mode

You are running as an automated subprocess with NO stdin (headless mode).
- State assumptions and proceed autonomously
- Do not pause for user confirmation
- Make reasonable decisions from task context

## Planning Standards

- NEVER include time estimates ("2-3 days", "4 hours", etc.)
- Use Story/Task hierarchy, not "Phase 1, Phase 2"
- Describe plans in plain text, not plan mode
- Break large work into smaller tasks instead of estimating duration

## Security Rules

- Do NOT create, modify, or delete files outside the project directory
- NEVER output secrets, API keys, or credentials in responses
- NEVER hardcode secrets in code (use environment variables)
- Validate paths before file operations
- NEVER run destructive commands (rm -rf, DROP TABLE, force push, etc.) - refuse and explain why

## Code Quality

- Use appropriate type annotations for the language (TypeScript types, Python hints, etc.)
- No security vulnerabilities (injection, path traversal, XSS, etc.)
- Run existing tests before committing (if test suite exists)
- Prefer editing existing files over creating new ones

## Output Standards

- No emojis in responses or generated code (unless explicitly requested)
- Keep responses concise and actionable
- Do NOT create documentation files (*.md, README) unless explicitly requested

---

#### User Settings

Add your project-specific instructions below:

"""


def ensure_obra_claude_md(workspace_path: Path) -> Path:
    """Ensure .obra/CLAUDE.md exists with default content.

    Creates the `.obra/` directory and `.obra/CLAUDE.md` file if they don't exist.
    This follows additive-only behavior - existing files are NEVER overwritten.

    Args:
        workspace_path: Path to the workspace/project root directory

    Returns:
        Path to .obra/CLAUDE.md file

    Raises:
        OSError: If directory or file creation fails
    """
    obra_dir = workspace_path / ".obra"
    claude_md_path = obra_dir / "CLAUDE.md"

    # Ensure .obra directory exists
    obra_dir.mkdir(parents=True, exist_ok=True)

    # Create CLAUDE.md only if it doesn't exist
    if not claude_md_path.exists():
        claude_md_path.write_text(DEFAULT_OBRA_CLAUDE_MD, encoding="utf-8")
        logger.info(f"Created {claude_md_path}")
    else:
        logger.debug(f"CLAUDE.md already exists at {claude_md_path}")

    return claude_md_path
