"""
Quiz Widget - Interactive multiple choice quizzes with persistence.

Features:
- YAML/JSON question format
- Multiple attempts with feedback
- Score tracking
- Hierarchical (collapsible) mode
- Hints and explanations
"""

from typing import Any, Optional
from pathlib import Path

import yaml
import ipywidgets as widgets
from IPython.display import display, HTML

from .base import BaseWidget


class Quiz(BaseWidget):
    """
    Interactive quiz widget with persistent state.

    Example:
        quiz = Quiz.from_yaml("quizzes/week-01.yaml")
        quiz.display()

        # Or inline:
        quiz = Quiz(
            name="my-quiz",
            questions=[
                {
                    "question": "What is 2+2?",
                    "options": ["3", "4", "5"],
                    "answer": 1,
                    "explanation": "Basic arithmetic"
                }
            ]
        )
    """

    def __init__(
        self,
        name: str,
        questions: list[dict] = None,
        title: str = None,
        hierarchical: bool = False,
        **kwargs
    ):
        self.questions = questions or []
        self.title = title or name
        self.hierarchical = hierarchical
        self.answers: dict[int, int] = {}
        self.attempts: dict[int, int] = {}

        # Validate questions
        self._validate_questions()

        super().__init__(name, category="quizzes", **kwargs)

    def _validate_questions(self) -> None:
        """
        Validate that all questions are properly formatted.

        Raises:
            ValueError: If any question is invalid
        """
        for i, q in enumerate(self.questions):
            # Check required fields
            if not q.get("question"):
                raise ValueError(f"Question {i+1}: missing 'question' text")

            options = q.get("options", [])
            if not isinstance(options, list):
                raise ValueError(f"Question {i+1}: 'options' must be a list")

            if len(options) < 2:
                raise ValueError(f"Question {i+1}: need at least 2 options, got {len(options)}")

            answer = q.get("answer")
            if answer is None:
                raise ValueError(f"Question {i+1}: missing 'answer' field")

            if not isinstance(answer, int):
                raise ValueError(f"Question {i+1}: 'answer' must be an integer index, got {type(answer).__name__}")

            if not 0 <= answer < len(options):
                raise ValueError(
                    f"Question {i+1}: answer index {answer} out of range "
                    f"(must be 0-{len(options)-1})"
                )

    @classmethod
    def from_yaml(cls, path: str, hierarchical: bool = False, **kwargs) -> "Quiz":
        """Load quiz from YAML file."""
        path = Path(path)
        with open(path) as f:
            data = yaml.safe_load(f)

        name = kwargs.pop("name", path.stem)
        return cls(
            name=name,
            questions=data.get("questions", []),
            title=data.get("title", name),
            hierarchical=hierarchical,
            **kwargs
        )

    @classmethod
    def from_dict(cls, data: dict, **kwargs) -> "Quiz":
        """Create quiz from dictionary."""
        return cls(
            name=data.get("name", "quiz"),
            questions=data.get("questions", []),
            title=data.get("title"),
            **kwargs
        )

    def _build_ui(self) -> widgets.Widget:
        """Build the quiz UI."""
        children = []

        # Title
        if self.title:
            title_html = widgets.HTML(f"<h2>{self.title}</h2>")
            children.append(title_html)

        # Questions
        self._question_widgets = []
        for i, q in enumerate(self.questions):
            q_widget = self._build_question(i, q)
            self._question_widgets.append(q_widget)

            if self.hierarchical:
                accordion = widgets.Accordion(children=[q_widget])
                accordion.set_title(0, f"Q{i+1}: {q['question'][:50]}...")
                children.append(accordion)
            else:
                children.append(q_widget)
                children.append(widgets.HTML("<hr>"))

        # Score display
        self._score_display = widgets.HTML()
        children.append(self._score_display)
        self._update_score()

        return widgets.VBox(children)

    def _build_question(self, index: int, question: dict) -> widgets.Widget:
        """Build UI for a single question."""
        q_text = question.get("question", "")
        options = question.get("options", [])
        correct = question.get("answer", 0)
        explanation = question.get("explanation", "")

        # Question text
        q_html = widgets.HTML(f"<p><strong>Q{index+1}:</strong> {q_text}</p>")

        # Options as radio buttons
        radio = widgets.RadioButtons(
            options=[(opt, i) for i, opt in enumerate(options)],
            value=self.answers.get(index),
            layout=widgets.Layout(width='auto')
        )

        # Feedback area
        feedback = widgets.HTML()

        # Check button
        check_btn = widgets.Button(description="Check", button_style="primary")

        def on_check(b):
            selected = radio.value
            if selected is None:
                feedback.value = "<span style='color: orange'>Please select an answer.</span>"
                return

            self.answers[index] = selected
            self.attempts[index] = self.attempts.get(index, 0) + 1

            if selected == correct:
                feedback.value = f"<span style='color: green'>✓ Correct!</span>"
                if explanation:
                    feedback.value += f"<br><em>{explanation}</em>"
            else:
                feedback.value = f"<span style='color: red'>✗ Try again.</span>"

            self._update_score()
            if self.auto_save:
                self.save()

        check_btn.on_click(on_check)

        return widgets.VBox([q_html, radio, check_btn, feedback])

    def _update_score(self):
        """Update the score display."""
        correct = sum(
            1 for i, q in enumerate(self.questions)
            if self.answers.get(i) == q.get("answer")
        )
        total = len(self.questions)
        pct = (correct / total * 100) if total > 0 else 0

        self._score_display.value = f"""
        <div style='margin-top: 20px; padding: 10px; background: #f0f0f0; border-radius: 5px;'>
            <strong>Score:</strong> {correct}/{total} ({pct:.0f}%)
        </div>
        """

        if correct == total and total > 0:
            self.mark_complete()
            self.submit_score(
                activity=f"quiz:{self.name}",
                score=correct * 10,
                details=f"Score: {correct}/{total}"
            )

    def _get_state(self) -> dict[str, Any]:
        return {
            "answers": self.answers,
            "attempts": self.attempts,
        }

    def _set_state(self, state: dict[str, Any]) -> None:
        # Normalize keys to integers (JSON serializes dict keys as strings)
        raw_answers = state.get("answers", {})
        raw_attempts = state.get("attempts", {})

        self.answers = {int(k): v for k, v in raw_answers.items()}
        self.attempts = {int(k): v for k, v in raw_attempts.items()}
