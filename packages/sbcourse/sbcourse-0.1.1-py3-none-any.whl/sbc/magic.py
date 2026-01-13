"""Magic commands for sbc.

The idea is you run magic commands from a console which has rich, clickable output.

import this in ~/.ipython/profile_default/startup/00-first.py

Available magics:
- %assign: Convert notebook to student version and push
- %update: Add, commit and push files
- %quiz: Load and display an interactive quiz
- %trivia: Start an interactive trivia game
- %flashcards: Load and display flashcards
- %leaderboard: Display the course leaderboard
- %%reflection: Create an interactive reflection prompt
"""

import argparse
import json
import os
import pathlib
import shlex
from pathlib import Path
from typing import Optional

from IPython.core.magic import register_line_magic, register_cell_magic
from IPython.display import display, Markdown, HTML
from .config import config


@register_line_magic
def assign(line: str) -> None:
    """Convert the source notebook to student version."""
    notebooks = line.split()
    
    for notebook in notebooks:
        with open(notebook) as f:
            ipynb = json.loads(f.read())

        for cell in ipynb['cells']:
            src = ''.join(cell['source'])
            if '# solution' in src:
                cell['outputs'] = []
                cell['source'] = ''

        label = pathlib.Path().cwd().name
        newfile = label + '.ipynb'
        if newfile == notebook:
            raise Exception('You need a source notebook. rename it.')

        with open(newfile, 'w') as nb:
            nb.write(json.dumps(ipynb))

        os.system(f'git add {newfile}')
        os.system(f'git commit {newfile} -m "adding {newfile}"')
        os.system('git push')

        # Build URL using config
        course_name = config.course.name
        github_repo = f'{config.course.github_org}/{config.course.github_repo}'
        path = f'{course_name}/{course_name}/assignments/{label}/{label}.ipynb'
        jh = f'{config.jupyterhub.base_url}/hub/user-redirect/git-pull?repo=https%3A//{github_repo}&urlpath=lab/tree/{path}&branch={config.course.github_branch}'
        display(jh)
        print(jh)


@register_line_magic
def update(line: str) -> None:
    """Add, commit and push the files in line."""
    files = line.split()
    for file in files:
        print(f'Adding {file}')
        os.system(f'git add {file}')
    os.system('git commit -m "committing {line}"')
    os.system('git push')


# =============================================================================
# Widget Magic Commands
# =============================================================================

from .utils import find_quiz_file as _find_quiz_file


@register_line_magic
def quiz(line: str = "") -> None:
    """
    Load and display an interactive quiz.

    Usage:
        %quiz week-01              - Load quizzes/week-01.yaml
        %quiz week-01 --hierarchical - Use expandable sections
        %quiz path/to/quiz.yaml    - Load from specific path

    Examples:
        %quiz week-01
        %quiz midterm --hierarchical
    """
    args = shlex.split(line)
    if not args:
        print("Usage: %quiz <name> [--hierarchical]")
        print("Example: %quiz week-01")
        return

    name = args[0]
    hierarchical = '--hierarchical' in args or '-h' in args

    # Try to find quiz file
    quiz_path = _find_quiz_file(name)
    if quiz_path is None:
        print(f"Quiz not found: {name}")
        print("Looked in: quizzes/, ./, and absolute path")
        return

    try:
        from .widgets import Quiz
        q = Quiz.from_yaml(str(quiz_path), hierarchical=hierarchical)
        q.display()
    except ImportError as e:
        print(f"Error: Quiz widget requires ipywidgets. Run: pip install ipywidgets")
        print(f"Details: {e}")
    except FileNotFoundError:
        print(f"Error: Quiz file not found: {quiz_path}")
    except ValueError as e:
        print(f"Error: Invalid quiz format: {e}")
    except Exception as e:
        print(f"Error loading quiz: {type(e).__name__}: {e}")


@register_line_magic
def trivia(line: str = "") -> None:
    """
    Start an interactive trivia game.

    Usage:
        %trivia                    - Random topic
        %trivia calculus           - Specific topic
        %trivia calculus -n 10     - 10 questions
        %trivia --difficulty hard  - Set difficulty

    Examples:
        %trivia
        %trivia "linear algebra" -n 5
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('topic', nargs='?', default=None)
    parser.add_argument('-n', '--num-questions', type=int, default=5)
    parser.add_argument('-d', '--difficulty', default='medium',
                       choices=['easy', 'medium', 'hard'])

    try:
        args = parser.parse_args(shlex.split(line))
    except SystemExit:
        return

    try:
        from .widgets import Trivia
        t = Trivia(
            topic=args.topic,
            num_questions=args.num_questions,
            difficulty=args.difficulty
        )
        t.display()
    except ImportError as e:
        print(f"Error: Trivia widget requires ipywidgets. Run: pip install ipywidgets")
        print(f"Details: {e}")
    except ValueError as e:
        print(f"Error: Invalid trivia configuration: {e}")
    except Exception as e:
        print(f"Error starting trivia: {type(e).__name__}: {e}")


@register_line_magic
def flashcards(line: str = "") -> None:
    """
    Load and display flashcards.

    Usage:
        %flashcards derivatives    - Load deck by name
        %flashcards path/deck.yaml - Load from file

    Examples:
        %flashcards week-01
        %flashcards "integration techniques"
    """
    args = shlex.split(line)
    if not args:
        print("Usage: %flashcards <deck-name>")
        print("Example: %flashcards derivatives")
        return

    deck_name = args[0]

    try:
        from .widgets import Flashcards
        fc = Flashcards.from_deck(deck_name)
        fc.display()
    except ImportError as e:
        print(f"Error: Flashcards widget requires ipywidgets. Run: pip install ipywidgets")
        print(f"Details: {e}")
    except FileNotFoundError:
        print(f"Error: Deck not found: {deck_name}")
        print("Looked in: flashcards/, games/flashcards/, and current directory")
    except ValueError as e:
        print(f"Error: Invalid flashcard format: {e}")
    except Exception as e:
        print(f"Error loading flashcards: {type(e).__name__}: {e}")


@register_line_magic
def leaderboard(line: str = "") -> None:
    """
    Display the course leaderboard.

    Usage:
        %leaderboard              - Show top 10
        %leaderboard --weekly     - This week only
        %leaderboard --fair       - Points per day (fair for late joiners)
        %leaderboard -n 20        - Show top 20

    Examples:
        %leaderboard
        %leaderboard --weekly -n 5
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-n', '--limit', type=int, default=10)
    parser.add_argument('--weekly', action='store_true')
    parser.add_argument('--fair', action='store_true')
    parser.add_argument('--cohort', default=None)

    try:
        args = parser.parse_args(shlex.split(line))
    except SystemExit:
        return

    try:
        from .leaderboard import Leaderboard
        lb = Leaderboard()

        metric = 'total'
        if args.weekly:
            metric = 'weekly'
        elif args.fair:
            metric = 'daily_avg'

        lb.show(limit=args.limit, metric=metric, cohort=args.cohort)
    except ImportError as e:
        print(f"Error: Leaderboard module not available.")
        print(f"Details: {e}")
    except Exception as e:
        print(f"Error showing leaderboard: {type(e).__name__}: {e}")


@register_cell_magic
def reflection(line: str = "", cell: str = "") -> None:
    """
    Create an interactive reflection prompt.

    The cell content becomes the reflection prompt.

    Usage:
        %%reflection week-01
        What did you learn about derivatives this week?
        How might you apply these concepts?

    Args:
        line: Reflection identifier (e.g., "week-01")
        cell: The reflection prompt text
    """
    args = shlex.split(line)
    name = args[0] if args else "reflection"

    if not cell.strip():
        print("Error: Reflection prompt cannot be empty.")
        print("Add your prompt text in the cell body.")
        return

    try:
        from .widgets import Reflection
        r = Reflection(name=name, prompt=cell.strip())
        r.display()
    except ImportError as e:
        print(f"Error: Reflection widget requires ipywidgets. Run: pip install ipywidgets")
        print(f"Details: {e}")
    except ValueError as e:
        print(f"Error: Invalid reflection configuration: {e}")
    except Exception as e:
        print(f"Error creating reflection: {type(e).__name__}: {e}")


