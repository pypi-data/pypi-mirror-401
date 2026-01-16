"""Prompt templates for LLM-based review agents.

This package contains prompt templates used by review agents for
LLM-based code analysis. Each agent type has its own template file.

Template Files:
    - security_sweep.txt: Fast-tier security scan
    - security_deep.txt: High-tier deep security analysis
    - testing_coverage.txt: Test coverage gap detection
    - code_quality.txt: Code quality analysis
    - docs_analysis.txt: Documentation quality analysis

Output Format:
    All templates require structured text output in this format:

    ISSUE: <ID like SEC-001, TEST-002, etc.>
    FILE: <exact file path>
    LINE: <line number>
    SEVERITY: <S0=critical, S1=high, S2=medium, S3=low>
    CONFIDENCE: <high/medium/low>
    WHY_BUG: <explain why this is wrong>
    FAILING_SCENARIO: <concrete input, state, or sequence that triggers the bug>
    SUGGESTED_FIX: <minimal code change or test>
    NEEDS_DEEP_REVIEW: <yes/no>
    ---

Related:
    - obra/agents/base.py (BaseAgent.parse_structured_response)
    - docs/design/briefs/LLM_AGENT_REFACTOR_BRIEF.md
"""

from pathlib import Path

# Directory containing prompt templates
PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str) -> str:
    """Load a prompt template by name.

    Args:
        name: Template name (without .txt extension)

    Returns:
        Template content as string

    Raises:
        FileNotFoundError: If template does not exist
    """
    template_path = PROMPTS_DIR / f"{name}.txt"
    if not template_path.exists():
        msg = f"Prompt template not found: {name}"
        raise FileNotFoundError(msg)
    return template_path.read_text(encoding="utf-8")


__all__ = ["PROMPTS_DIR", "load_prompt"]
