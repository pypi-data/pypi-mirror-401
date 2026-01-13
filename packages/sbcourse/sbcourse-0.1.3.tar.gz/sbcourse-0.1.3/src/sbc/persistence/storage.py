"""
JSON-based persistent storage for widget state.

Provides automatic save/load of widget state to JSON files,
supporting both course-level and user-level storage.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


def sanitize_filename(name: str) -> str:
    """
    Sanitize a name for safe filesystem use.

    Removes or replaces characters that are unsafe on various filesystems
    (Windows, macOS, Linux).

    Args:
        name: The name to sanitize

    Returns:
        A filesystem-safe version of the name

    Raises:
        ValueError: If name is empty or results in empty string after sanitization
    """
    if not name:
        raise ValueError("Name cannot be empty")

    # Remove or replace unsafe characters
    # < > : " / \ | ? * are unsafe on Windows
    # Null bytes and control characters (0x00-0x1f) are unsafe everywhere
    safe = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '-', name)

    # Collapse multiple dashes into one
    safe = re.sub(r'-+', '-', safe)

    # Remove leading/trailing dashes, dots, and spaces
    # (Leading dots create hidden files on Unix, trailing dots cause issues on Windows)
    safe = safe.strip('.- ')

    if not safe:
        raise ValueError(f"Name '{name}' results in empty string after sanitization")

    # Limit length (most filesystems have 255 char limit, leave room for extension)
    if len(safe) > 200:
        safe = safe[:200]

    return safe


def get_storage_path(
    name: str,
    category: str = "state",
    base_dir: Optional[Path] = None,
    user_dir: bool = False,
) -> Path:
    """
    Get the storage path for a given name and category.

    Args:
        name: Identifier for the storage (e.g., "quiz-week-01")
        category: Category subdirectory (e.g., "state", "scores", "reflections")
        base_dir: Base directory for storage. Defaults to .sbc/ in current dir
        user_dir: If True, use ~/.sbc/ for user-level storage

    Returns:
        Path to the JSON storage file

    Raises:
        ValueError: If name is invalid
    """
    if user_dir:
        base = Path.home() / ".sbc"
    elif base_dir:
        base = Path(base_dir)
    else:
        base = Path.cwd() / ".sbc"

    storage_dir = base / category
    storage_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize name for filesystem
    safe_name = sanitize_filename(name)
    return storage_dir / f"{safe_name}.json"


class Storage:
    """
    Persistent JSON storage with automatic save/load.

    Example:
        storage = Storage("quiz-week-01")
        storage.set("answers", {"q1": "a", "q2": "b"})
        storage.set("score", 85)
        storage.save()

        # Later...
        storage = Storage("quiz-week-01")
        answers = storage.get("answers", {})
    """

    def __init__(
        self,
        name: str,
        category: str = "state",
        base_dir: Optional[Path] = None,
        user_dir: bool = False,
        auto_save: bool = True,
    ):
        """
        Initialize storage.

        Args:
            name: Identifier for this storage
            category: Category subdirectory
            base_dir: Base directory override
            user_dir: Use user home directory
            auto_save: Automatically save after each set()
        """
        self.name = name
        self.category = category
        self.path = get_storage_path(name, category, base_dir, user_dir)
        self.auto_save = auto_save
        self._data: dict[str, Any] = {}
        self._metadata: dict[str, Any] = {
            "created_at": None,
            "updated_at": None,
            "version": 1,
        }
        self._load()

    def _load(self) -> None:
        """Load data from disk if exists."""
        if self.path.exists():
            try:
                with open(self.path, "r") as f:
                    stored = json.load(f)
                    self._data = stored.get("data", {})
                    self._metadata = stored.get("metadata", self._metadata)
            except (json.JSONDecodeError, IOError):
                # Corrupted or unreadable - start fresh
                self._data = {}

    def save(self) -> None:
        """Save current state to disk."""
        self._metadata["updated_at"] = datetime.now().isoformat()
        if self._metadata["created_at"] is None:
            self._metadata["created_at"] = self._metadata["updated_at"]

        with open(self.path, "w") as f:
            json.dump({
                "data": self._data,
                "metadata": self._metadata,
            }, f, indent=2, default=str)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value by key."""
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a value by key."""
        self._data[key] = value
        if self.auto_save:
            self.save()

    def update(self, data: dict[str, Any]) -> None:
        """Update multiple values at once."""
        self._data.update(data)
        if self.auto_save:
            self.save()

    def delete(self, key: str) -> None:
        """Delete a key."""
        if key in self._data:
            del self._data[key]
            if self.auto_save:
                self.save()

    def clear(self) -> None:
        """Clear all data."""
        self._data = {}
        if self.auto_save:
            self.save()

    def keys(self) -> list[str]:
        """Get all keys."""
        return list(self._data.keys())

    def all(self) -> dict[str, Any]:
        """Get all data as a dict."""
        return self._data.copy()

    @property
    def created_at(self) -> Optional[str]:
        """When this storage was first created."""
        return self._metadata.get("created_at")

    @property
    def updated_at(self) -> Optional[str]:
        """When this storage was last updated."""
        return self._metadata.get("updated_at")

    def __repr__(self) -> str:
        return f"Storage({self.name!r}, keys={self.keys()})"
