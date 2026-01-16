"""Project context manager for notes.yaml storage.

This module provides storage and retrieval for project-specific context notes
that are injected into orchestration prompts for LLM-agnostic operation.

Key Features:
- Load/save notes from .obra/context/notes.yaml
- Add/remove/clear notes with auto-pruning (50-note limit)
- Usage metrics tracking (injections_count, total_notes_added)
- Recency-based prioritization for token budget enforcement

Schema:
    _meta:
      version: 1
      updated: "2026-01-04T12:00:00Z"
      count: 3
      metrics:
        created: "2026-01-04T10:00:00Z"
        total_notes_added: 5
        injections_count: 42
    notes:
      - id: "note-001"
        text: "Use snake_case for API params"
        added: "2026-01-04T10:00:00Z"

Example:
    >>> from obra.project.context import ProjectContextManager
    >>> manager = ProjectContextManager(project_root=".obra")
    >>> manager.add_note("Use pytest fixtures for DB tests")
    >>> notes = manager.load_notes()
    >>> print(f"Loaded {len(notes)} notes")
"""

import logging
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

logger = logging.getLogger(__name__)


@dataclass
class ProjectNote:
    """A single project context note.

    Attributes:
        id: Unique identifier (e.g., "note-001")
        text: Note content
        added: ISO 8601 timestamp when note was created
    """

    id: str
    text: str
    added: str

    def to_dict(self) -> dict[str, str]:
        """Convert to dictionary for YAML serialization."""
        return {"id": self.id, "text": self.text, "added": self.added}

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "ProjectNote":
        """Create from dictionary loaded from YAML."""
        return cls(id=data["id"], text=data["text"], added=data["added"])


@dataclass
class NotesMetadata:
    """Metadata section for notes.yaml.

    Attributes:
        version: Schema version (currently 1)
        updated: Last modification timestamp
        count: Current number of notes
        metrics: Usage tracking metrics
    """

    version: int = 1
    updated: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    count: int = 0
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Convert to dictionary for YAML serialization."""
        return {
            "version": self.version,
            "updated": self.updated,
            "count": self.count,
            "metrics": self.metrics,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NotesMetadata":
        """Create from dictionary loaded from YAML."""
        return cls(
            version=data.get("version", 1),
            updated=data.get("updated", datetime.now(UTC).isoformat()),
            count=data.get("count", 0),
            metrics=data.get("metrics", {}),
        )


class ProjectContextManager:
    """Manager for project context notes storage.

    This class handles all operations on .obra/context/notes.yaml, including
    load, save, add, remove, and clear operations. Enforces 50-note limit
    with automatic pruning of oldest notes.

    Thread-safe: No (file I/O not synchronized)

    Attributes:
        project_root: Path to .obra directory (default: ".obra")
        notes_path: Full path to notes.yaml file
        max_notes: Maximum number of notes (default: 50)

    Example:
        >>> manager = ProjectContextManager()
        >>> manager.add_note("Use composition over inheritance")
        >>> notes = manager.load_notes()
        >>> manager.remove_note("note-001")
        >>> manager.clear_notes()
    """

    DEFAULT_MAX_NOTES = 50

    def __init__(
        self,
        project_root: str = ".obra",
        max_notes: int = DEFAULT_MAX_NOTES,
    ):
        """Initialize ProjectContextManager.

        Args:
            project_root: Path to .obra directory (default: ".obra")
            max_notes: Maximum number of notes to keep (default: 50)
        """
        self.project_root = Path(project_root)
        self.context_dir = self.project_root / "context"
        self.notes_path = self.context_dir / "notes.yaml"
        self.max_notes = max_notes

    def _ensure_context_dir(self) -> None:
        """Create .obra/context/ directory if it doesn't exist."""
        self.context_dir.mkdir(parents=True, exist_ok=True)
        logger.debug("Ensured context directory exists: %s", self.context_dir)

    def _generate_note_id(self, existing_notes: list[ProjectNote]) -> str:
        """Generate next sequential note ID.

        Args:
            existing_notes: List of existing notes to check for ID conflicts

        Returns:
            Next available note ID (e.g., "note-001", "note-002")
        """
        if not existing_notes:
            return "note-001"

        # Extract numeric IDs
        ids = []
        for note in existing_notes:
            if note.id.startswith("note-"):
                try:
                    ids.append(int(note.id.split("-")[1]))
                except (IndexError, ValueError):
                    continue

        next_id = max(ids, default=0) + 1
        return f"note-{next_id:03d}"

    def _load_yaml_data(self) -> dict:
        """Load raw YAML data from notes.yaml.

        Returns:
            Dictionary with _meta and notes keys, or empty structure if file doesn't exist

        Raises:
            yaml.YAMLError: If YAML parsing fails
        """
        if not self.notes_path.exists():
            logger.debug("Notes file does not exist: %s", self.notes_path)
            return {
                "_meta": NotesMetadata().to_dict(),
                "notes": [],
            }

        with open(self.notes_path, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        # Ensure structure
        if "_meta" not in data:
            data["_meta"] = NotesMetadata().to_dict()
        if "notes" not in data:
            data["notes"] = []

        return data

    def _save_yaml_data(self, data: dict) -> None:
        """Save YAML data to notes.yaml.

        Args:
            data: Dictionary with _meta and notes keys

        Raises:
            IOError: If file write fails
        """
        self._ensure_context_dir()

        with open(self.notes_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(
                data,
                f,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            )

        logger.debug("Saved notes to %s", self.notes_path)

    def load_notes(self, increment_injections: bool = False) -> list[ProjectNote]:
        """Load all notes from notes.yaml.

        Args:
            increment_injections: If True, increment metrics.injections_count

        Returns:
            List of ProjectNote objects, sorted by added date (oldest first)
        """
        data = self._load_yaml_data()

        # Increment injection count if requested
        # Only save if there are actual notes - avoid file churn from metrics-only updates
        if increment_injections:
            notes_list = data.get("notes", [])
            if notes_list:
                # Only persist injection count when notes exist (avoids git churn)
                meta = NotesMetadata.from_dict(data["_meta"])
                injections = meta.metrics.get("injections_count", 0)
                meta.metrics["injections_count"] = injections + 1
                meta.updated = datetime.now(UTC).isoformat()
                data["_meta"] = meta.to_dict()
                self._save_yaml_data(data)
                logger.debug("Incremented injections_count to %s", injections + 1)
            else:
                logger.debug("Skipping injection count save - no notes to track")

        notes = [ProjectNote.from_dict(n) for n in data.get("notes", [])]
        logger.debug("Loaded %s notes from %s", len(notes), self.notes_path)
        return notes

    def save_notes(self, notes: list[ProjectNote], metadata: NotesMetadata) -> None:
        """Save notes and metadata to notes.yaml.

        Args:
            notes: List of ProjectNote objects to save
            metadata: Metadata to save
        """
        data = {
            "_meta": metadata.to_dict(),
            "notes": [n.to_dict() for n in notes],
        }
        self._save_yaml_data(data)

    def add_note(self, text: str) -> str:
        """Add a new note to notes.yaml.

        Enforces 50-note limit with auto-pruning (oldest note removed).
        Updates metrics.total_notes_added.

        Args:
            text: Note content

        Returns:
            ID of the newly created note
        """
        data = self._load_yaml_data()
        meta = NotesMetadata.from_dict(data["_meta"])
        notes = [ProjectNote.from_dict(n) for n in data.get("notes", [])]

        # Generate ID and create note
        note_id = self._generate_note_id(notes)
        new_note = ProjectNote(
            id=note_id,
            text=text,
            added=datetime.now(UTC).isoformat(),
        )
        notes.append(new_note)

        # Auto-prune if exceeds limit (remove oldest)
        if len(notes) > self.max_notes:
            # Sort by added date, remove oldest
            notes_sorted = sorted(notes, key=lambda n: n.added)
            removed_note = notes_sorted[0]
            notes = notes_sorted[1:]
            logger.info(
                "Auto-pruned oldest note %s (exceeded %s note limit)",
                removed_note.id,
                self.max_notes,
            )

        # Update metadata
        meta.count = len(notes)
        meta.updated = datetime.now(UTC).isoformat()

        # Initialize metrics if missing
        if "created" not in meta.metrics:
            meta.metrics["created"] = datetime.now(UTC).isoformat()
        if "total_notes_added" not in meta.metrics:
            meta.metrics["total_notes_added"] = 0
        if "injections_count" not in meta.metrics:
            meta.metrics["injections_count"] = 0

        meta.metrics["total_notes_added"] += 1

        # Save
        self.save_notes(notes, meta)
        logger.info("Added note %s: %s...", note_id, text[:50])

        return note_id

    def remove_note(self, note_id: str) -> bool:
        """Remove a note by ID.

        Args:
            note_id: ID of note to remove (e.g., "note-001")

        Returns:
            True if note was removed, False if not found
        """
        data = self._load_yaml_data()
        meta = NotesMetadata.from_dict(data["_meta"])
        notes = [ProjectNote.from_dict(n) for n in data.get("notes", [])]

        # Find and remove
        original_count = len(notes)
        notes = [n for n in notes if n.id != note_id]

        if len(notes) == original_count:
            logger.warning("Note %s not found", note_id)
            return False

        # Update metadata
        meta.count = len(notes)
        meta.updated = datetime.now(UTC).isoformat()

        # Save
        self.save_notes(notes, meta)
        logger.info("Removed note %s", note_id)

        return True

    def clear_notes(self) -> int:
        """Remove all notes.

        Returns:
            Number of notes that were removed
        """
        data = self._load_yaml_data()
        meta = NotesMetadata.from_dict(data["_meta"])
        notes = [ProjectNote.from_dict(n) for n in data.get("notes", [])]

        count = len(notes)

        # Clear notes
        notes = []

        # Update metadata
        meta.count = 0
        meta.updated = datetime.now(UTC).isoformat()

        # Save
        self.save_notes(notes, meta)
        logger.info("Cleared %s notes", count)

        return count

    def get_note(self, note_id: str) -> ProjectNote | None:
        """Get a single note by ID.

        Args:
            note_id: ID of note to retrieve

        Returns:
            ProjectNote if found, None otherwise
        """
        notes = self.load_notes()
        for note in notes:
            if note.id == note_id:
                return note
        return None

    def get_metadata(self) -> NotesMetadata:
        """Get current metadata.

        Returns:
            NotesMetadata object
        """
        data = self._load_yaml_data()
        return NotesMetadata.from_dict(data["_meta"])
