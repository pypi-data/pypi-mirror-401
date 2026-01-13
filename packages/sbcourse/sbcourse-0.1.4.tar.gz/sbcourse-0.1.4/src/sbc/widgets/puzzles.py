"""
Puzzles Widget - Code challenges and debugging exercises.

Features:
- Code completion puzzles
- Debug challenges
- Output prediction
- Syntax exercises
"""

from typing import Any
import ipywidgets as widgets

from .base import BaseWidget


class Puzzles(BaseWidget):
    """
    Interactive code puzzle widget.

    Example:
        puzzles = Puzzles.from_file("puzzles/week-01.yaml")
        puzzles.display()
    """

    def __init__(
        self,
        name: str,
        puzzles: list[dict] = None,
        title: str = None,
        **kwargs
    ):
        self.puzzles = puzzles or []
        self.title = title or name
        self.current_index = 0
        self.solved = set()

        super().__init__(name, category="puzzles", **kwargs)

    def _build_ui(self) -> widgets.Widget:
        """Build the puzzle UI."""
        header = widgets.HTML(f"<h2>🧩 {self.title}</h2>")

        self._progress = widgets.HTML()
        self._puzzle_html = widgets.HTML()
        self._input = widgets.Textarea(
            placeholder="Enter your answer...",
            layout=widgets.Layout(width='100%', height='100px')
        )
        self._feedback = widgets.HTML()

        check_btn = widgets.Button(description="Check Answer", button_style="primary")
        check_btn.on_click(self._check_answer)

        next_btn = widgets.Button(description="Next Puzzle", button_style="info")
        next_btn.on_click(lambda b: self._next_puzzle())

        self._update_display()

        return widgets.VBox([
            header,
            self._progress,
            self._puzzle_html,
            self._input,
            widgets.HBox([check_btn, next_btn]),
            self._feedback,
        ])

    def _update_display(self):
        """Update the puzzle display."""
        self._progress.value = f"<p>Puzzle {self.current_index + 1}/{len(self.puzzles)} | Solved: {len(self.solved)}</p>"

        if not self.puzzles:
            self._puzzle_html.value = "<p><em>No puzzles loaded.</em></p>"
            return

        puzzle = self.puzzles[self.current_index]
        ptype = puzzle.get("type", "complete")
        code = puzzle.get("code", "")
        prompt = puzzle.get("prompt", "Complete the code:")

        self._puzzle_html.value = f"""
            <p><strong>{prompt}</strong></p>
            <pre style='background: #f5f5f5; padding: 10px; border-radius: 5px;'>{code}</pre>
        """

    def _check_answer(self, b):
        """Check the submitted answer."""
        if not self.puzzles:
            return

        puzzle = self.puzzles[self.current_index]
        answer = puzzle.get("answer", "")
        user_answer = self._input.value.strip()

        if user_answer.lower() == answer.lower():
            self.solved.add(self.current_index)
            self._feedback.value = "<span style='color: green'>✓ Correct!</span>"

            if self.auto_save:
                self.save()

            if len(self.solved) == len(self.puzzles):
                self.mark_complete()
                self.submit_score(
                    activity=f"puzzles:{self.name}",
                    score=len(self.puzzles) * 25,
                    details=f"Solved {len(self.puzzles)} puzzles"
                )
        else:
            hint = puzzle.get("hint", "")
            self._feedback.value = f"<span style='color: red'>✗ Not quite.</span>"
            if hint:
                self._feedback.value += f"<br><em>Hint: {hint}</em>"

    def _next_puzzle(self):
        """Move to next puzzle."""
        self.current_index = (self.current_index + 1) % len(self.puzzles)
        self._input.value = ""
        self._feedback.value = ""
        self._update_display()

    def _get_state(self) -> dict[str, Any]:
        return {
            "current_index": self.current_index,
            "solved": list(self.solved),
        }

    def _set_state(self, state: dict[str, Any]) -> None:
        self.current_index = int(state.get("current_index", 0))
        # Ensure solved indices are integers
        self.solved = set(int(x) for x in state.get("solved", []))
