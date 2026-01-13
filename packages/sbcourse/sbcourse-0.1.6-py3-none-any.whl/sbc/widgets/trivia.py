"""
Trivia Widget - Timed quiz game with scoring.

Features:
- Topic-based questions
- Difficulty levels
- Streak tracking
- Timed responses
- Leaderboard integration
"""

from typing import Any, Optional
import ipywidgets as widgets

from .base import BaseWidget


class Trivia(BaseWidget):
    """
    Interactive trivia game widget.

    Example:
        trivia = Trivia(topic="calculus", num_questions=5)
        trivia.display()
    """

    def __init__(
        self,
        topic: str = None,
        num_questions: int = 5,
        difficulty: str = "medium",
        questions: list[dict] = None,
        **kwargs
    ):
        name = kwargs.pop("name", f"trivia-{topic or 'general'}")
        self.topic = topic
        self.num_questions = num_questions
        self.difficulty = difficulty
        self.questions = questions or []

        self.current_index = 0
        self.score = 0
        self.streak = 0
        self.max_streak = 0

        super().__init__(name, category="trivia", **kwargs)

    def _build_ui(self) -> widgets.Widget:
        """Build the trivia game UI."""
        # Header
        header = widgets.HTML(f"""
            <h2>🎯 Trivia: {self.topic or 'General'}</h2>
            <p>Difficulty: {self.difficulty} | Questions: {self.num_questions}</p>
        """)

        # Score display
        self._score_html = widgets.HTML()
        self._update_score_display()

        # Question area
        self._question_html = widgets.HTML("<p>Loading questions...</p>")

        # Options
        self._options = widgets.RadioButtons(options=[], layout=widgets.Layout(width='auto'))

        # Submit button
        self._submit_btn = widgets.Button(description="Submit Answer", button_style="primary")
        self._submit_btn.on_click(self._on_submit)

        # Feedback
        self._feedback = widgets.HTML()

        # Next button (hidden initially)
        self._next_btn = widgets.Button(description="Next Question", button_style="info")
        self._next_btn.on_click(self._on_next)
        self._next_btn.layout.display = 'none'

        # Load first question
        if self.questions:
            self._show_question()
        else:
            self._question_html.value = "<p><em>No questions loaded. Provide questions or load from file.</em></p>"

        return widgets.VBox([
            header,
            self._score_html,
            self._question_html,
            self._options,
            widgets.HBox([self._submit_btn, self._next_btn]),
            self._feedback,
        ])

    def _update_score_display(self):
        """Update the score display."""
        self._score_html.value = f"""
            <div style='display: flex; gap: 20px; margin: 10px 0;'>
                <span>🏆 Score: <strong>{self.score}</strong></span>
                <span>🔥 Streak: <strong>{self.streak}</strong></span>
                <span>📊 Max Streak: <strong>{self.max_streak}</strong></span>
            </div>
        """

    def _show_question(self):
        """Display the current question."""
        if self.current_index >= len(self.questions):
            self._end_game()
            return

        q = self.questions[self.current_index]
        self._question_html.value = f"""
            <p><strong>Q{self.current_index + 1}/{len(self.questions)}:</strong> {q['question']}</p>
        """
        self._options.options = [(opt, i) for i, opt in enumerate(q.get('options', []))]
        self._options.value = None
        self._feedback.value = ""
        self._submit_btn.layout.display = 'inline-block'
        self._next_btn.layout.display = 'none'

    def _on_submit(self, b):
        """Handle answer submission."""
        if self._options.value is None:
            self._feedback.value = "<span style='color: orange'>Please select an answer.</span>"
            return

        q = self.questions[self.current_index]
        correct = q.get('answer', 0)

        if self._options.value == correct:
            self.streak += 1
            self.max_streak = max(self.max_streak, self.streak)
            points = 10 * (1 + self.streak // 3)  # Bonus for streaks
            self.score += points
            self._feedback.value = f"<span style='color: green'>✓ Correct! +{points} points</span>"
        else:
            self.streak = 0
            self._feedback.value = f"<span style='color: red'>✗ Wrong! The answer was: {q['options'][correct]}</span>"

        self._update_score_display()
        self._submit_btn.layout.display = 'none'
        self._next_btn.layout.display = 'inline-block'

        if self.auto_save:
            self.save()

    def _on_next(self, b):
        """Move to next question."""
        self.current_index += 1
        self._show_question()

    def _end_game(self):
        """End the trivia game."""
        self._question_html.value = f"""
            <h3>🎉 Game Complete!</h3>
            <p>Final Score: <strong>{self.score}</strong></p>
            <p>Max Streak: <strong>{self.max_streak}</strong></p>
        """
        self._options.layout.display = 'none'
        self._submit_btn.layout.display = 'none'
        self._next_btn.layout.display = 'none'

        self.mark_complete()
        self.submit_score(
            activity=f"trivia:{self.topic or 'general'}",
            score=self.score,
            details=f"Streak: {self.max_streak} | Questions: {len(self.questions)}"
        )

    def _get_state(self) -> dict[str, Any]:
        return {
            "current_index": self.current_index,
            "score": self.score,
            "streak": self.streak,
            "max_streak": self.max_streak,
        }

    def _set_state(self, state: dict[str, Any]) -> None:
        # Ensure integer types for state values
        self.current_index = int(state.get("current_index", 0))
        self.score = int(state.get("score", 0))
        self.streak = int(state.get("streak", 0))
        self.max_streak = int(state.get("max_streak", 0))
