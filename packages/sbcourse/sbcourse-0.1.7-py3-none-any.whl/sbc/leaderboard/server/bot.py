"""
Discord bot with slash commands for the leaderboard.

Run with: sbc bot run
"""

import os
import asyncio
import threading
from datetime import datetime, timedelta
from typing import Optional

try:
    import discord
    from discord import app_commands
    from flask import Flask, request, jsonify
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

from .database import init_db, add_score, get_leaderboard, get_student_stats, get_cohorts


def run_bot(
    token: Optional[str] = None,
    api_port: int = 5000,
    api_secret: str = "change-me",
    db_path: str = "leaderboard.db",
) -> None:
    """
    Run the Discord bot with Flask API.

    Args:
        token: Discord bot token (or DISCORD_TOKEN env var)
        api_port: Port for HTTP API
        api_secret: Secret for API authentication
        db_path: Path to SQLite database
    """
    if not DISCORD_AVAILABLE:
        print("Error: discord.py and flask are required.")
        print("Install with: pip install sbc[bot]")
        return

    token = token or os.environ.get("DISCORD_TOKEN")
    if not token:
        print("Error: DISCORD_TOKEN environment variable not set")
        print("Create a bot at https://discord.com/developers/applications")
        return

    api_secret = os.environ.get("API_SECRET", api_secret)

    # Initialize database
    init_db(db_path)

    # Create bot
    intents = discord.Intents.default()
    bot = discord.Client(intents=intents)
    tree = app_commands.CommandTree(bot)

    # Activity icons
    ICONS = {
        "trivia": "🎯",
        "flashcards": "📚",
        "puzzles": "🧩",
        "quiz": "📝",
        "reflection": "💭",
    }

    @bot.event
    async def on_ready():
        await tree.sync()
        print(f"Bot ready! Logged in as {bot.user}")
        print(f"Invite: https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=2147483648&scope=bot%20applications.commands")

    @tree.command(name="leaderboard", description="Show the leaderboard")
    @app_commands.describe(
        metric="Ranking metric",
        cohort="Class/semester filter"
    )
    @app_commands.choices(metric=[
        app_commands.Choice(name="Total Points", value="total"),
        app_commands.Choice(name="This Week", value="weekly"),
        app_commands.Choice(name="Points/Day", value="daily_avg"),
    ])
    async def leaderboard_cmd(
        interaction: discord.Interaction,
        metric: str = "total",
        cohort: str = None,
    ):
        data = get_leaderboard(db_path, limit=10, cohort=cohort, metric=metric)

        if not data:
            await interaction.response.send_message("No scores yet!")
            return

        medals = ["🥇", "🥈", "🥉"]
        lines = []

        for i, entry in enumerate(data):
            name = entry.get("display_name") or entry.get("student_id")
            score = entry.get("score", 0)

            if metric == "daily_avg":
                score_text = f"{score:.1f} pts/day"
            else:
                score_text = f"{score:,} pts"

            if i < 3:
                lines.append(f"{medals[i]} **{name}** — {score_text}")
            else:
                lines.append(f"`{i+1}.` {name} — {score_text}")

        embed = discord.Embed(
            title="🏆 Leaderboard",
            description="\n".join(lines),
            color=0xFFD700
        )

        footer = f"Metric: {metric}"
        if cohort:
            footer += f" | Cohort: {cohort}"
        embed.set_footer(text=footer)

        await interaction.response.send_message(embed=embed)

    @tree.command(name="mystats", description="View your stats")
    async def mystats(interaction: discord.Interaction):
        student_id = interaction.user.name
        stats = get_student_stats(db_path, student_id)

        if stats.get("total", 0) == 0:
            await interaction.response.send_message(
                f"No scores found for **{student_id}**",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"📊 Stats for {student_id}",
            color=0x5865F2
        )
        embed.add_field(
            name="🏆 Total",
            value=f"**{stats['total']:,}** pts",
            inline=True
        )
        embed.add_field(
            name="📅 This Week",
            value=f"**{stats['weekly']:,}** pts",
            inline=True
        )
        embed.add_field(
            name="📈 Daily Avg",
            value=f"**{stats['daily_avg']}** pts/day",
            inline=True
        )
        embed.set_footer(text=f"Cohort: {stats.get('cohort', 'default')} | Days active: {stats.get('days_active', 0)}")

        await interaction.response.send_message(embed=embed)

    @tree.command(name="cohorts", description="List all cohorts")
    async def cohorts_cmd(interaction: discord.Interaction):
        cohort_list = get_cohorts(db_path)
        embed = discord.Embed(
            title="📚 Cohorts",
            description="\n".join([f"• `{c}`" for c in cohort_list]),
            color=0x9B59B6
        )
        await interaction.response.send_message(embed=embed)

    # Flask API
    api = Flask(__name__)

    @api.route("/health", methods=["GET"])
    def health():
        return jsonify({"status": "ok", "cohorts": get_cohorts(db_path)})

    @api.route("/submit", methods=["POST"])
    def submit():
        data = request.json

        if data.get("secret") != api_secret:
            return jsonify({"error": "Invalid secret"}), 401

        student_id = data.get("student_id")
        activity = data.get("activity")
        score = data.get("score")

        if not all([student_id, activity, score]):
            return jsonify({"error": "Missing fields"}), 400

        add_score(
            db_path=db_path,
            student_id=student_id,
            display_name=data.get("display_name"),
            activity=activity,
            score=score,
            cohort=data.get("cohort", "default"),
            details=data.get("details"),
            session_hash=data.get("session_hash"),
        )

        stats = get_student_stats(db_path, student_id)
        return jsonify({
            "success": True,
            "total": stats.get("total", 0),
            "daily_avg": stats.get("daily_avg", 0),
        })

    @api.route("/leaderboard", methods=["GET"])
    def leaderboard_api():
        limit = request.args.get("limit", 10, type=int)
        metric = request.args.get("metric", "total")
        cohort = request.args.get("cohort")

        entries = get_leaderboard(db_path, limit=limit, cohort=cohort, metric=metric)
        return jsonify({"entries": entries, "metric": metric})

    def run_api():
        api.run(host="0.0.0.0", port=api_port, debug=False, use_reloader=False)

    # Start API in background
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    print(f"API running on port {api_port}")

    # Run bot
    print("Starting Discord bot...")
    bot.run(token)
