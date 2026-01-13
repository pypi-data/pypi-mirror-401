"""
SBC - Steel Bank Course

A comprehensive toolkit for managing Jupyter notebook-based courses with:
- Interactive widgets (quizzes, flashcards, trivia, reflections, puzzles)
- Persistent state management
- Discord-based leaderboards and gamification
- Assignment generation and distribution
- PDF export with notebook attachment
- Semantic search across course materials

Usage:
    # In Jupyter notebooks
    %load_ext sbc

    # Available magic commands
    %quiz week-01           - Load and display a quiz
    %trivia calculus        - Start a trivia game
    %flashcards derivatives - Study flashcards
    %leaderboard            - Show leaderboard
    %%reflection week-01    - Create a reflection prompt
    %pdf                    - Export notebook to PDF

    # CLI commands
    sbc assign <directory>  - Generate student assignment
    sbc new <name>          - Create new course from template
    sbc bot run             - Run Discord leaderboard bot
"""

__version__ = "0.1.1"


def main() -> None:
    print("Hello from sbc!")


# Import magic commands (registers them automatically)
try:
    from .magic import *
except Exception:
    pass

# Import PDF export magic
try:
    from .pdf import *
except Exception:
    pass

# Import search functionality
try:
    from .search import *
except Exception:
    pass

# Export key classes for programmatic use
try:
    from .widgets import Quiz, Trivia, Flashcards, Reflection, Puzzles, BaseWidget
except ImportError:
    pass

try:
    from .persistence import Storage
except ImportError:
    pass

try:
    from .leaderboard import Leaderboard, configure, submit_score
except ImportError:
    pass


# IPython extension loading
def load_ipython_extension(ipython):
    """Load the SBC IPython extension.

    Usage:
        %load_ext sbc
    """
    # Magic commands are automatically registered on import
    print("SBC extension loaded. Available magics: %quiz, %trivia, %flashcards, %leaderboard, %%reflection, %pdf")


def unload_ipython_extension(ipython):
    """Unload the SBC IPython extension."""
    pass
