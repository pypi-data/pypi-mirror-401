"""
Reflection Widget - Free-form text responses with persistence.

Features:
- Multi-prompt reflections
- Auto-save drafts
- Word count tracking
- Optional AI feedback hooks
"""

from typing import Any
import ipywidgets as widgets

from .base import BaseWidget


class Reflection(BaseWidget):
    """
    Interactive reflection widget with persistent state.

    Example:
        reflection = Reflection(
            name="week-01",
            prompt="What did you learn this week?"
        )
        reflection.display()
    """

    def __init__(
        self,
        name: str,
        prompt: str = "",
        prompts: list[str] = None,
        min_words: int = 50,
        **kwargs
    ):
        self.prompt = prompt
        self.prompts = prompts or ([prompt] if prompt else [])
        self.min_words = min_words
        self.responses = {}

        super().__init__(name, category="reflections", **kwargs)

    def _build_ui(self) -> widgets.Widget:
        """Build the reflection UI."""
        children = []

        self._text_areas = []
        for i, prompt in enumerate(self.prompts):
            # Prompt text
            prompt_html = widgets.HTML(f"<p><strong>{prompt}</strong></p>")

            # Text area
            text = widgets.Textarea(
                value=self.responses.get(i, ""),
                placeholder="Write your reflection here...",
                layout=widgets.Layout(width='100%', height='150px')
            )

            # Word count
            word_count = widgets.HTML()

            def update_count(change, idx=i, wc=word_count):
                words = len(change['new'].split())
                color = 'green' if words >= self.min_words else 'orange'
                wc.value = f"<span style='color: {color}'>{words} words</span>"
                self.responses[idx] = change['new']
                if self.auto_save:
                    self.save()

            text.observe(update_count, names='value')
            update_count({'new': text.value})

            self._text_areas.append(text)
            children.extend([prompt_html, text, word_count, widgets.HTML("<hr>")])

        # Submit button
        submit_btn = widgets.Button(
            description="Submit Reflection",
            button_style="success"
        )
        self._feedback = widgets.HTML()

        def on_submit(b):
            total_words = sum(len(r.split()) for r in self.responses.values())
            if total_words < self.min_words * len(self.prompts):
                self._feedback.value = (
                    f"<span style='color: orange'>Please write at least "
                    f"{self.min_words} words per prompt.</span>"
                )
                return

            self.mark_complete()
            self.submit_score(
                activity=f"reflection:{self.name}",
                score=25,
                details=f"Words: {total_words}"
            )
            self._feedback.value = (
                "<span style='color: green'>✓ Reflection submitted!</span>"
            )

        submit_btn.on_click(on_submit)
        children.extend([submit_btn, self._feedback])

        return widgets.VBox(children)

    def _get_state(self) -> dict[str, Any]:
        return {"responses": self.responses}

    def _set_state(self, state: dict[str, Any]) -> None:
        # Normalize keys to integers (JSON serializes dict keys as strings)
        raw_responses = state.get("responses", {})
        self.responses = {int(k): v for k, v in raw_responses.items()}
