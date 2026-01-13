"""Common utility functions for sbc."""

from pathlib import Path
from typing import Optional, Sequence


def find_file(
    name: str,
    search_dirs: Sequence[str],
    extensions: Sequence[str] = (".yaml", ".yml", ".json"),
) -> Optional[Path]:
    """
    Find a file by name in common search locations.

    Args:
        name: Filename or path to find
        search_dirs: Directory names to search in (e.g., ["quizzes", "flashcards"])
        extensions: File extensions to try if name doesn't have one

    Returns:
        Path to the file if found, None otherwise

    Example:
        >>> find_file("week-01", ["quizzes", "."], [".yaml", ".yml"])
        PosixPath('quizzes/week-01.yaml')
    """
    # Check if it's already a valid path
    path = Path(name)
    if path.exists():
        return path

    # Determine which extensions to try
    if path.suffix in extensions:
        # Already has a valid extension, use as-is
        names_to_try = [name]
    else:
        # Add extensions to try
        names_to_try = [name + ext for ext in extensions]

    # Build search paths
    for dir_name in search_dirs:
        dir_path = Path(dir_name)
        for filename in names_to_try:
            candidate = dir_path / filename
            if candidate.exists():
                return candidate

    return None


def find_quiz_file(name: str) -> Optional[Path]:
    """Find a quiz file by name.

    Args:
        name: Quiz name or path

    Returns:
        Path to quiz file if found, None otherwise
    """
    return find_file(name, search_dirs=["quizzes", "."])


def find_flashcard_file(name: str) -> Optional[Path]:
    """Find a flashcard deck file by name.

    Args:
        name: Deck name or path

    Returns:
        Path to deck file if found, None otherwise
    """
    return find_file(name, search_dirs=["flashcards", "games/flashcards", "."])
