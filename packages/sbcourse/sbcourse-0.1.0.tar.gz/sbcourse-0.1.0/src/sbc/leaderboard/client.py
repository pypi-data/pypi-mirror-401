"""
Leaderboard client for submitting scores from Jupyter notebooks.

Configuration is stored in ~/.sbc/leaderboard.json
"""

import hashlib
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import requests


def _get_config_path() -> Path:
    """Get path to leaderboard config file."""
    return Path.home() / ".sbc" / "leaderboard.json"


def _load_config() -> dict[str, Any]:
    """Load configuration from file."""
    config_path = _get_config_path()
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return {}


def _save_config(config: dict[str, Any]) -> None:
    """Save configuration to file."""
    config_path = _get_config_path()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def configure(
    api_url: str = None,
    api_secret: str = None,
    student_id: str = None,
    display_name: str = None,
    cohort: str = None,
) -> None:
    """
    Configure leaderboard settings.

    Args:
        api_url: URL of the leaderboard API
        api_secret: API secret for authentication
        student_id: Your student ID
        display_name: Your display name on leaderboard
        cohort: Class/semester identifier

    Example:
        from sbc.leaderboard import configure

        configure(
            api_url="https://my-bot.fly.dev",
            api_secret="secret123",
            student_id="jsmith",
            display_name="Jane Smith",
            cohort="F25-06623"
        )
    """
    config = _load_config()

    if api_url is not None:
        config["api_url"] = api_url.rstrip("/")
    if api_secret is not None:
        config["api_secret"] = api_secret
    if student_id is not None:
        config["student_id"] = student_id
    if display_name is not None:
        config["display_name"] = display_name
    if cohort is not None:
        config["cohort"] = cohort

    _save_config(config)
    print("Leaderboard configuration saved!")


def submit_score(
    activity: str,
    score: int,
    details: str = None,
    session_data: dict = None,
) -> Optional[dict]:
    """
    Submit a score to the leaderboard.

    Args:
        activity: Activity identifier (e.g., "quiz:week-01", "trivia:calculus")
        score: Points earned
        details: Optional description
        session_data: Optional session data for verification hash

    Returns:
        Response dict with rank and total, or None if not configured
    """
    config = _load_config()

    api_url = config.get("api_url")
    if not api_url:
        return None  # Not configured, silently skip

    # Generate session hash for basic verification
    session_hash = None
    if session_data:
        hash_input = json.dumps(session_data, sort_keys=True) + datetime.now().isoformat()
        session_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    payload = {
        "secret": config.get("api_secret", ""),
        "student_id": config.get("student_id", os.environ.get("USER", "anonymous")),
        "display_name": config.get("display_name"),
        "cohort": config.get("cohort", "default"),
        "activity": activity,
        "score": score,
        "details": details,
        "session_hash": session_hash,
    }

    try:
        response = requests.post(
            f"{api_url}/submit",
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            import warnings
            warnings.warn("Leaderboard API authentication failed. Check your api_secret.")
        # Other status codes are silently ignored (server may be temporarily unavailable)
    except requests.exceptions.Timeout:
        # Timeout is acceptable - don't block the user
        pass
    except requests.exceptions.ConnectionError:
        # Network issue - acceptable to skip silently
        pass
    except requests.exceptions.RequestException as e:
        # Other request errors - warn but don't crash
        import warnings
        warnings.warn(f"Failed to submit score: {e}")

    return None


class Leaderboard:
    """
    Leaderboard client with instance-based configuration.

    Example:
        lb = Leaderboard()
        lb.configure(api_url="...", student_id="...")
        lb.submit("quiz:week-01", 100)
        lb.show()
    """

    def __init__(self):
        self._config = _load_config()

    def configure(self, **kwargs: Any) -> None:
        """Configure this leaderboard instance."""
        configure(**kwargs)
        self._config = _load_config()

    def submit(
        self,
        activity: str,
        score: int,
        details: str = None,
        session_data: dict = None,
    ) -> Optional[dict]:
        """Submit a score."""
        return submit_score(activity, score, details, session_data)

    def show(
        self,
        limit: int = 10,
        metric: str = "total",
        cohort: str = None,
    ) -> None:
        """
        Display the leaderboard.

        Args:
            limit: Number of entries to show
            metric: Ranking metric (total, weekly, daily_avg)
            cohort: Filter by cohort
        """
        from IPython.display import display, HTML

        api_url = self._config.get("api_url")
        if not api_url:
            print("Leaderboard not configured. Run: from sbc.leaderboard import configure")
            return

        try:
            response = requests.get(
                f"{api_url}/leaderboard",
                params={
                    "limit": limit,
                    "metric": metric,
                    "cohort": cohort or self._config.get("cohort"),
                },
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                self._display_leaderboard(data, metric)
            elif response.status_code == 401:
                print("Error: Authentication failed. Check your leaderboard configuration.")
            else:
                print(f"Error fetching leaderboard: HTTP {response.status_code}")
        except requests.exceptions.Timeout:
            print("Error: Request timed out. The leaderboard server may be slow or unavailable.")
        except requests.exceptions.ConnectionError:
            print("Error: Could not connect to leaderboard server. Check your internet connection.")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching leaderboard: {e}")

    def _display_leaderboard(self, data: dict[str, Any], metric: str) -> None:
        """Display leaderboard as HTML."""
        from IPython.display import display, HTML

        entries = data.get("entries", [])
        if not entries:
            display(HTML("<p><em>No scores yet!</em></p>"))
            return

        medals = ["🥇", "🥈", "🥉"]
        rows = []

        for i, entry in enumerate(entries):
            medal = medals[i] if i < 3 else f"{i+1}."
            name = entry.get("display_name") or entry.get("student_id")
            score = entry.get("score", 0)

            if metric == "daily_avg":
                score_text = f"{score:.1f} pts/day"
            else:
                score_text = f"{score:,} pts"

            rows.append(f"<tr><td>{medal}</td><td>{name}</td><td>{score_text}</td></tr>")

        html = f"""
        <table style='width: 100%; border-collapse: collapse;'>
            <thead>
                <tr style='background: #f0f0f0;'>
                    <th style='padding: 8px; text-align: left;'>Rank</th>
                    <th style='padding: 8px; text-align: left;'>Name</th>
                    <th style='padding: 8px; text-align: left;'>Score</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows)}
            </tbody>
        </table>
        """
        display(HTML(html))

    def status(self) -> None:
        """Show configuration status."""
        from IPython.display import display, Markdown

        config = self._config
        api_url = config.get("api_url", "Not configured")
        student_id = config.get("student_id", "Not set")
        cohort = config.get("cohort", "default")

        display(Markdown(f"""
**Leaderboard Status**
- API URL: `{api_url}`
- Student ID: `{student_id}`
- Cohort: `{cohort}`
        """))
