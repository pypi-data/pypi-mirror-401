"""
SQLite database operations for the leaderboard.

This module provides safe database operations with:
- Context managers for automatic connection cleanup
- Parameterized queries to prevent SQL injection
- Proper error handling and rollback on failures
"""

import sqlite3
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Any, Generator, Optional


@contextmanager
def get_connection(db_path: str = "leaderboard.db") -> Generator[sqlite3.Connection, None, None]:
    """
    Get database connection as a context manager.

    Automatically commits on success, rolls back on failure,
    and closes the connection when done.

    Usage:
        with get_connection(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(...)
    """
    conn = sqlite3.connect(db_path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db(db_path: str = "leaderboard.db") -> None:
    """Initialize the database schema."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        # Scores table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id TEXT NOT NULL,
                display_name TEXT,
                cohort TEXT DEFAULT 'default',
                activity TEXT NOT NULL,
                score INTEGER NOT NULL,
                details TEXT,
                session_hash TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Students table for join date tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                display_name TEXT,
                cohort TEXT DEFAULT 'default',
                joined_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                discord_id TEXT
            )
        """)

        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_student ON scores(student_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cohort ON scores(cohort)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON scores(timestamp)")


def add_score(
    db_path: str,
    student_id: str,
    display_name: str,
    activity: str,
    score: int,
    cohort: str = "default",
    details: Optional[str] = None,
    session_hash: Optional[str] = None,
) -> None:
    """Add a score to the database."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        # Ensure student exists
        cursor.execute(
            "INSERT OR IGNORE INTO students (student_id, display_name, cohort) VALUES (?, ?, ?)",
            (student_id, display_name, cohort)
        )

        # Add score
        cursor.execute(
            """
            INSERT INTO scores (student_id, display_name, cohort, activity, score, details, session_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (student_id, display_name, cohort, activity, score, details, session_hash)
        )


def _build_query(
    base_query: str,
    conditions: list[str],
    order_by: Optional[str] = None,
    limit: Optional[int] = None,
) -> str:
    """
    Build a SQL query string safely.

    All conditions should use ? placeholders for parameters.
    This function only builds the query structure, not the values.
    """
    query = base_query

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if order_by:
        query += f" ORDER BY {order_by}"

    if limit is not None:
        query += " LIMIT ?"

    return query


def get_leaderboard(
    db_path: str,
    limit: int = 10,
    cohort: Optional[str] = None,
    metric: str = "total",
    since: Optional[datetime] = None,
) -> list[dict[str, Any]]:
    """
    Get leaderboard entries.

    Args:
        db_path: Path to the database file
        limit: Maximum number of entries to return
        cohort: Filter by cohort (optional)
        metric: Ranking metric - "total", "weekly", or "daily_avg"
        since: Filter scores since this datetime (optional)

    Returns:
        List of dicts with student_id, display_name, and score
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        params: list[Any] = []

        if metric == "daily_avg":
            # Build conditions
            conditions = ["1=1"]  # Base condition for easier appending
            if cohort:
                conditions.append("s.cohort = ?")
                params.append(cohort)

            query = f"""
                SELECT
                    s.student_id,
                    s.display_name,
                    SUM(s.score) as total,
                    CAST(SUM(s.score) AS FLOAT) /
                        MAX(1, julianday('now') - julianday(st.joined_at)) as daily_avg
                FROM scores s
                LEFT JOIN students st ON s.student_id = st.student_id
                WHERE {" AND ".join(conditions)}
                GROUP BY s.student_id
                ORDER BY daily_avg DESC
                LIMIT ?
            """
            params.append(limit)

            cursor.execute(query, params)

            return [
                {
                    "student_id": row[0],
                    "display_name": row[1],
                    "total": row[2],
                    "score": row[3],  # daily_avg as score for display
                }
                for row in cursor.fetchall()
            ]

        elif metric == "weekly" or since:
            if not since:
                since = datetime.now() - timedelta(days=7)

            conditions = ["timestamp >= ?"]
            params.append(since.isoformat())

            if cohort:
                conditions.append("cohort = ?")
                params.append(cohort)

            query = f"""
                SELECT student_id, display_name, SUM(score) as total
                FROM scores
                WHERE {" AND ".join(conditions)}
                GROUP BY student_id
                ORDER BY total DESC
                LIMIT ?
            """
            params.append(limit)

            cursor.execute(query, params)

            return [
                {"student_id": r[0], "display_name": r[1], "score": r[2]}
                for r in cursor.fetchall()
            ]

        else:
            # Total metric (default)
            conditions = ["1=1"]
            if cohort:
                conditions.append("cohort = ?")
                params.append(cohort)

            query = f"""
                SELECT student_id, display_name, SUM(score) as total
                FROM scores
                WHERE {" AND ".join(conditions)}
                GROUP BY student_id
                ORDER BY total DESC
                LIMIT ?
            """
            params.append(limit)

            cursor.execute(query, params)

            return [
                {"student_id": r[0], "display_name": r[1], "score": r[2]}
                for r in cursor.fetchall()
            ]


def get_student_stats(db_path: str, student_id: str, cohort: Optional[str] = None) -> dict[str, Any]:
    """
    Get stats for a specific student.

    Args:
        db_path: Path to the database file
        student_id: The student's identifier
        cohort: Filter by cohort (optional, defaults to student's cohort)

    Returns:
        Dict with total, weekly, daily_avg, days_active, cohort, joined_at
    """
    with get_connection(db_path) as conn:
        cursor = conn.cursor()

        # Get student info
        cursor.execute(
            "SELECT cohort, joined_at FROM students WHERE student_id = ?",
            (student_id,)
        )
        info = cursor.fetchone()

        if not info:
            return {"total": 0}

        student_cohort = info[0]
        joined_at = datetime.fromisoformat(info[1]) if info[1] else datetime.now()

        # Use provided cohort or student's cohort
        effective_cohort = cohort or student_cohort

        # Build total query
        if effective_cohort:
            cursor.execute(
                "SELECT SUM(score) FROM scores WHERE student_id = ? AND cohort = ?",
                (student_id, effective_cohort)
            )
        else:
            cursor.execute(
                "SELECT SUM(score) FROM scores WHERE student_id = ?",
                (student_id,)
            )
        total = cursor.fetchone()[0] or 0

        # Build weekly query
        week_ago = datetime.now() - timedelta(days=7)
        if effective_cohort:
            cursor.execute(
                "SELECT SUM(score) FROM scores WHERE student_id = ? AND timestamp >= ? AND cohort = ?",
                (student_id, week_ago.isoformat(), effective_cohort)
            )
        else:
            cursor.execute(
                "SELECT SUM(score) FROM scores WHERE student_id = ? AND timestamp >= ?",
                (student_id, week_ago.isoformat())
            )
        weekly = cursor.fetchone()[0] or 0

        # Calculate days active
        days = max(1, (datetime.now() - joined_at).days)
        daily_avg = round(total / days, 1)

        return {
            "total": total,
            "weekly": weekly,
            "daily_avg": daily_avg,
            "days_active": days,
            "cohort": effective_cohort,
            "joined_at": joined_at.strftime("%Y-%m-%d"),
        }


def get_cohorts(db_path: str) -> list[str]:
    """Get list of all cohorts."""
    with get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT cohort FROM scores ORDER BY cohort")
        results = [row[0] for row in cursor.fetchall()]
        return results if results else ["default"]
