#!/usr/bin/env python
'''Utility script for sbc
sbc is Steel Bank Course.

The idea here is you have a separate repository of assignments.
Each assignment is in a directory. You assign a directory like this:

> sbc assign path-to-assignment-directory

That will remove any Solution / Hidden information in the notebooks and add it to the course repo.

Additional commands:
- sbc bot run: Run the Discord leaderboard bot
- sbc bot init-db: Initialize the leaderboard database
- sbc bot export: Export scores to CSV
- sbc new <name>: Create a new course from template
'''

from fnmatch import fnmatch
import glob
import json
import os
import csv
import click
import shutil
from pathlib import Path

from nbconvert.exporters import NotebookExporter
from nbconvert.writers import FilesWriter
import nbformat
from traitlets.config import Config
from .preprocessors import RemoveSolutionPreprocessor, HiddenPreprocessor
from nbconvert.preprocessors import ClearOutputPreprocessor
from .config import config, save_config_template, reload_config

@click.group()
def cli():
    """Group command for sbc."""
    pass

def ignore_file(f, ignore_rxs):
    'Return True if F matches any patterns in IGNORE_RXS.'
    for rx in ignore_rxs:
        if fnmatch(f, rx):
            return True
    return False


def generate_ipynb(path, dest):
    '''Generate student version of path.
    Strips solution and hidden fences from the ipynb.
    '''

    c = Config()
    c.NotebookExporter.preprocessors = [RemoveSolutionPreprocessor, HiddenPreprocessor, ClearOutputPreprocessor]

    nbe = NotebookExporter(config=c)
    (content, resources) = nbe.from_filename(path)
    j = json.loads(content)

    content = json.dumps(j)

    nbw = FilesWriter()

    # strip extension from dest for writing out, or you get dest.ipynb.ipynb
    nbw.write(content, resources, os.path.splitext(dest)[0])
    print(f'    Wrote to {dest}')


@cli.command()
@click.argument('directory')
@click.option('--push', is_flag=True)
def assign(directory, push=False):
    '''Directory contains the files to assign
    '''
    DEST = os.path.expanduser(config.paths.dest_root)

    base_dir = Path(directory).absolute().name
    print(f'basedir: {base_dir}')
    cwd = os.getcwd()

    os.chdir(directory)

    files = glob.glob('**')
    print(f'    Found {files} in {directory}')

    ignore_rxs = []
    if os.path.exists('.ignore'):
        with open('.ignore') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    ignore_rxs += [line.strip()]

    for file in files:
        if ignore_file(file, ignore_rxs):
            print(f'    Ignoring {file}')
            continue

        elif file.endswith('.ipynb'):
            dest = Path(DEST) / base_dir
            os.makedirs(dest, exist_ok=True)
            generate_ipynb(file, dest / file)

        # Another kind of file, we just copy it
        else:
            dest = Path(DEST) / base_dir
            os.makedirs(dest, exist_ok=True)
            print(f'    Copying {file} to {dest}')
            shutil.copyfile(file, dest / file)


    if push:
        print('Pushing!')
        os.chdir(DEST)
        for file in glob.glob(f'{base_dir}/**'):
            os.system(f'git add {file}')
            os.system(f'git commit {file} -m "Adding {file}"')
        os.system('git push')

        # Build URL using config
        course_name = config.course.name
        github_repo = f'{config.course.github_org}/{config.course.github_repo}'
        path = f'{course_name}/{course_name}/assignments/{base_dir}/{base_dir}.ipynb'
        jh = f'{config.jupyterhub.base_url}/hub/user-redirect/git-pull?repo=https%3A//{github_repo}&urlpath=lab/tree/{path}&branch={config.course.github_branch}'
        print()
        print(jh)


@cli.command()
@click.argument('directory')
def push(directory):
    """Push assignment directory to git."""
    base_dir = Path(directory).absolute().name


@cli.group()
def cfg():
    """Configuration management commands."""
    pass


@cfg.command('init')
@click.option('--project', is_flag=True, help='Create config in current directory (.sbc.toml)')
@click.option('--user', is_flag=True, help='Create config in user directory (~/.config/sbc/config.toml)')
def config_init(project, user):
    """Generate a configuration template file."""
    if project:
        path = Path.cwd() / '.sbc.toml'
        scope = 'project'
    elif user:
        path = Path.home() / '.config' / 'sbc' / 'config.toml'
        scope = 'user'
    else:
        path = Path.home() / '.sbc.toml'
        scope = 'home'

    if path.exists():
        click.confirm(f'Configuration file already exists at {path}. Overwrite?', abort=True)

    save_config_template(path)
    click.echo(f'Created {scope} configuration file at: {path}')
    click.echo('\nEdit this file to customize your settings.')


@cfg.command('show')
@click.option('--raw', is_flag=True, help='Show raw dictionary instead of formatted output')
def config_show(raw):
    """Show current configuration."""
    if raw:
        import pprint
        pprint.pprint(config.to_dict())
    else:
        click.echo('Current SBC Configuration:')
        click.echo('=' * 50)
        click.echo('\n[JupyterHub]')
        click.echo(f'  Base URL: {config.jupyterhub.base_url}')
        click.echo(f'  Dev URL:  {config.jupyterhub.dev_url}')
        click.echo('\n[Course]')
        click.echo(f'  Name:         {config.course.name}')
        click.echo(f'  Semester:     {config.course.semester}')
        click.echo(f'  Course #:     {config.course.course_number}')
        click.echo(f'  GitHub Org:   {config.course.github_org}')
        click.echo(f'  GitHub Repo:  {config.course.github_repo}')
        click.echo(f'  Branch:       {config.course.github_branch}')
        click.echo('\n[Paths]')
        click.echo(f'  Source Root:    {config.paths.source_root}')
        click.echo(f'  Dest Root:      {config.paths.dest_root}')
        click.echo(f'  Notebook Root:  {config.paths.notebook_root}')
        click.echo(f'  Search DB:      {config.paths.search_db}')
        click.echo(f'  Collection:     {config.paths.search_collection}')
        click.echo('\n[Search]')
        click.echo(f'  Include Pattern:  {config.search.include_pattern}')
        click.echo(f'  Exclude Patterns: {config.search.exclude_patterns}')


@cfg.command('reload')
def config_reload():
    """Reload configuration from files."""
    reload_config()
    click.echo('Configuration reloaded successfully.')


# =============================================================================
# Bot Commands (Leaderboard)
# =============================================================================

@cli.group()
def bot():
    """Leaderboard bot commands."""
    pass


@bot.command('run')
@click.option('--port', type=int, default=5000, help='API port')
@click.option('--db', default='leaderboard.db', help='Database path')
@click.option('--token', help='Discord token (or use DISCORD_TOKEN env)')
@click.option('--secret', help='API secret (or use API_SECRET env)')
def bot_run(port, db, token, secret):
    """Run the Discord bot with Flask API."""
    try:
        from .leaderboard.server import run_bot
        run_bot(
            token=token,
            api_port=port,
            api_secret=secret or os.environ.get("API_SECRET", "change-me"),
            db_path=db,
        )
    except ImportError as e:
        click.echo(f"Error: {e}")
        click.echo("Install bot dependencies with: pip install sbc[bot]")


@bot.command('init-db')
@click.option('--db', default='leaderboard.db', help='Database path')
def bot_init_db(db):
    """Initialize the leaderboard database."""
    try:
        from .leaderboard.server import init_db
        init_db(db)
        click.echo(f"Database initialized: {db}")
    except ImportError as e:
        click.echo(f"Error: {e}")


@bot.command('export')
@click.option('--output', '-o', default='scores.csv', help='Output file')
@click.option('--cohort', help='Filter by cohort')
@click.option('--db', default='leaderboard.db', help='Database path')
def bot_export(output, cohort, db):
    """Export scores to CSV."""
    import sqlite3

    if not os.path.exists(db):
        click.echo(f"Database not found: {db}")
        return

    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    query = "SELECT student_id, display_name, cohort, activity, score, timestamp FROM scores"
    params = []

    if cohort:
        query += " WHERE cohort = ?"
        params.append(cohort)

    query += " ORDER BY timestamp DESC"

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    with open(output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["student_id", "display_name", "cohort", "activity", "score", "timestamp"])
        writer.writerows(rows)

    click.echo(f"Exported {len(rows)} scores to {output}")


# =============================================================================
# New Course Command
# =============================================================================

@cli.command('new')
@click.argument('name')
@click.option('--template', default='basic', help='Template to use')
def new_course(name, template):
    """Create a new course from template."""
    target = Path(name)

    if target.exists():
        click.echo(f"Error: Directory already exists: {name}")
        return

    # Create basic structure
    target.mkdir(parents=True)
    (target / "lectures").mkdir()
    (target / "assignments").mkdir()
    (target / "quizzes").mkdir()
    (target / "flashcards").mkdir()
    (target / "games").mkdir()
    (target / ".sbc").mkdir()

    # Create pyproject.toml
    pyproject = f'''[project]
name = "{name}"
version = "0.1.0"
dependencies = ["sbc"]

[tool.sbc]
cohort = "{name}"
'''
    (target / "pyproject.toml").write_text(pyproject)

    # Create sample quiz
    sample_quiz = '''title: Sample Quiz
questions:
  - question: What is 2 + 2?
    options:
      - "3"
      - "4"
      - "5"
    answer: 1
    explanation: Basic arithmetic!
'''
    (target / "quizzes" / "sample.yaml").write_text(sample_quiz)

    # Create sample flashcard deck
    sample_flashcards = '''title: Sample Flashcards
cards:
  - front: What is the derivative of x^2?
    back: 2x
  - front: What is the integral of 1/x?
    back: ln|x| + C
'''
    (target / "flashcards" / "sample.yaml").write_text(sample_flashcards)

    # Create intro notebook
    intro_nb = '''{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": ["# Welcome to the Course\\n", "\\n", "Run the cell below to get started."]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": ["%load_ext sbc\\n", "%quiz sample"]
  }
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}
 },
 "nbformat": 4,
 "nbformat_minor": 4
}'''
    (target / "lectures" / "01-intro.ipynb").write_text(intro_nb)

    click.echo(f"Created course: {name}/")
    click.echo(f"  lectures/01-intro.ipynb")
    click.echo(f"  quizzes/sample.yaml")
    click.echo(f"  flashcards/sample.yaml")
    click.echo(f"  pyproject.toml")
    click.echo()
    click.echo("Next steps:")
    click.echo(f"  cd {name}")
    click.echo("  pip install sbc")
    click.echo("  jupyter lab")


if __name__ == "__main__":
    cli()
