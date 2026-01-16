"""Prompt file lifecycle management for hybrid orchestration."""

from __future__ import annotations

from pathlib import Path
import shutil
import time
from uuid import uuid4


class PromptFileManager:
    """Manage prompt file creation and cleanup for LLM invocations."""

    DEFAULT_PROMPT_STALE_AGE_S = 21600

    def __init__(
        self,
        working_dir: Path,
        retain: bool = False,
        run_id: str | None = None,
        stale_age_s: int | None = None,
    ) -> None:
        self._working_dir = working_dir
        self._retain = retain
        self._run_id = run_id or uuid4().hex
        self._prompt_root = self._working_dir / ".obra" / "prompts"
        self._run_dir = self._prompt_root / self._run_id
        self._stale_age_s = stale_age_s or self.DEFAULT_PROMPT_STALE_AGE_S

    def write_prompt(self, prompt: str) -> tuple[Path, str]:
        """Write prompt to a file and return (path, instruction)."""
        self._run_dir.mkdir(parents=True, exist_ok=True)
        filename = f".obra-prompt-{uuid4().hex[:8]}.txt"
        filepath = self._run_dir / filename
        filepath.write_text(prompt, encoding="utf-8")
        instruction_path = self._relative_instruction_path(filepath)
        instruction = f"Read and execute all instructions in {instruction_path}"
        return filepath, instruction

    def cleanup(self, filepath: Path) -> None:
        """Delete prompt file unless retention is enabled."""
        if self._retain:
            return
        filepath.unlink(missing_ok=True)
        if filepath.parent == self._run_dir:
            self._cleanup_run_dir()

    def cleanup_stale_prompt_artifacts(self) -> int:
        """Remove stale prompt directories and legacy files."""
        cutoff = time.time() - self._stale_age_s
        removed = 0
        removed += self._cleanup_stale_run_dirs(cutoff)
        removed += self._cleanup_stale_legacy_files(cutoff)
        return removed

    @classmethod
    def cleanup_orphaned(cls, working_dir: Path) -> int:
        """Remove stale prompt artifacts in the working directory."""
        manager = cls(working_dir, retain=False)
        return manager.cleanup_stale_prompt_artifacts()

    def _cleanup_run_dir(self) -> None:
        if not self._run_dir.exists():
            return
        if any(self._run_dir.iterdir()):
            return
        self._run_dir.rmdir()
        if self._prompt_root.exists() and not any(self._prompt_root.iterdir()):
            self._prompt_root.rmdir()

    def _cleanup_stale_run_dirs(self, cutoff: float) -> int:
        if not self._prompt_root.exists():
            return 0
        removed = 0
        for run_dir in self._prompt_root.iterdir():
            if run_dir == self._run_dir or not run_dir.is_dir():
                continue
            if self._is_path_stale(run_dir, cutoff):
                shutil.rmtree(run_dir, ignore_errors=True)
                removed += 1
        return removed

    def _cleanup_stale_legacy_files(self, cutoff: float) -> int:
        removed = 0
        for prompt_file in self._working_dir.glob(".obra-prompt-*.txt"):
            if self._is_path_stale(prompt_file, cutoff):
                prompt_file.unlink(missing_ok=True)
                removed += 1
        return removed

    def _relative_instruction_path(self, filepath: Path) -> str:
        try:
            relative = filepath.relative_to(self._working_dir)
        except ValueError:
            return str(filepath)
        return relative.as_posix()

    def _is_path_stale(self, path: Path, cutoff: float) -> bool:
        try:
            return self._latest_mtime(path) < cutoff
        except OSError:
            return False

    def _latest_mtime(self, path: Path) -> float:
        latest = path.stat().st_mtime
        if path.is_dir():
            for entry in path.rglob("*"):
                try:
                    entry_mtime = entry.stat().st_mtime
                except OSError:
                    continue
                latest = max(latest, entry_mtime)
        return latest


__all__ = ["PromptFileManager"]
