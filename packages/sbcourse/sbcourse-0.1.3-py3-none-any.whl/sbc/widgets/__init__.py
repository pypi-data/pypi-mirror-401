"""
SBC Widgets - Persistent interactive widgets for Jupyter notebooks.

All widgets automatically save their state and can be resumed later.
"""

from .base import BaseWidget
from .quiz import Quiz
from .reflection import Reflection
from .trivia import Trivia
from .flashcards import Flashcards
from .puzzles import Puzzles

__all__ = [
    "BaseWidget",
    "Quiz",
    "Reflection",
    "Trivia",
    "Flashcards",
    "Puzzles",
]
