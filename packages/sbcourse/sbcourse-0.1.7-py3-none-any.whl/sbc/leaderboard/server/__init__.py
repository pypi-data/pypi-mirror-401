"""
SBC Leaderboard Server - Discord bot with Flask API.

Run with: sbc bot run
"""

from .bot import run_bot
from .database import init_db, add_score, get_leaderboard, get_student_stats, get_cohorts

__all__ = [
    "run_bot",
    "init_db",
    "add_score",
    "get_leaderboard",
    "get_student_stats",
    "get_cohorts",
]
