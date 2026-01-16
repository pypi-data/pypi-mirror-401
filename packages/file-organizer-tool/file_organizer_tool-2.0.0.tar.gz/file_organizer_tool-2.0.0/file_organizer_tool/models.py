# file_organizer_tool/models.py
"""Data models for file organization results."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class FileMove:
    """Represents a single file move operation."""
    source: Path
    destination: Path
    category: str
    status: str  # 'moved', 'skipped', 'error'
    error_message: Optional[str] = None

    def __str__(self) -> str:
        if self.status == 'error':
            return f"[ERROR] {self.source.name}: {self.error_message}"
        elif self.status == 'skipped':
            return f"[SKIP] {self.source.name} -> {self.category}/"
        return f"[MOVED] {self.source.name} -> {self.category}/"


@dataclass
class OrganizationResult:
    """Result summary of a file organization operation."""
    total_files: int = 0
    moved: int = 0
    skipped: int = 0
    errors: int = 0
    moves: list[FileMove] = field(default_factory=list)

    def add_move(self, move: FileMove) -> None:
        """Add a file move result and update counters."""
        self.moves.append(move)
        self.total_files += 1
        if move.status == 'moved':
            self.moved += 1
        elif move.status == 'skipped':
            self.skipped += 1
        elif move.status == 'error':
            self.errors += 1

    def summary(self) -> str:
        """Return a summary string of the organization."""
        return (
            f"Organization complete: {self.moved} moved, "
            f"{self.skipped} skipped, {self.errors} errors "
            f"(total: {self.total_files} files)"
        )
