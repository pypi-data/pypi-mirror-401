"""Derivation engine for breaking down objectives into implementation plans.

This module provides the DerivationEngine class that uses LLM invocation
to transform high-level objectives into structured implementation plans.

The engine:
    1. Gathers project context (files, structure, README)
    2. Builds a derivation prompt with context and constraints
    3. Invokes LLM with optional extended thinking
    4. Parses structured output into plan items

Related:
    - docs/design/prds/UNIFIED_HYBRID_ARCHITECTURE_PRD.md Section 1
    - obra/hybrid/handlers/derive.py (handler layer)
    - obra/llm/invoker.py (LLM invocation)
    - src/derivation/engine.py (CLI implementation reference)
"""

import json
import logging
import time
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from obra.llm.invoker import LLMInvoker

logger = logging.getLogger(__name__)


# Work type detection patterns (aligned with CLI src/derivation/engine.py)
WORK_TYPE_KEYWORDS: dict[str, list[str]] = {
    "feature_implementation": ["implement", "create", "build", "add feature", "new feature"],
    "bug_fix": ["fix", "bug", "issue", "error", "broken", "failing"],
    "refactoring": ["refactor", "restructure", "reorganize", "clean up", "simplify"],
    "documentation": ["docs", "doc", "documentation", "readme", "guide"],
    "integration": ["integrate", "connect", "api", "external", "third-party"],
    "database": ["database", "schema", "migration", "table", "column", "index"],
}

ITEM_COUNT_WARNING_THRESHOLDS = (25, 50, 100, 200, 500, 1000)
README_PREVIEW_LIMIT = 2000
RAW_RESPONSE_PREVIEW_LIMIT = 200
RAW_RESPONSE_WARN_LIMIT = 10000
EXPLORATION_LOOKBACK_MINUTES = 180

SIZING_GUIDANCE = """
## Plan Quality Criteria

### What Makes a Good Plan

**Good items:**
- ✅ ONE primary action per item (create, modify, test, document)
- ✅ Achievable in a single focused LLM session
- ✅ Self-contained description (executor sees ONLY this item)
- ✅ Concrete, verifiable acceptance criteria
- ✅ Explicit dependencies between items
- ✅ Target: 1-3 files modified, ~50-300 lines changed

**Avoid:**
- ❌ Compound titles with "and", "then", "after" (split these)
- ❌ Items touching >5 files (add explore item first)
- ❌ Vague criteria ("works correctly", "code is clean")
- ❌ Hidden dependencies between items
- ❌ Descriptions over ~150 words (too big)

### Acceptance Criteria Quality

Each criterion must be objectively verifiable:
- GOOD: "pytest tests/auth/ passes with 0 failures"
- GOOD: "Returns 401 JSON error on invalid credentials"
- GOOD: "ruff check exits 0 with no lint errors"
- BAD: "Code is clean and readable"
- BAD: "Tests look good"

Cover both success and failure paths. State where artifacts live.

### Context-Aware Descriptions

The executing LLM sees ONLY this item's description—not the original objective or other items.
- Include specific file paths, function names, API contracts
- Don't assume knowledge of previous decisions—repeat key context
- Call out inputs/outputs, feature flags, config values explicitly

### Phase-Specific Guidance

For each phase, consider what's appropriate:
- **EXPLORE**: What context do you need? What patterns exist? (Read-only)
- **PLAN**: What's the approach? What are the interfaces? (Design-focused)
- **IMPLEMENT**: What's the smallest shippable unit? (1-3 files, single feature)
- **COMMIT**: What verification ensures quality? (Tests, lint, docs)

### Complexity Signals (Split If Present)

If any of these apply, the item is likely too big:
- Description exceeds ~150 words
- Item touches >5 files
- Item lists >5 acceptance criteria
- Title contains "and", "then", or "after"
- Work spans multiple phases
- Requires understanding multiple subsystems
"""

# Work phases (4-phase workflow)
VALID_PHASES = ["explore", "plan", "implement", "commit"]

# Work types that benefit from exploration phase
WORK_TYPES_NEEDING_EXPLORATION = ["feature_implementation", "refactoring", "integration"]


def detect_recent_exploration(
    working_dir: Path,
    *,
    lookback_minutes: int = EXPLORATION_LOOKBACK_MINUTES,
    log_paths: Sequence[Path] | None = None,
) -> dict[str, Any]:
    """Detect whether exploration or plan mode activity occurred recently.

    Checks a set of JSON/JSONL log files for entries indicating either an
    explore agent run or Plan Mode activity inside a configurable lookback
    window. Returns a small report that can be used for nudging the user.
    """
    cutoff = datetime.now(UTC) - timedelta(minutes=lookback_minutes)
    candidates = (
        list(log_paths)
        if log_paths is not None
        else [
            working_dir / ".obra" / "activity.log",
            working_dir / ".obra" / "session_history.jsonl",
            Path.home() / ".obra" / "memory" / "activity.log",
            Path.home() / ".obra" / "last-session.json",
        ]
    )

    signals: list[dict[str, str]] = []
    for path in candidates:
        signals.extend(_collect_exploration_signals(path, cutoff))

    signals.sort(key=lambda signal: signal["timestamp"], reverse=True)
    return {
        "recent_exploration": bool(signals),
        "signals": signals,
    }


def _collect_exploration_signals(path: Path, cutoff: datetime) -> list[dict[str, str]]:
    """Parse a log file and collect exploration signals within cutoff."""
    if not path.exists() or not path.is_file():
        return []

    try:
        content = path.read_text(encoding="utf-8")
    except OSError:
        return []

    entries: list[Any] = []
    try:
        loaded = json.loads(content)
        if isinstance(loaded, list):
            entries = loaded
        elif isinstance(loaded, dict):
            entries = [loaded]
    except json.JSONDecodeError:
        for line in content.splitlines():
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                continue
            entries.append(entry)

    signals: list[dict[str, str]] = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        if not _is_exploration_entry(entry):
            continue

        ts = _extract_timestamp(entry) or datetime.fromtimestamp(path.stat().st_mtime, tz=UTC)
        if ts < cutoff:
            continue

        signals.append(
            {
                "source": str(path),
                "timestamp": ts.isoformat(),
                "reason": _extract_reason(entry),
            }
        )
    return signals


def _is_exploration_entry(entry: dict[str, Any]) -> bool:
    """Determine if an entry represents exploration or plan mode activity."""
    action = str(entry.get("action", "")).lower()
    mode = str(entry.get("mode", "")).lower()
    agent = str(entry.get("agent", "")).lower()
    tags = entry.get("tags", [])
    tag_values = tags if isinstance(tags, list) else ([tags] if tags else [])

    tagged_exploration = any(
        str(tag).lower() in {"explore", "exploration", "plan_mode"} for tag in tag_values
    )

    return bool(
        tagged_exploration
        or action in {"explore", "exploration", "plan_mode"}
        or agent == "explore"
        or entry.get("plan_mode") is True
        or "plan_mode" in mode
    )


def _extract_timestamp(entry: dict[str, Any]) -> datetime | None:
    """Extract a timestamp from common log fields."""
    candidates = [
        entry.get("timestamp"),
        entry.get("created_at"),
        entry.get("ts"),
        entry.get("time"),
    ]
    for value in candidates:
        if value is None:
            continue
        if isinstance(value, (int, float)):
            try:
                return datetime.fromtimestamp(float(value), tz=UTC)
            except (OSError, ValueError):
                continue
        if isinstance(value, str):
            parsed = _parse_iso_timestamp(value)
            if parsed:
                return parsed
    return None


def _parse_iso_timestamp(value: str) -> datetime | None:
    """Parse ISO timestamp strings, including those ending with Z."""
    try:
        normalized = value.replace("Z", "+00:00") if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)
    except ValueError:
        return None


def _extract_reason(entry: dict[str, Any]) -> str:
    """Extract a human-friendly reason for the detected signal."""
    for key in ["action", "mode", "agent"]:
        value = entry.get(key)
        if value:
            return str(value)
    return "exploration"


@dataclass
class DerivationResult:
    """Result from plan derivation.

    Attributes:
        plan_items: List of derived plan items
        raw_response: Raw LLM response for debugging
        work_type: Detected work type
        duration_seconds: Time taken for derivation
        tokens_used: Estimated tokens used
        success: Whether derivation succeeded
        error_message: Error message if failed
    """

    plan_items: list[dict[str, Any]] = field(default_factory=list)
    raw_response: str = ""
    work_type: str = "general"
    duration_seconds: float = 0.0
    tokens_used: int = 0
    success: bool = True
    error_message: str = ""

    @property
    def item_count(self) -> int:
        """Number of derived plan items."""
        return len(self.plan_items)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "plan_items": self.plan_items,
            "raw_response": self.raw_response,
            "work_type": self.work_type,
            "duration_seconds": self.duration_seconds,
            "tokens_used": self.tokens_used,
            "success": self.success,
            "error_message": self.error_message,
            "item_count": self.item_count,
        }


class DerivationEngine:
    """Engine for deriving implementation plans from objectives.

    Uses LLM invocation to break down high-level objectives into
    structured plan items (tasks/stories) with proper sequencing
    and dependencies.

    Example:
        >>> from obra.llm.invoker import LLMInvoker
        >>> invoker = LLMInvoker()
        >>> engine = DerivationEngine(
        ...     working_dir=Path("/path/to/project"),
        ...     llm_invoker=invoker,
        ... )
        >>> result = engine.derive("Add user authentication")
        >>> for item in result.plan_items:
        ...     print(f"{item['id']}: {item['title']}")

    Thread-safety:
        Thread-safe through LLMInvoker's thread safety guarantees.

    Related:
        - obra/hybrid/handlers/derive.py (handler layer)
        - obra/llm/invoker.py (LLM invocation)
    """

    def __init__(
        self,
        working_dir: Path,
        llm_invoker: Optional["LLMInvoker"] = None,
        thinking_enabled: bool = True,
        thinking_level: str = "high",
        max_items: int = 20,
    ) -> None:
        """Initialize DerivationEngine.

        Args:
            working_dir: Working directory for file access
            llm_invoker: LLMInvoker instance for LLM calls
            thinking_enabled: Whether to use extended thinking
            thinking_level: Thinking level (off, minimal, standard, high, maximum)
            max_items: Advisory target for plan item count (prompt guidance only; no truncation)
        """
        self._working_dir = working_dir
        self._llm_invoker = llm_invoker
        self._thinking_enabled = thinking_enabled
        self._thinking_level = thinking_level
        self._max_items = max_items

        logger.debug(
            f"DerivationEngine initialized: working_dir={working_dir}, "
            f"thinking_enabled={thinking_enabled}, thinking_level={thinking_level}"
        )

    def derive(
        self,
        objective: str,
        project_context: dict[str, Any] | None = None,
        constraints: dict[str, Any] | None = None,
        provider: str = "anthropic",
    ) -> DerivationResult:
        """Derive implementation plan from objective.

        Args:
            objective: Task objective to plan for
            project_context: Optional project context (languages, frameworks)
            constraints: Optional derivation constraints
            provider: LLM provider to use

        Returns:
            DerivationResult with plan items and metadata

        Example:
            >>> result = engine.derive(
            ...     "Add user authentication",
            ...     project_context={"languages": ["python"]},
            ...     constraints={"max_items": 10},
            ... )
        """
        start_time = time.time()

        try:
            # Detect work type
            work_type = self._detect_work_type(objective)

            # Gather local context
            context = self._gather_context(project_context or {})

            # Build prompt
            prompt = self._build_prompt(
                objective=objective,
                context=context,
                constraints=constraints or {},
                work_type=work_type,
            )

            # Invoke LLM
            raw_response, tokens_used = self._invoke_llm(
                prompt=prompt,
                provider=provider,
                _work_type=work_type,
            )

            # Parse response
            plan_items = self._parse_response(raw_response)

            duration = time.time() - start_time
            logger.info(
                f"Derivation completed: {len(plan_items)} items, "
                f"{duration:.2f}s, work_type={work_type}"
            )

            return DerivationResult(
                plan_items=plan_items,
                raw_response=raw_response,
                work_type=work_type,
                duration_seconds=duration,
                tokens_used=tokens_used,
                success=True,
            )

        except Exception as exc:
            duration = time.time() - start_time
            logger.exception("Derivation failed")
            return DerivationResult(
                success=False,
                error_message=str(exc),
                duration_seconds=duration,
            )

    def _detect_work_type(self, objective: str) -> str:
        """Detect work type from objective text.

        Args:
            objective: Task objective

        Returns:
            Work type string
        """
        text = objective.lower()

        for work_type, keywords in WORK_TYPE_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                logger.debug(f"Detected work type: {work_type}")
                return work_type

        return "general"

    def _gather_context(self, project_context: dict[str, Any]) -> dict[str, Any]:
        """Gather local context for derivation.

        Args:
            project_context: Base project context

        Returns:
            Enhanced context dictionary
        """
        context = dict(project_context)

        # Add file structure summary
        try:
            structure = self._summarize_structure()
            context["file_structure"] = structure
        except Exception as e:
            logger.warning(f"Failed to gather file structure: {e}")

        # Add README if exists
        readme_path = self._working_dir / "README.md"
        if readme_path.exists():
            try:
                content = readme_path.read_text(encoding="utf-8")
                # Truncate to first README_PREVIEW_LIMIT chars
                context["readme"] = content[:README_PREVIEW_LIMIT] + (
                    "..." if len(content) > README_PREVIEW_LIMIT else ""
                )
            except Exception:
                pass

        return context

    def _summarize_structure(self) -> list[str]:
        """Summarize project file structure.

        Returns:
            List of important file paths
        """
        important_files: list[str] = []
        important_patterns = [
            "*.py",
            "*.js",
            "*.ts",
            "*.tsx",
            "*.jsx",
            "package.json",
            "pyproject.toml",
            "requirements.txt",
            "Cargo.toml",
            "go.mod",
            "README.md",
            "Makefile",
            "Dockerfile",
        ]

        max_files = 50
        skip_dirs = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}

        for pattern in important_patterns:
            for path in self._working_dir.rglob(pattern):
                if any(skip_dir in path.parts for skip_dir in skip_dirs):
                    continue

                try:
                    rel_path = path.relative_to(self._working_dir)
                    important_files.append(str(rel_path))
                except ValueError:
                    continue

                if len(important_files) >= max_files:
                    break

            if len(important_files) >= max_files:
                break

        return sorted(important_files)[:max_files]

    def _build_prompt(
        self,
        objective: str,
        context: dict[str, Any],
        constraints: dict[str, Any],
        work_type: str,
    ) -> str:
        """Build derivation prompt.

        Args:
            objective: Task objective
            context: Project context
            constraints: Derivation constraints
            work_type: Detected work type

        Returns:
            Prompt string for LLM
        """
        # Build context section
        context_parts = []

        if context.get("languages"):
            context_parts.append(f"Languages: {', '.join(context['languages'])}")

        if context.get("frameworks"):
            context_parts.append(f"Frameworks: {', '.join(context['frameworks'])}")

        if context.get("file_structure"):
            files = context["file_structure"][:20]
            context_parts.append(f"Key files: {', '.join(files)}")

        if context.get("readme"):
            context_parts.append(f"README excerpt:\n{context['readme'][:500]}")

        context_section = (
            "\n".join(context_parts) if context_parts else "No project context available."
        )

        # Build constraints section
        max_items = constraints.get("max_items", self._max_items)
        constraint_lines = []
        if max_items:
            constraint_lines.append(
                f"- Advisory: Aim for ~{max_items} plan items if they stay small and testable; no hard cap—split oversized work instead of dropping items."
            )

        if constraints.get("scope_boundaries"):
            constraint_lines.append(f"- Scope boundaries: {', '.join(constraints['scope_boundaries'])}")

        constraints_section = ("\n".join(constraint_lines) + "\n") if constraint_lines else ""

        # Get pattern guidance
        pattern_guidance = self._get_pattern_guidance(work_type)

        # 4-phase guidance for complex work types
        four_phase_guidance = ""
        if work_type in WORK_TYPES_NEEDING_EXPLORATION:
            four_phase_guidance = """
## Recommended Phase Structure (4-Phase Workflow)

For best results, structure derived items to follow the 4-phase workflow:

1. **Explore** (work_phase: "explore")
   - Research existing code, patterns, dependencies
   - Do NOT write implementation code in this phase

2. **Plan** (work_phase: "plan")
   - Design the approach based on exploration
   - Create implementation plan

3. **Implement** (work_phase: "implement")
   - Execute the plan step by step
   - Reference the plan to stay on track

4. **Commit** (work_phase: "commit")
   - Run tests, verify, commit
   - Update documentation

Not all work requires all phases. Bug fixes may skip exploration.
Simple tasks may skip planning. Use judgment based on complexity.
"""

        return f"""You are an expert software architect. Derive an implementation plan for the following objective.

## Objective
{objective}

## Project Context
{context_section}

## Work Type Detected: {work_type}
{pattern_guidance}

## Constraints
{constraints_section}
{four_phase_guidance}{SIZING_GUIDANCE}
## Instructions
Create a structured implementation plan with the following requirements:
1. Break the objective into logical tasks/stories
2. Each item should be independently testable
3. Order items by dependencies (items that must be done first come first)
4. Be specific about what each item accomplishes
5. Include acceptance criteria for each item
6. Classify each item's work_phase if applicable (explore, plan, implement, commit)

## Output Format
Return a JSON object with a "plan_items" array. Each item should have:
- id: Unique identifier (e.g., "T1", "T2")
- item_type: "task" or "story"
- title: Brief title
- description: Detailed description
- acceptance_criteria: Array of criteria strings
- dependencies: Array of item IDs this depends on
- work_phase: "explore" | "plan" | "implement" | "commit" (optional)

Example:
```json
{{
  "plan_items": [
    {{
      "id": "T1",
      "item_type": "task",
      "title": "Research existing authentication patterns",
      "description": "Explore the codebase to understand existing auth patterns",
      "acceptance_criteria": [
        "Exploration notes saved to docs/auth/README.md with file paths for existing flows",
        "pytest tests/auth/ passes with 0 failures"
      ],
      "dependencies": [],
      "work_phase": "explore"
    }},
    {{
      "id": "T2",
      "item_type": "task",
      "title": "Implement login endpoint",
      "description": "Create POST /login endpoint that validates credentials",
      "acceptance_criteria": ["Endpoint returns JWT on valid credentials", "Returns 401 on invalid"],
      "dependencies": ["T1"],
      "work_phase": "implement"
    }}
  ]
}}
```

Return ONLY the JSON object, no additional text.
"""

    def _get_pattern_guidance(self, work_type: str) -> str:
        """Get decomposition guidance for work type.

        Args:
            work_type: Detected work type

        Returns:
            Pattern guidance string
        """
        patterns = {
            "feature_implementation": """
For new features, consider:
- What data models and interfaces need to exist?
- What's the core functionality that delivers user value?
- How will you verify it works (tests, manual checks)?
- What documentation helps users understand it?""",
            "bug_fix": """
For bug fixes, consider:
- Can you reproduce the bug reliably? (Write a failing test first)
- What's the root cause, not just the symptom?
- What regression test prevents this from recurring?
- How do you verify the fix works in realistic conditions?""",
            "refactoring": """
For refactoring, consider:
- What's wrong with the current structure? (Document before changing)
- What's the target state and migration path?
- How do you maintain test coverage throughout?
- How do you verify behavior is unchanged?""",
            "integration": """
For integrations, consider:
- What's the contract between systems? (Define interfaces first)
- How do you handle errors and edge cases?
- How do you test without depending on external systems?
- What documentation helps others use this integration?""",
            "database": """
For database changes, consider:
- What's the schema change and migration strategy?
- How do you handle rollback if something goes wrong?
- What ORM/query changes follow from the schema change?
- How do you test migrations safely before production?""",
            "general": """
Consider for any work:
- What context do you need before starting? (explore)
- What's the approach and key decisions? (plan)
- What's the smallest shippable implementation? (implement)
- How do you verify quality and completeness? (commit)""",
        }

        return patterns.get(work_type, patterns["general"])

    def _invoke_llm(
        self,
        prompt: str,
        provider: str,
        _work_type: str,
    ) -> tuple[str, int]:
        """Invoke LLM to generate plan.

        Args:
            prompt: Derivation prompt
            provider: LLM provider name
            work_type: Detected work type

        Returns:
            Tuple of (raw_response, tokens_used)
        """
        if self._llm_invoker is None:
            logger.warning("No LLM invoker configured, returning placeholder")
            return self._placeholder_response(), 0

        # Determine thinking level
        thinking_level = None
        if self._thinking_enabled:
            thinking_level = self._thinking_level

        # Invoke LLM
        result = self._llm_invoker.invoke(
            prompt=prompt,
            provider=provider,
            thinking_level=thinking_level,
            response_format="json",
        )

        return result.content, result.tokens_used

    def _placeholder_response(self) -> str:
        """Generate placeholder response when no LLM available.

        Returns:
            Placeholder JSON response
        """
        return json.dumps(
            {
                "plan_items": [
                    {
                        "id": "T1",
                        "item_type": "task",
                        "title": "Placeholder task",
                        "description": "LLM invoker not configured - configure via obra/llm/invoker.py",
                        "acceptance_criteria": ["LLM invocation implemented"],
                        "dependencies": [],
                        "work_phase": "implement",
                    }
                ]
            }
        )

    def _parse_response(self, raw_response: str) -> list[dict[str, Any]]:
        """Parse LLM response into plan items.

        Args:
            raw_response: Raw LLM response

        Returns:
            List of plan item dictionaries
        """
        try:
            response = raw_response.strip()

            # Check for empty response
            if not response:
                logger.error("Received empty response from LLM")
                return self._create_diagnostic_fallback(
                    "Empty response",
                    "LLM returned empty content. Check LLM provider configuration and API key.",
                    raw_response,
                )

            # Handle markdown code blocks
            if response.startswith("```"):
                lines = response.split("\n")
                start = 1 if lines[0].startswith("```") else 0
                end = len(lines) - 1 if lines[-1] == "```" else len(lines)
                response = "\n".join(lines[start:end])

            # Parse JSON
            data = json.loads(response)

            # Extract plan_items
            if isinstance(data, dict) and "plan_items" in data:
                items = data["plan_items"]
            elif isinstance(data, list):
                items = data
            else:
                logger.warning("Unexpected response format")
                items = [data]

            # Validate and normalize items
            normalized = []
            for i, item in enumerate(items):
                # Coerce item_type to supported values
                raw_item_type = item.get("item_type", "task")
                item_type = (
                    raw_item_type
                    if raw_item_type in {"task", "subtask", "milestone"}
                    else "task"
                )

                normalized_item = {
                    "id": item.get("id", f"T{i + 1}"),
                    "item_type": item_type,
                    "title": item.get("title", "Untitled"),
                    "description": item.get("description", "") or item.get("title", "Untitled"),
                    "acceptance_criteria": item.get("acceptance_criteria", []),
                    "dependencies": item.get("dependencies", []),
                }
                normalized.append(normalized_item)

            self._log_item_count_warning(len(normalized))

        except json.JSONDecodeError as e:
            logger.exception(
                "Failed to parse plan JSON. Raw response (first 500 chars): %s",
                raw_response[:500],
            )
            return self._create_diagnostic_fallback(
                f"JSON parse error: {e!s}",
                self._generate_parse_error_diagnostic(e, raw_response),
                raw_response,
            )
        else:
            return normalized

    def _log_item_count_warning(self, item_count: int) -> None:
        """Log tiered warnings for large derived plans."""
        for threshold in sorted(ITEM_COUNT_WARNING_THRESHOLDS, reverse=True):
            if item_count >= threshold:
                logger.warning(
                    "Large derived plan: %s items (>= %s). Ensure items stay small, single-action, and self-contained; no hard cap applied.",
                    item_count,
                    threshold,
                )
                return

    def _create_diagnostic_fallback(
        self, error_type: str, diagnostic: str, raw_response: str
    ) -> list[dict[str, Any]]:
        """Create diagnostic fallback task with detailed information.

        Args:
            error_type: Type of error encountered
            diagnostic: Detailed diagnostic message
            raw_response: Raw LLM response for reference

        Returns:
            List containing single diagnostic task
        """
        # Truncate raw response for description (keep it manageable)
        response_preview = raw_response[:RAW_RESPONSE_PREVIEW_LIMIT] if raw_response else "(empty)"
        if len(raw_response) > RAW_RESPONSE_PREVIEW_LIMIT:
            response_preview += "... (truncated)"

        # Save full response to a debug file for investigation
        try:
            debug_dir = Path.home() / ".obra" / "debug"
            debug_dir.mkdir(parents=True, exist_ok=True)
            debug_file = debug_dir / f"parse_error_{int(time.time())}.txt"
            debug_file.write_text(
                f"Error Type: {error_type}\n\n"
                f"Diagnostic: {diagnostic}\n\n"
                f"Raw Response:\n{raw_response}\n",
                encoding="utf-8",
            )
            logger.info(f"Full parse error details saved to: {debug_file}")
            debug_path_info = f"\n\nFull response saved to: {debug_file}"
        except Exception as e:
            logger.warning(f"Could not save debug file: {e}")
            debug_path_info = ""

        return [
            {
                "id": "T1",
                "item_type": "task",
                "title": "LLM Response Parse Error - Manual Review Required",
                "description": (
                    f"**Error**: {error_type}\n\n"
                    f"**Diagnostic**: {diagnostic}\n\n"
                    f"**Raw Response Preview**:\n```\n{response_preview}\n```"
                    f"{debug_path_info}\n\n"
                    f"**Next Steps**:\n"
                    f"1. Review the raw response in the debug file above\n"
                    f"2. Check LLM provider configuration (API key, model, endpoint)\n"
                    f"3. Verify the prompt format is compatible with the LLM\n"
                    f"4. Check for rate limiting or quota issues\n"
                    f"5. If using extended thinking, try without it\n"
                ),
                "acceptance_criteria": [
                    "Root cause identified",
                    "LLM returns valid JSON response",
                    "Plan items parse successfully",
                ],
                "dependencies": [],
                "work_phase": "explore",
            }
        ]

    def _generate_parse_error_diagnostic(
        self, error: json.JSONDecodeError, raw_response: str
    ) -> str:
        """Generate detailed diagnostic for JSON parse errors.

        Args:
            error: JSONDecodeError exception
            raw_response: Raw LLM response

        Returns:
            Diagnostic message
        """
        diagnostics = []

        # Check for common issues
        if not raw_response:
            diagnostics.append("• Response is completely empty")
        elif raw_response.strip().startswith("<"):
            diagnostics.append("• Response appears to be HTML/XML, not JSON")
        elif "error" in raw_response.lower() and "rate" in raw_response.lower():
            diagnostics.append("• Response may indicate rate limiting")
        elif "error" in raw_response.lower() and "auth" in raw_response.lower():
            diagnostics.append("• Response may indicate authentication failure")
        elif not raw_response.strip().startswith(("{", "[")):
            diagnostics.append(
                f"• Response starts with unexpected character: '{raw_response[0] if raw_response else 'N/A'}'"
            )

        # Add JSON error details
        diagnostics.append(f"• JSON error at line {error.lineno}, column {error.colno}")
        diagnostics.append(f"• Error message: {error.msg}")

        # Check response length
        if len(raw_response) > RAW_RESPONSE_WARN_LIMIT:
            diagnostics.append(
                f"• Response is very large ({len(raw_response)} chars) - may have exceeded output limits"
            )

        return "\n".join(diagnostics) if diagnostics else "No specific diagnostic available"


__all__ = [
    "EXPLORATION_LOOKBACK_MINUTES",
    "VALID_PHASES",
    "WORK_TYPES_NEEDING_EXPLORATION",
    "WORK_TYPE_KEYWORDS",
    "DerivationEngine",
    "DerivationResult",
    "detect_recent_exploration",
]
