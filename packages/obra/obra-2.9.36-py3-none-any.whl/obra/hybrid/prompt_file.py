"""Prompt file lifecycle management for hybrid orchestration."""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from uuid import uuid4

logger = logging.getLogger(__name__)


class PromptFileManager:
    """Manage prompt file creation and cleanup for LLM invocations."""

    DEFAULT_PROMPT_MAX_FILES = 200
    INDEX_FILENAME = ".prompt-index.json"

    def __init__(
        self,
        working_dir: Path,
        retain: bool = False,
        run_id: str | None = None,
        max_files: int | None = None,
    ) -> None:
        self._working_dir = working_dir
        self._retain = retain
        self._run_id = run_id or uuid4().hex
        self._prompt_root = self._working_dir / ".obra" / "prompts"
        self._run_dir = self._prompt_root / self._run_id
        self._max_files = max_files or self.DEFAULT_PROMPT_MAX_FILES
        self._index_path = self._prompt_root / self.INDEX_FILENAME

    def write_prompt(self, prompt: str) -> tuple[Path, str]:
        """Write prompt to a file and return (path, instruction)."""
        self._run_dir.mkdir(parents=True, exist_ok=True)
        filename = f".obra-prompt-{uuid4().hex[:8]}.txt"
        filepath = self._run_dir / filename
        filepath.write_text(prompt, encoding="utf-8")
        self._record_prompt(filepath)
        instruction_path = self._relative_instruction_path(filepath)
        instruction = f"Read and execute all instructions in {instruction_path}"
        return filepath, instruction

    def cleanup(self, filepath: Path) -> None:
        """Apply prompt cleanup policy unless retention is enabled."""
        if self._retain:
            return
        removed = self._cleanup_over_cap(protected_run_ids={self._run_id})
        if removed:
            logger.debug("Removed %d prompt artifact(s) (count cap).", removed)

    def cleanup_stale_prompt_artifacts(self) -> int:
        """Remove prompt artifacts that exceed the max-files cap."""
        removed = self._cleanup_over_cap(protected_run_ids={self._run_id})
        if removed:
            logger.debug("Removed %d prompt artifact(s) during preflight cleanup.", removed)
        return removed

    @classmethod
    def cleanup_orphaned(cls, working_dir: Path, max_files: int | None = None) -> int:
        """Remove prompt artifacts over the max-files cap in the working directory."""
        manager = cls(working_dir, retain=False, max_files=max_files)
        return manager.cleanup_stale_prompt_artifacts()

    def _cleanup_run_dir_path(self, run_dir: Path) -> None:
        if not run_dir.exists():
            return
        if any(run_dir.iterdir()):
            return
        run_dir.rmdir()

    def _relative_instruction_path(self, filepath: Path) -> str:
        try:
            relative = filepath.relative_to(self._working_dir)
        except ValueError:
            return str(filepath)
        if os.name == "nt":
            return str(relative)
        return relative.as_posix()

    def _relative_index_path(self, filepath: Path) -> str:
        try:
            relative = filepath.relative_to(self._working_dir)
        except ValueError:
            return str(filepath)
        return relative.as_posix()

    def _record_prompt(self, filepath: Path) -> None:
        index = self._load_index()
        path_key = self._relative_index_path(filepath)
        for entry in index["entries"]:
            if isinstance(entry, dict) and entry.get("path") == path_key:
                self._save_index(index)
                return
        entry = {
            "id": index["next_id"],
            "run_id": self._run_id,
            "path": path_key,
        }
        index["next_id"] += 1
        index["entries"].append(entry)
        self._save_index(index)

    def _load_index(self) -> dict[str, object]:
        if not self._prompt_root.exists():
            return {"next_id": 1, "entries": []}
        if self._index_path.exists():
            try:
                data = json.loads(self._index_path.read_text(encoding="utf-8"))
                if isinstance(data, dict) and "entries" in data and "next_id" in data:
                    return data
            except (OSError, json.JSONDecodeError):
                logger.warning("Failed to load prompt index; rebuilding.")
        return self._build_index_from_scan()

    def _build_index_from_scan(self) -> dict[str, object]:
        prompt_files = sorted(
            self._prompt_root.rglob(".obra-prompt-*.txt"),
            key=lambda path: path.as_posix(),
        )
        entries = []
        next_id = 1
        for path in prompt_files:
            entries.append(
                {
                    "id": next_id,
                    "run_id": path.parent.name,
                    "path": self._relative_index_path(path),
                }
            )
            next_id += 1
        return {"next_id": next_id, "entries": entries}

    def _save_index(self, index: dict[str, object]) -> None:
        self._prompt_root.mkdir(parents=True, exist_ok=True)
        self._index_path.write_text(json.dumps(index, indent=2), encoding="utf-8")

    def _entry_path(self, entry: dict[str, object]) -> Path:
        path = entry.get("path")
        if isinstance(path, str):
            candidate = Path(path)
            if candidate.is_absolute():
                return candidate
            return self._working_dir / candidate
        return self._working_dir

    def _cleanup_over_cap(self, protected_run_ids: set[str] | None = None) -> int:
        if self._max_files <= 0:
            return 0
        index = self._load_index()
        entries = []
        for entry in index["entries"]:
            if not isinstance(entry, dict):
                continue
            entry_path = self._entry_path(entry)
            if entry_path.exists():
                entries.append(entry)
            else:
                logger.debug("Pruned missing prompt entry: %s", entry.get("path"))
        index["entries"] = entries

        legacy_files = sorted(
            self._working_dir.glob(".obra-prompt-*.txt"),
            key=lambda path: path.as_posix(),
        )
        total_existing = len(entries) + len(legacy_files)
        if total_existing == 0 and not self._prompt_root.exists():
            return 0
        if total_existing <= self._max_files:
            self._save_index(index)
            return 0

        to_delete = total_existing - self._max_files
        removed = 0
        for legacy in legacy_files:
            if removed >= to_delete:
                break
            legacy.unlink(missing_ok=True)
            removed += 1

        protected = protected_run_ids or set()
        kept_entries = []
        for entry in sorted(entries, key=self._entry_sort_key):
            if removed >= to_delete:
                kept_entries.append(entry)
                continue
            if entry.get("run_id") in protected:
                kept_entries.append(entry)
                continue
            entry_path = self._entry_path(entry)
            entry_path.unlink(missing_ok=True)
            removed += 1
            self._cleanup_run_dir_path(entry_path.parent)

        index["entries"] = kept_entries
        self._save_index(index)
        return removed

    @staticmethod
    def _entry_sort_key(entry: dict[str, object]) -> int:
        try:
            return int(entry.get("id", 0))
        except (TypeError, ValueError):
            return 0


__all__ = ["PromptFileManager"]
