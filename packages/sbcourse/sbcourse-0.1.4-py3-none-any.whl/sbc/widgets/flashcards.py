"""
Flashcards Widget - Spaced repetition learning system.

Features:
- Flip card interface
- Spaced repetition algorithm
- Progress tracking
- Deck management
"""

from typing import Any
from pathlib import Path
import yaml
import ipywidgets as widgets

from .base import BaseWidget
from ..utils import find_flashcard_file


class Flashcards(BaseWidget):
    """
    Interactive flashcard widget with spaced repetition.

    Example:
        flashcards = Flashcards.from_deck("derivatives")
        flashcards.display()
    """

    def __init__(
        self,
        name: str,
        cards: list[dict] = None,
        title: str = None,
        **kwargs
    ):
        self.cards = cards or []
        self.title = title or name
        self.current_index = 0
        self.revealed = False
        self.scores = {}  # card_id -> {"correct": int, "incorrect": int, "ease": float}

        super().__init__(name, category="flashcards", **kwargs)

    @classmethod
    def from_deck(cls, name: str, **kwargs) -> "Flashcards":
        """Load flashcards from deck file."""
        path = find_flashcard_file(name)
        if path is None:
            raise FileNotFoundError(f"Deck not found: {name}")

        with open(path) as f:
            data = yaml.safe_load(f)

        return cls(
            name=name,
            cards=data.get("cards", []),
            title=data.get("title", name),
            **kwargs
        )

    def _build_ui(self) -> widgets.Widget:
        """Build the flashcard UI."""
        # Header
        header = widgets.HTML(f"<h2>📚 {self.title}</h2>")

        # Progress
        self._progress = widgets.HTML()

        # Card display
        self._card_html = widgets.HTML()

        # Flip button
        flip_btn = widgets.Button(description="Flip Card", button_style="info")
        flip_btn.on_click(lambda b: self._flip_card())

        # Rating buttons (hidden until revealed) - must be created before _show_card
        self._rating_box = widgets.HBox([
            widgets.Button(description="❌ Wrong", button_style="danger"),
            widgets.Button(description="😐 Hard", button_style="warning"),
            widgets.Button(description="✓ Good", button_style="success"),
            widgets.Button(description="⚡ Easy", button_style="primary"),
        ])
        self._rating_box.layout.display = 'none'

        for i, btn in enumerate(self._rating_box.children):
            btn.on_click(lambda b, rating=i: self._rate_card(rating))

        # Initialize display after all widgets are created
        self._update_progress()
        self._show_card()

        return widgets.VBox([
            header,
            self._progress,
            self._card_html,
            flip_btn,
            self._rating_box,
        ])

    def _update_progress(self):
        """Update progress display."""
        learned = sum(1 for s in self.scores.values() if s.get("correct", 0) >= 3)
        self._progress.value = f"""
            <p>Card {self.current_index + 1}/{len(self.cards)} |
            Learned: {learned}/{len(self.cards)}</p>
        """

    def _show_card(self):
        """Display the current card (front)."""
        if not self.cards:
            self._card_html.value = "<p><em>No cards in deck.</em></p>"
            return

        card = self.cards[self.current_index]
        self._card_html.value = f"""
            <div style='padding: 40px; background: #f5f5f5; border-radius: 10px;
                        text-align: center; min-height: 150px; margin: 20px 0;'>
                <h3>{card.get('front', '')}</h3>
            </div>
        """
        self.revealed = False
        self._rating_box.layout.display = 'none'

    def _flip_card(self):
        """Flip to show the back of the card."""
        if not self.cards:
            return

        card = self.cards[self.current_index]
        self._card_html.value = f"""
            <div style='padding: 40px; background: #e8f4e8; border-radius: 10px;
                        text-align: center; min-height: 150px; margin: 20px 0;'>
                <h3>{card.get('back', '')}</h3>
            </div>
        """
        self.revealed = True
        self._rating_box.layout.display = 'flex'

    def _rate_card(self, rating: int):
        """Rate the card and move to next."""
        card_id = str(self.current_index)
        if card_id not in self.scores:
            self.scores[card_id] = {"correct": 0, "incorrect": 0, "ease": 2.5}

        if rating >= 2:  # Good or Easy
            self.scores[card_id]["correct"] += 1
        else:
            self.scores[card_id]["incorrect"] += 1

        # Move to next card
        self.current_index = (self.current_index + 1) % len(self.cards)
        self._show_card()
        self._update_progress()

        if self.auto_save:
            self.save()

        # Check if all cards learned
        learned = sum(1 for s in self.scores.values() if s.get("correct", 0) >= 3)
        if learned == len(self.cards):
            self.mark_complete()
            self.submit_score(
                activity=f"flashcards:{self.name}",
                score=len(self.cards) * 10,
                details=f"Mastered {len(self.cards)} cards"
            )

    def _get_state(self) -> dict[str, Any]:
        return {
            "current_index": self.current_index,
            "scores": self.scores,
        }

    def _set_state(self, state: dict[str, Any]) -> None:
        # Ensure integer type for current_index
        self.current_index = int(state.get("current_index", 0))
        self.scores = state.get("scores", {})
