"""
Base class for persistent widgets.

Provides automatic state persistence, styling, and common functionality
shared by all SBC widgets.
"""

from abc import ABC, abstractmethod
from typing import Any, Optional
from pathlib import Path

import ipywidgets as widgets
from IPython.display import display

from ..persistence import Storage


class BaseWidget(ABC):
    """
    Abstract base class for persistent widgets.

    Provides:
    - Automatic state persistence to JSON
    - Common styling and theming
    - Progress tracking
    - Leaderboard integration hooks

    Subclasses must implement:
    - _build_ui(): Create the widget UI
    - _get_state(): Return state dict to persist
    - _set_state(): Restore from state dict
    """

    def __init__(
        self,
        name: str,
        category: str = "widgets",
        auto_save: bool = True,
        submit_scores: bool = True,
    ):
        """
        Initialize the widget.

        Args:
            name: Unique identifier for this widget instance
            category: Storage category (e.g., "quizzes", "reflections")
            auto_save: Automatically save state on changes
            submit_scores: Submit scores to leaderboard if configured
        """
        self.name = name
        self.category = category
        self.auto_save = auto_save
        self.submit_scores = submit_scores

        # Initialize storage
        self._storage = Storage(name, category=category, auto_save=auto_save)

        # UI container
        self._container: Optional[widgets.Widget] = None

        # Load any existing state
        saved_state = self._storage.get("state", {})
        if saved_state:
            self._set_state(saved_state)

    def display(self):
        """Build and display the widget."""
        if self._container is None:
            self._container = self._build_ui()
        display(self._container)

    def save(self):
        """Save current state to storage."""
        state = self._get_state()
        self._storage.set("state", state)

    def reset(self):
        """Reset widget to initial state."""
        self._storage.clear()
        self._container = None

    def submit_score(self, activity: str, score: int, details: str = None):
        """Submit score to leaderboard if configured."""
        if not self.submit_scores:
            return

        try:
            from ..leaderboard import submit_score
            submit_score(
                activity=activity,
                score=score,
                details=details,
                session_data={"widget": self.name}
            )
        except ImportError:
            # Leaderboard module not available - this is expected in some setups
            pass
        except ConnectionError:
            # Network issue - acceptable to skip silently
            pass
        except Exception as e:
            # Log unexpected errors but don't crash the widget
            import warnings
            warnings.warn(f"Failed to submit score to leaderboard: {e}")

    @abstractmethod
    def _build_ui(self) -> widgets.Widget:
        """Build and return the widget UI. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def _get_state(self) -> dict[str, Any]:
        """Return the current state as a dict. Must be implemented by subclasses."""
        pass

    @abstractmethod
    def _set_state(self, state: dict[str, Any]) -> None:
        """Restore state from a dict. Must be implemented by subclasses."""
        pass

    @property
    def is_complete(self) -> bool:
        """Check if the widget activity is complete."""
        return self._storage.get("completed", False)

    def mark_complete(self):
        """Mark the widget activity as complete."""
        self._storage.set("completed", True)

    def __repr__(self) -> str:
        status = "complete" if self.is_complete else "in progress"
        return f"{self.__class__.__name__}({self.name!r}, {status})"
