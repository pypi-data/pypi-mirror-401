"""Input type detection for intent generation.

This module provides classification of user input to determine
the appropriate intent generation strategy:
- vague_nl: Short, underspecified natural language (~2-5s LLM)
- rich_nl: Detailed natural language description (~2-5s LLM)
- prd: Product requirements document (~2-5s LLM extraction)
- prose_plan: Unstructured plan document (~2-5s LLM extraction)
- structured_plan: MACHINE_PLAN JSON/YAML (~0ms mechanical)

And project state detection:
- EMPTY: New/minimal project (<5 meaningful files)
- EXISTING: Established project with codebase (>50 files or LLM classification)

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - docs/design/briefs/AUTO_INTENT_POLISH_BRIEF.md
    - obra/intent/models.py
"""

import json
import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import yaml

from obra.intent.models import InputType

logger = logging.getLogger(__name__)


class ProjectState(str, Enum):
    """Project state classification for context-aware intent generation.

    Determines whether intent should include technology assumptions (EMPTY)
    or questions for derivation to investigate existing codebase (EXISTING).
    """
    EMPTY = "EMPTY"  # New/minimal project - provide foundation proposals
    EXISTING = "EXISTING"  # Established codebase - ask questions for derivation


@dataclass
class ProjectStateResult:
    """Result of project state detection.

    Attributes:
        state: Detected project state (EMPTY or EXISTING)
        method: Detection method used (deterministic_fast_path or llm_classification)
        rationale: Explanation of why this state was chosen
        file_count: Number of meaningful files found in project
    """
    state: ProjectState
    method: str  # "deterministic_fast_path" or "llm_classification"
    rationale: str
    file_count: int


# Infrastructure directories to exclude from project state detection
EXCLUDED_DIRS = {
    ".git",
    ".obra",
    "node_modules",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    ".env",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "target",  # Rust
    "bin",
    "obj",  # C#
}

# File patterns to exclude
EXCLUDED_PATTERNS = {
    ".pyc",
    ".pyo",
    ".so",
    ".dll",
    ".dylib",
    ".log",
    ".lock",
    "package-lock.json",
    "yarn.lock",
    "Cargo.lock",
}


def list_meaningful_files(project_dir: Path) -> list[Path]:
    """List meaningful files in project directory.

    Excludes infrastructure directories and build artifacts.
    Returns relative paths from project root.

    Args:
        project_dir: Root directory of project

    Returns:
        List of Path objects (relative to project_dir)

    Examples:
        >>> files = list_meaningful_files(Path("/path/to/project"))
        >>> len(files)
        23
        >>> Path("src/main.py") in files
        True
        >>> Path(".git/HEAD") in files
        False
    """
    meaningful_files: list[Path] = []

    if not project_dir.exists():
        return meaningful_files

    for item in project_dir.rglob("*"):
        # Skip if not a file
        if not item.is_file():
            continue

        # Get relative path
        try:
            rel_path = item.relative_to(project_dir)
        except ValueError:
            continue

        # Check if any parent directory is excluded
        if any(part in EXCLUDED_DIRS for part in rel_path.parts):
            continue

        # Check if filename matches excluded pattern
        if any(pattern in item.name for pattern in EXCLUDED_PATTERNS):
            continue

        meaningful_files.append(rel_path)

    return meaningful_files


def detect_project_state(
    project_dir: Path,
    empty_threshold: int = 5,
    existing_threshold: int = 50,
    llm_config: dict | None = None,
    force_state: ProjectState | None = None,
) -> ProjectStateResult:
    """Detect project state using hybrid detection (deterministic + LLM).

    Uses file count thresholds with LLM classification for gray areas:
    - < empty_threshold files → EMPTY (deterministic)
    - > existing_threshold files → EXISTING (deterministic)
    - Between thresholds → LLM classification (with fallback to EXISTING on error)

    Args:
        project_dir: Root directory of project
        empty_threshold: Max files for EMPTY classification (default: 5)
        existing_threshold: Min files for EXISTING classification (default: 50)
        llm_config: Optional LLM configuration dict
        force_state: Optional forced state (bypasses all detection)

    Returns:
        ProjectStateResult with classification

    Examples:
        >>> result = detect_project_state(Path("/new/project"))
        >>> result.state
        ProjectState.EMPTY
        >>> result.method
        'deterministic_fast_path'

        >>> result = detect_project_state(Path("/large/project"))
        >>> result.state
        ProjectState.EXISTING
        >>> result.file_count
        127
    """
    # User-facing message
    logger.info("Analyzing project structure...")

    # Count meaningful files
    files = list_meaningful_files(project_dir)
    file_count = len(files)

    logger.debug(
        "Project state detection triggered: dir=%s, files=%d, thresholds=(%d, %d)",
        project_dir,
        file_count,
        empty_threshold,
        existing_threshold,
    )

    # Force state if requested (for --force-empty, --force-existing flags)
    if force_state is not None:
        logger.info("Using forced project state: %s", force_state.value)
        result = ProjectStateResult(
            state=force_state,
            method="forced_override",
            rationale=f"Manually forced to {force_state.value}",
            file_count=file_count,
        )
        _log_classification_result(result)
        return result

    # Deterministic fast path: very few files → EMPTY
    if file_count < empty_threshold:
        result = ProjectStateResult(
            state=ProjectState.EMPTY,
            method="deterministic_fast_path",
            rationale=f"Project has {file_count} files (< {empty_threshold} threshold)",
            file_count=file_count,
        )
        _log_classification_result(result)
        return result

    # Deterministic fast path: many files → EXISTING
    if file_count > existing_threshold:
        result = ProjectStateResult(
            state=ProjectState.EXISTING,
            method="deterministic_fast_path",
            rationale=f"Project has {file_count} files (> {existing_threshold} threshold)",
            file_count=file_count,
        )
        _log_classification_result(result)
        return result

    # Gray area: requires LLM classification
    logger.debug(
        "Project has %d files (between %d and %d) - attempting LLM classification",
        file_count,
        empty_threshold,
        existing_threshold,
    )

    try:
        result = classify_project_state_with_llm(project_dir, files, llm_config)
        _log_classification_result(result)
        return result
    except Exception as e:
        # Fallback to EXISTING (conservative choice) on any error
        logger.warning(
            "LLM classification failed (%s), falling back to EXISTING (conservative)",
            str(e),
        )
        result = ProjectStateResult(
            state=ProjectState.EXISTING,
            method="error_fallback",
            rationale=f"LLM classification failed ({str(e)[:100]}), defaulting to EXISTING (conservative)",
            file_count=file_count,
        )
        _log_classification_result(result)
        return result


def _log_classification_result(result: ProjectStateResult) -> None:
    """Log structured classification result with all metadata.

    Args:
        result: ProjectStateResult to log
    """
    logger.info(
        "Project state classified: state=%s, method=%s, files=%d, rationale='%s'",
        result.state.value,
        result.method,
        result.file_count,
        result.rationale,
    )


def build_project_classification_prompt(files: list[Path]) -> str:
    """Build prompt for LLM-based project state classification.

    Generates a prompt with file listing that asks the LLM to classify
    the project as EMPTY or EXISTING based on the presence of substantial
    implementation code.

    Args:
        files: List of meaningful files in project (relative paths)

    Returns:
        Formatted prompt string requesting JSON response

    Example:
        >>> files = [Path("README.md"), Path("src/main.py")]
        >>> prompt = build_project_classification_prompt(files)
        >>> "EMPTY" in prompt
        True
        >>> "JSON" in prompt
        True
    """
    file_listing = "\n".join(f"  - {f}" for f in sorted(files))

    return f"""Analyze this project's file structure to determine if it's a new/minimal project (EMPTY) or an established codebase (EXISTING).

Project has {len(files)} files:
{file_listing}

Classification Definitions:

EMPTY: New or minimal project with:
- Only documentation/config files (README, .gitignore, package.json, etc.)
- Minimal starter code or scaffolding
- No substantial implementation yet
- Examples: Fresh repo, starter template, initial setup

EXISTING: Established project with:
- Substantial implementation code
- Multiple modules/components
- Clear project structure with implementation
- Examples: Working application, library with features, active codebase

Respond with JSON only:
{{
  "state": "EMPTY" or "EXISTING",
  "rationale": "Brief explanation of why this classification was chosen"
}}"""


def classify_project_state_with_llm(
    project_dir: Path,
    files: list[Path],
    llm_config: dict | None = None,
) -> ProjectStateResult:
    """Classify project state using LLM for gray-area cases.

    Invokes LLM with file listing to determine if project is EMPTY or EXISTING.
    Uses llm.fast from config, falling back to llm.orchestrator if unavailable.

    Args:
        project_dir: Root directory of project
        files: List of meaningful files (from list_meaningful_files)
        llm_config: Optional LLM configuration dict with provider/model/thinking_level

    Returns:
        ProjectStateResult with LLM classification

    Raises:
        Exception: If LLM invocation fails (caller should handle with fallback)

    Example:
        >>> files = [Path("README.md"), Path("src/main.py"), Path("src/utils.py")]
        >>> result = classify_project_state_with_llm(Path.cwd(), files)
        >>> result.state in [ProjectState.EMPTY, ProjectState.EXISTING]
        True
        >>> result.method
        'llm_classification'
    """
    from obra.llm.cli_runner import invoke_llm_via_cli  # noqa: PLC0415

    # Build classification prompt
    prompt = build_project_classification_prompt(files)

    # Resolve LLM config (use fast model for quick classification)
    # TODO: In S1, load from config with intent.project_detection.llm_model
    config = llm_config or {}
    provider = config.get("provider", "claude")
    model = config.get("model", "default")
    thinking_level = config.get("thinking_level", "low")
    auth_method = config.get("auth_method", "oauth")

    logger.info("Analyzing project structure with LLM...")

    # Invoke LLM
    raw_response = invoke_llm_via_cli(
        prompt=prompt,
        cwd=project_dir,
        provider=provider,
        model=model,
        thinking_level=thinking_level,
        auth_method=auth_method,
        call_site="project_state_classification",
        skip_git_check=config.get("git", {}).get("skip_check", False),  # GIT-HARD-001
    )

    # Parse JSON response
    try:
        response = raw_response.strip()

        # Handle markdown code blocks
        if response.startswith("```"):
            lines = response.split("\n")
            start = 1 if lines[0].startswith("```") else 0
            end = len(lines) - 1 if lines[-1] == "```" else len(lines)
            response = "\n".join(lines[start:end])

        data = json.loads(response)
        state_str = data.get("state", "").upper()
        rationale = data.get("rationale", "LLM classification")

        # Validate state
        if state_str not in {"EMPTY", "EXISTING"}:
            logger.warning(
                "Invalid state from LLM: %s, defaulting to EXISTING",
                state_str,
            )
            state = ProjectState.EXISTING
            rationale = f"Invalid LLM response ({state_str}), defaulting to EXISTING"
        else:
            state = ProjectState(state_str)

        return ProjectStateResult(
            state=state,
            method="llm_classification",
            rationale=rationale,
            file_count=len(files),
        )

    except (json.JSONDecodeError, KeyError, ValueError) as e:
        logger.warning("Failed to parse LLM response: %s", e)
        logger.debug("Raw response: %s", raw_response[:500])
        # Re-raise to trigger fallback in caller
        raise


# Thresholds for classification
VAGUE_MAX_WORDS = 10
VAGUE_MAX_CHARS = 100
RICH_MIN_WORDS = 50
MIN_KEYWORD_MATCHES = 2
MIN_DETAIL_MARKERS = 2
PRD_KEYWORDS = {
    "product requirements",
    "user stories",
    "use cases",
    "stakeholders",
    "scope",
    "deliverables",
    "acceptance criteria",
    "functional requirements",
    "non-functional requirements",
}
PLAN_KEYWORDS = {
    "implementation plan",
    "technical design",
    "architecture",
    "milestones",
    "phases",
    "timeline",
    "tasks",
    "stories",
}


def detect_input_type(
    text: str,
    file_path: Path | None = None,
) -> InputType:
    """Detect the input type for intent generation.

    Classifies input into one of:
    - vague_nl: Short/underspecified natural language
    - rich_nl: Detailed natural language description
    - prd: Product requirements document
    - prose_plan: Unstructured plan document
    - structured_plan: MACHINE_PLAN JSON/YAML format

    Args:
        text: Input text content
        file_path: Optional file path for context

    Returns:
        InputType classification

    Examples:
        >>> detect_input_type("add auth")
        InputType.VAGUE_NL

        >>> detect_input_type("Add user authentication with JWT...")
        InputType.RICH_NL
    """
    # Check for structured plan first (file or JSON content)
    if file_path and is_structured_plan_file(file_path):
        return InputType.STRUCTURED_PLAN

    # Try to detect structured plan from content
    if is_structured_plan_content(text):
        return InputType.STRUCTURED_PLAN

    # Check for PRD keywords
    if is_prd_content(text):
        return InputType.PRD

    # Check for prose plan keywords
    if is_prose_plan_content(text):
        return InputType.PROSE_PLAN

    # Classify natural language by length/detail
    return classify_natural_language(text)


def is_vague(text: str) -> bool:
    """Check if input is vague/underspecified.

    Args:
        text: Input text

    Returns:
        True if vague (short, lacks detail)

    Examples:
        >>> is_vague("add auth")
        True

        >>> is_vague("Add user authentication with JWT tokens...")
        False
    """
    return classify_natural_language(text) == InputType.VAGUE_NL


def classify_natural_language(text: str) -> InputType:
    """Classify natural language input as vague or rich.

    Args:
        text: Input text

    Returns:
        InputType.VAGUE_NL or InputType.RICH_NL
    """
    text = text.strip()
    words = text.split()
    word_count = len(words)
    char_count = len(text)

    # Short inputs are vague
    if word_count <= VAGUE_MAX_WORDS or char_count <= VAGUE_MAX_CHARS:
        return InputType.VAGUE_NL

    # Rich inputs have substantial detail
    if word_count >= RICH_MIN_WORDS:
        return InputType.RICH_NL

    # Medium length - check for detail markers
    detail_markers = [
        "should",
        "must",
        "will",
        "requires",
        "including",
        "such as",
        "for example",
        "specifically",
    ]

    marker_count = sum(1 for m in detail_markers if m in text.lower())
    if marker_count >= MIN_DETAIL_MARKERS:
        return InputType.RICH_NL

    # Default medium-length to vague (safer to expand)
    return InputType.VAGUE_NL


def is_structured_plan_file(file_path: Path) -> bool:
    """Check if file is a structured MACHINE_PLAN format.

    Args:
        file_path: Path to file

    Returns:
        True if file appears to be a MACHINE_PLAN
    """
    if not file_path.exists():
        return False

    # Check file extension
    suffix = file_path.suffix.lower()
    if suffix not in {".json", ".yaml", ".yml"}:
        return False

    # Check filename patterns
    name = file_path.name.lower()
    if "machine_plan" in name or "_machine_plan" in name:
        return True

    # Check content structure
    try:
        content = file_path.read_text(encoding="utf-8")
        return is_structured_plan_content(content)
    except Exception as e:
        logger.debug("Failed to read file for plan detection: %s", e)
        return False


def is_structured_plan_content(text: str) -> bool:
    """Check if content is structured MACHINE_PLAN format.

    Validates for:
    - JSON with work_id and stories keys
    - YAML with work_id and stories keys

    Args:
        text: Content text

    Returns:
        True if structured plan format
    """
    text = text.strip()

    # Try JSON
    if text.startswith("{"):
        try:
            data = json.loads(text)
            return is_valid_machine_plan(data)
        except json.JSONDecodeError:
            pass

    # Try YAML
    try:
        data = yaml.safe_load(text)
        if isinstance(data, dict):
            return is_valid_machine_plan(data)
    except Exception:
        pass

    return False


def is_valid_machine_plan(data: dict) -> bool:
    """Validate if data structure is a valid MACHINE_PLAN.

    Checks for required fields:
    - work_id: Work identifier
    - stories: List of stories with tasks

    Args:
        data: Parsed JSON/YAML data

    Returns:
        True if valid machine plan structure
    """
    if not isinstance(data, dict):
        return False

    # Must have work_id
    if "work_id" not in data:
        return False

    # Must have stories list
    stories = data.get("stories")
    if not isinstance(stories, list) or not stories:
        return False

    # First story must have tasks or be story-shaped
    first_story = stories[0]
    if not isinstance(first_story, dict):
        return False

    # Check for story structure (id, title/desc, tasks)
    has_id = "id" in first_story
    has_title = "title" in first_story or "desc" in first_story
    has_tasks = "tasks" in first_story and isinstance(first_story["tasks"], list)

    return has_id and has_title and has_tasks


def is_prd_content(text: str) -> bool:
    """Check if content appears to be a PRD.

    Args:
        text: Content text

    Returns:
        True if PRD-like content
    """
    text_lower = text.lower()
    keyword_count = sum(1 for k in PRD_KEYWORDS if k in text_lower)
    return keyword_count >= MIN_KEYWORD_MATCHES


def is_prose_plan_content(text: str) -> bool:
    """Check if content appears to be a prose plan.

    Args:
        text: Content text

    Returns:
        True if prose plan-like content
    """
    text_lower = text.lower()
    keyword_count = sum(1 for k in PLAN_KEYWORDS if k in text_lower)
    return keyword_count >= MIN_KEYWORD_MATCHES


def extract_objective_from_plan(data: dict) -> str:
    """Extract objective text from structured plan data.

    Uses work_id and first story title as basis.

    Args:
        data: Machine plan data

    Returns:
        Objective string
    """
    work_id = data.get("work_id", "")

    # Try to get objective from context
    context = data.get("context", {})
    if isinstance(context, dict) and "objective" in context:
        return str(context["objective"])

    # Fall back to work_id + first story
    stories = data.get("stories", [])
    if stories and isinstance(stories[0], dict):
        first_title = stories[0].get("title", stories[0].get("desc", ""))
        if first_title:
            return f"{work_id}: {first_title}"

    return work_id


# Convenience exports
__all__ = [
    "ProjectState",
    "ProjectStateResult",
    "build_project_classification_prompt",
    "classify_project_state_with_llm",
    "detect_input_type",
    "detect_project_state",
    "extract_objective_from_plan",
    "is_prd_content",
    "is_prose_plan_content",
    "is_structured_plan_content",
    "is_structured_plan_file",
    "is_vague",
    "is_valid_machine_plan",
    "list_meaningful_files",
]
