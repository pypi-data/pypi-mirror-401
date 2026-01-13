"""
SBC Leaderboard - Discord-based score tracking and leaderboards.

Client library for submitting scores from Jupyter notebooks
to a Discord bot with slash commands.
"""

from .client import Leaderboard, submit_score, configure

__all__ = ["Leaderboard", "submit_score", "configure"]
