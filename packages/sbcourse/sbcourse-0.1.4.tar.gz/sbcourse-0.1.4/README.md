# SBC - Steel Bank Course

A comprehensive Python toolkit for managing Jupyter notebook-based courses with interactive widgets, persistent state, leaderboards, and gamification.

## Features

### For Students
- **Interactive Widgets** - Quizzes, flashcards, trivia games, code puzzles, and reflections
- **State Persistence** - Automatically resume activities where you left off
- **Gamification** - Streaks, points, and leaderboard competition
- **PDF Export** - Export notebooks to PDF with source attachment

### For Instructors
- **YAML-based Content** - Define quizzes, flashcards, and challenges in simple YAML
- **Assignment Distribution** - Strip solutions and generate student versions
- **Score Tracking** - Discord-based leaderboards with multiple metrics
- **Course Templates** - Quickly scaffold new course structures

## Installation

```bash
pip install sbcourse

# For Discord bot functionality
pip install sbcourse[bot]
```

## Quick Start

### In Jupyter Notebooks

```python
# Load the extension
%load_ext sbc

# Run a quiz
%quiz week-01

# Play trivia
%trivia calculus -n 5

# Study flashcards
%flashcards derivatives

# Write a reflection
%%reflection week-01
What did you learn about derivatives this week?

# Export to PDF (with .ipynb attached)
%pdf
```

### Command Line

```bash
# Create a new course
sbc new my-course

# Generate student assignment (strips solutions)
sbc assign assignment-01 --push

# Show configuration
sbc cfg show

# Run Discord leaderboard bot
sbc bot run
```

## Magic Commands

| Command | Description |
|---------|-------------|
| `%quiz <name>` | Load and display an interactive quiz |
| `%trivia [topic] [-n NUM]` | Start a trivia game |
| `%flashcards <deck>` | Load flashcard deck for study |
| `%leaderboard [--weekly] [--fair]` | Display course leaderboard |
| `%%reflection <name>` | Create reflection prompt (cell body is prompt) |
| `%pdf [filename]` | Export notebook to PDF |
| `%index [--rebuild]` | Build semantic search index |
| `%%search [-n NUM]` | Search course notebooks |
| `%assign <notebook>` | Generate student version |
| `%update <files>` | Commit and push files |

## Content Formats

### Quiz Format (YAML)

```yaml
title: Week 1 Quiz
questions:
  - question: What is the derivative of x^2?
    options:
      - "x"
      - "2x"
      - "x^2"
    answer: 1
    explanation: Power rule - bring down the exponent and subtract 1
```

### Flashcard Format (YAML)

```yaml
title: Calculus Fundamentals
cards:
  - front: What is the derivative of sin(x)?
    back: cos(x)
  - front: What is the integral of 1/x?
    back: ln|x| + C
```

## Leaderboard Setup

### 1. Configure Students

```python
from sbc.leaderboard import configure

configure(
    api_url="https://your-bot.fly.dev",
    api_secret="your-secret",
    student_id="jsmith",
    display_name="Jane Smith",
    cohort="F25-06623"
)
```

### 2. Run Discord Bot

```bash
export DISCORD_TOKEN="your-bot-token"
export API_SECRET="your-api-secret"
sbc bot run --port 5000
```

### 3. Discord Commands

- `/leaderboard [metric] [cohort]` - Display standings
- `/mystats` - View your personal statistics
- `/cohorts` - List all cohorts

## Project Structure

```
sbc/
├── src/sbc/
│   ├── widgets/           # Interactive Jupyter widgets
│   │   ├── quiz.py        # Multiple choice quizzes
│   │   ├── trivia.py      # Timed trivia games
│   │   ├── flashcards.py  # Spaced repetition cards
│   │   ├── reflection.py  # Free-form responses
│   │   └── puzzles.py     # Code challenges
│   ├── persistence/       # State management
│   ├── leaderboard/       # Score tracking
│   │   ├── client.py      # Notebook client
│   │   └── server/        # Discord bot + API
│   ├── magic.py           # IPython magic commands
│   ├── pdf.py             # PDF export
│   ├── search.py          # Semantic search
│   ├── cli.py             # Command-line interface
│   └── config.py          # Configuration system
└── pyproject.toml
```

## Configuration

SBC uses a hierarchical configuration system:

1. Default values (built-in)
2. `~/.sbc.toml` - User-level config
3. `.sbc.toml` - Project-level config
4. `SBC_*` environment variables

Generate a template:

```bash
sbc cfg init
```

## Assignment Generation

Mark solution code in notebooks:

```python
# Code cells
### BEGIN SOLUTION
answer = 42
### END SOLUTION
```

```markdown
<!-- Markdown cells -->
<!-- BEGIN SOLUTION -->
The answer is 42.
<!-- END SOLUTION -->
```

Generate student version:

```bash
sbc assign assignment-01 --push
```

## PDF Export Options

```python
%pdf                  # Default: attach .ipynb, add header
%pdf report.pdf       # Custom filename
%pdf --no-attach      # Don't attach source notebook
%pdf --no-header      # Skip timestamp header
%pdf --no-save        # Don't auto-save before export
%pdf -v               # Verbose output
```

## Semantic Search

Search across all course notebooks using ChromaDB for semantic similarity.

```python
# Build the search index (one time)
%index

# Force rebuild the index
%index --rebuild

# Search for related content
%%search -n 5
What is a Gaussian process?
```

The search returns links to relevant notebook cells (markdown and code) ranked by semantic similarity to your query.

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"
# or with uv
uv pip install -e ".[dev]"

# Run tests
pytest

# Lint code
ruff check src/
```

## License

MIT License - see LICENSE file for details.

## Author

John Kitchin (jkitchin@andrew.cmu.edu)
