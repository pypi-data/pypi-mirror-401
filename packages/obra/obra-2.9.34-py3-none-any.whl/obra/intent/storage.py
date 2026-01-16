"""Intent storage layer for persistence to ~/.obra/intents/.

This module provides the IntentStorage class for saving and loading
intents to the global ~/.obra/intents/{project}/ directory structure.

Storage Layout:
    ~/.obra/intents/
        index.yaml              # Global index with active_intent per project
        {project}/
            {timestamp}-{slug}.md   # Intent files (markdown with YAML frontmatter)

Related:
    - docs/design/briefs/AUTO_INTENT_GENERATION_BRIEF.md
    - obra/intent/models.py
"""

import hashlib
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from obra.intent.models import IntentModel, IntentStatus

logger = logging.getLogger(__name__)

# Default storage root
DEFAULT_INTENTS_ROOT = Path.home() / ".obra" / "intents"

# YAML frontmatter parsing
FRONTMATTER_PARTS_COUNT = 3  # "---\nfrontmatter\n---\nbody" splits into 3 parts


class IntentStorage:
    """Storage layer for intent persistence.

    Manages saving and loading intents to ~/.obra/intents/{project}/
    with an index.yaml file tracking active intents per project.

    Attributes:
        root: Root directory for intent storage (default: ~/.obra/intents/)

    Example:
        >>> storage = IntentStorage()
        >>> storage.save(intent)
        >>> loaded = storage.load(intent.id, project="my-app")
    """

    def __init__(self, root: Path | None = None) -> None:
        """Initialize IntentStorage.

        Args:
            root: Optional custom root directory (default: ~/.obra/intents/)
        """
        self._root = root or DEFAULT_INTENTS_ROOT

    @property
    def root(self) -> Path:
        """Get the storage root directory."""
        return self._root

    def _ensure_dirs(self, project: str) -> Path:
        """Ensure project directory exists.

        Args:
            project: Project identifier

        Returns:
            Path to project intent directory
        """
        project_dir = self._root / project
        project_dir.mkdir(parents=True, exist_ok=True)
        return project_dir

    def save(self, intent: IntentModel) -> Path:
        """Save an intent to storage.

        Creates a timestamped markdown file with YAML frontmatter.
        Updates the index.yaml to track this as the active intent
        for the project.

        Args:
            intent: IntentModel to save

        Returns:
            Path to the saved intent file

        Example:
            >>> storage = IntentStorage()
            >>> path = storage.save(intent)
            >>> print(path)
            ~/.obra/intents/my-app/20260110T1200-add-auth.md
        """
        project_dir = self._ensure_dirs(intent.project)
        file_path = project_dir / f"{intent.id}.md"

        # Render intent to markdown
        content = self._render_intent_markdown(intent)
        file_path.write_text(content, encoding="utf-8")

        # Update index with active intent
        self._update_index(intent.project, intent.id, intent.status)

        logger.info("Saved intent %s to %s", intent.id, file_path)
        return file_path

    def load(self, intent_id: str, project: str) -> IntentModel | None:
        """Load an intent from storage.

        Args:
            intent_id: Intent ID to load
            project: Project identifier

        Returns:
            IntentModel if found, None otherwise

        Example:
            >>> storage = IntentStorage()
            >>> intent = storage.load("20260110T1200-add-auth", "my-app")
        """
        project_dir = self._root / project
        file_path = project_dir / f"{intent_id}.md"

        if not file_path.exists():
            logger.debug("Intent file not found: %s", file_path)
            return None

        try:
            content = file_path.read_text(encoding="utf-8")
            return self._parse_intent_markdown(content, intent_id, project)
        except Exception:
            logger.exception("Failed to load intent %s", intent_id)
            return None

    def load_active(self, project: str) -> IntentModel | None:
        """Load the active intent for a project.

        Args:
            project: Project identifier

        Returns:
            Active IntentModel if exists, None otherwise
        """
        index = self._load_index()
        project_data = index.get("projects", {}).get(project, {})
        active_id = project_data.get("active_intent")

        if not active_id:
            logger.debug("No active intent for project: %s", project)
            return None

        return self.load(active_id, project)

    def list_intents(self, project: str | None = None) -> list[dict[str, Any]]:
        """List all intents, optionally filtered by project.

        Args:
            project: Optional project filter

        Returns:
            List of intent summaries with id, project, slug, created, status
        """
        intents: list[dict[str, Any]] = []
        index = self._load_index()

        if project:
            projects = {project: index.get("projects", {}).get(project, {})}
        else:
            projects = index.get("projects", {})

        for proj_name, proj_data in projects.items():
            proj_dir = self._root / proj_name
            if not proj_dir.exists():
                continue

            active_id = proj_data.get("active_intent")

            for intent_file in proj_dir.glob("*.md"):
                intent_id = intent_file.stem
                # Parse minimal info from filename
                parts = intent_id.split("-", 1)
                timestamp = parts[0] if parts else ""
                slug = parts[1] if len(parts) > 1 else intent_id

                intents.append(
                    {
                        "id": intent_id,
                        "project": proj_name,
                        "slug": slug,
                        "created": timestamp,
                        "is_active": intent_id == active_id,
                    }
                )

        # Sort by created timestamp descending
        intents.sort(key=lambda x: x.get("created", ""), reverse=True)
        return intents

    def delete(self, intent_id: str, project: str) -> bool:
        """Delete an intent from storage.

        Args:
            intent_id: Intent ID to delete
            project: Project identifier

        Returns:
            True if deleted, False if not found
        """
        project_dir = self._root / project
        file_path = project_dir / f"{intent_id}.md"

        if not file_path.exists():
            logger.debug("Intent file not found for deletion: %s", file_path)
            return False

        file_path.unlink()

        # Update index if this was the active intent
        index = self._load_index()
        proj_data = index.get("projects", {}).get(project, {})
        if proj_data.get("active_intent") == intent_id:
            proj_data["active_intent"] = None
            self._save_index(index)

        logger.info("Deleted intent %s from %s", intent_id, project)
        return True

    def set_active(self, intent_id: str, project: str) -> bool:
        """Set an intent as the active intent for a project.

        Args:
            intent_id: Intent ID to set as active
            project: Project identifier

        Returns:
            True if set, False if intent not found
        """
        project_dir = self._root / project
        file_path = project_dir / f"{intent_id}.md"

        if not file_path.exists():
            logger.debug("Intent file not found: %s", file_path)
            return False

        self._update_index(project, intent_id, IntentStatus.ACTIVE)
        logger.info("Set active intent for %s: %s", project, intent_id)
        return True

    def resolve_id(self, partial_id: str, project: str) -> str | None:
        """Resolve a partial ID to a full intent ID.

        Supports:
        - Full ID: 20260110T1200-add-auth
        - Timestamp only: 20260110T1200
        - Slug only: add-auth

        Args:
            partial_id: Partial or full intent ID
            project: Project identifier

        Returns:
            Full intent ID if unique match found, None otherwise
        """
        project_dir = self._root / project
        if not project_dir.exists():
            return None

        matches: list[str] = []
        for intent_file in project_dir.glob("*.md"):
            intent_id = intent_file.stem

            # Exact match
            if intent_id == partial_id:
                return intent_id

            # Timestamp prefix match
            if intent_id.startswith(partial_id):
                matches.append(intent_id)
                continue

            # Slug suffix match
            if intent_id.endswith(f"-{partial_id}"):
                matches.append(intent_id)
                continue

        if len(matches) == 1:
            return matches[0]

        if len(matches) > 1:
            logger.warning(
                "Ambiguous intent ID '%s' matches multiple: %s",
                partial_id,
                matches,
            )

        return None

    def get_project_id(self, working_dir: Path) -> str:
        """Get project identifier from working directory.

        Uses the directory name for readability, falling back to
        a hash if the name contains problematic characters.

        Args:
            working_dir: Project working directory

        Returns:
            Project identifier string
        """
        name = working_dir.name

        # If name is simple alphanumeric with hyphens/underscores, use it
        if all(c.isalnum() or c in "-_" for c in name):
            return name.lower()

        # Otherwise hash the full path
        return hashlib.sha256(str(working_dir).encode()).hexdigest()[:12]

    def _update_index(
        self,
        project: str,
        intent_id: str,
        status: IntentStatus,
    ) -> None:
        """Update the index.yaml with intent information.

        Args:
            project: Project identifier
            intent_id: Intent ID
            status: Intent status
        """
        index = self._load_index()

        if "projects" not in index:
            index["projects"] = {}

        if project not in index["projects"]:
            index["projects"][project] = {}

        proj_data = index["projects"][project]

        # Set as active if status is ACTIVE
        if status == IntentStatus.ACTIVE:
            proj_data["active_intent"] = intent_id

        proj_data["last_updated"] = datetime.now(UTC).isoformat()

        self._save_index(index)

    def _load_index(self) -> dict[str, Any]:
        """Load the index.yaml file.

        Returns:
            Index data dictionary
        """
        index_path = self._root / "index.yaml"
        if not index_path.exists():
            return {"version": 1, "projects": {}}

        try:
            content = index_path.read_text(encoding="utf-8")
            return yaml.safe_load(content) or {"version": 1, "projects": {}}
        except Exception:
            logger.exception("Failed to load index.yaml")
            return {"version": 1, "projects": {}}

    def _save_index(self, index: dict[str, Any]) -> None:
        """Save the index.yaml file.

        Args:
            index: Index data dictionary
        """
        self._root.mkdir(parents=True, exist_ok=True)
        index_path = self._root / "index.yaml"

        index["version"] = 1
        index["updated"] = datetime.now(UTC).isoformat()

        content = yaml.safe_dump(index, default_flow_style=False, sort_keys=False)
        index_path.write_text(content, encoding="utf-8")

    def _render_intent_markdown(self, intent: IntentModel) -> str:
        """Render an intent to markdown with YAML frontmatter.

        Args:
            intent: IntentModel to render

        Returns:
            Markdown content string
        """
        # Import here to avoid circular import
        from obra.intent.templates import render_intent_template  # noqa: PLC0415

        return render_intent_template(intent)

    def _parse_intent_markdown(
        self,
        content: str,
        intent_id: str,
        project: str,
    ) -> IntentModel | None:
        """Parse markdown with YAML frontmatter into IntentModel.

        Args:
            content: Markdown content
            intent_id: Intent ID for the file
            project: Project identifier

        Returns:
            IntentModel if parsing succeeds, None otherwise
        """
        try:
            # Split frontmatter from body
            if not content.startswith("---"):
                logger.error("Intent file missing YAML frontmatter")
                return None

            parts = content.split("---", 2)
            if len(parts) < FRONTMATTER_PARTS_COUNT:
                logger.error("Invalid YAML frontmatter format")
                return None

            frontmatter = yaml.safe_load(parts[1])
            body = parts[2].strip()

            # Extract sections from body
            sections = self._parse_body_sections(body)

            return IntentModel(
                id=intent_id,
                project=project,
                slug=frontmatter.get("slug", intent_id.split("-", 1)[-1]),
                created=frontmatter.get("created", ""),
                status=IntentStatus(frontmatter.get("status", "active")),
                input_type=frontmatter.get("input_type", "vague_nl"),
                problem_statement=sections.get("problem_statement", ""),
                assumptions=sections.get("assumptions", []),
                requirements=sections.get("requirements", []),
                constraints=sections.get("constraints", []),
                acceptance_criteria=sections.get("acceptance_criteria", []),
                non_goals=sections.get("non_goals", []),
                risks=sections.get("risks", []),
                context_amendments=sections.get("context_amendments", []),
                raw_objective=frontmatter.get("raw_objective", ""),
                metadata=frontmatter.get("metadata", {}),
            )
        except Exception:
            logger.exception("Failed to parse intent markdown")
            return None

    def _parse_body_sections(self, body: str) -> dict[str, Any]:
        """Parse markdown body into sections.

        Args:
            body: Markdown body content

        Returns:
            Dictionary with section name -> content mappings
        """
        sections: dict[str, Any] = {}
        current_section: str | None = None
        current_content: list[str] = []

        for line in body.split("\n"):
            # Check for section header
            if line.startswith("## "):
                # Save previous section
                if current_section:
                    sections[current_section] = self._parse_section_content(
                        current_section, current_content
                    )
                # Start new section
                header = line[3:].strip().lower().replace(" ", "_")
                current_section = header
                current_content = []
            elif current_section:
                current_content.append(line)

        # Save last section
        if current_section:
            sections[current_section] = self._parse_section_content(
                current_section, current_content
            )

        return sections

    def _parse_section_content(
        self,
        section: str,
        lines: list[str],
    ) -> str | list[str]:
        """Parse section content based on section type.

        Args:
            section: Section name
            lines: Content lines

        Returns:
            String for prose sections, list for bullet sections
        """
        list_sections = {
            "assumptions",
            "requirements",
            "constraints",
            "acceptance_criteria",
            "non_goals",
            "risks",
            "context_amendments",
        }

        content = "\n".join(lines).strip()

        if section in list_sections:
            # Parse bullet points
            items: list[str] = []
            for raw_line in lines:
                stripped_line = raw_line.strip()
                if stripped_line.startswith(("- ", "* ")):
                    items.append(stripped_line[2:].strip())
            return items

        return content


    def write_project_pointer(
        self,
        working_dir: Path,
        intent: IntentModel,
    ) -> Path:
        """Write a project-local pointer file for LLM discoverability.

        Creates .obra/active_intent.yaml in the project directory,
        enabling LLM agents to discover the active intent without
        knowing the global storage location.

        Args:
            working_dir: Project working directory
            intent: Active IntentModel to reference

        Returns:
            Path to the created pointer file
        """
        obra_dir = working_dir / ".obra"
        obra_dir.mkdir(parents=True, exist_ok=True)
        pointer_path = obra_dir / "active_intent.yaml"

        # Get the full path to the intent file
        project_dir = self._root / intent.project
        intent_file_path = project_dir / f"{intent.id}.md"

        # Build pointer content
        pointer_content = {
            "_meta": {
                "purpose": "LLM discoverability pointer for Obra intent system",
                "generated": datetime.now(UTC).isoformat(),
                "view_command": "obra intent show",
            },
            "intent": {
                "id": intent.id,
                "project": intent.project,
                "status": intent.status.value,
                "summary": intent.problem_statement[:200] if intent.problem_statement else "",
                "full_path": str(intent_file_path),
            },
        }

        content = yaml.safe_dump(
            pointer_content,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )
        pointer_path.write_text(content, encoding="utf-8")

        logger.info("Wrote project pointer to %s", pointer_path)
        return pointer_path

    def remove_project_pointer(self, working_dir: Path) -> bool:
        """Remove the project-local pointer file.

        Called when an intent is deactivated or deleted.

        Args:
            working_dir: Project working directory

        Returns:
            True if removed, False if not found
        """
        pointer_path = working_dir / ".obra" / "active_intent.yaml"
        if pointer_path.exists():
            pointer_path.unlink()
            logger.info("Removed project pointer: %s", pointer_path)
            return True
        return False


# Convenience exports
__all__ = ["IntentStorage"]
