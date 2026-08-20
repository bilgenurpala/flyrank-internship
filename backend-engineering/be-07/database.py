import sqlite3
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("reports.db")


def connect():
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize():
    with connect() as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT NOT NULL,
                done INTEGER NOT NULL CHECK (done IN (0, 1))
            );
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                kind TEXT NOT NULL,
                status TEXT NOT NULL,
                payload TEXT NOT NULL,
                result TEXT,
                error TEXT,
                created_at TEXT NOT NULL,
                started_at TEXT,
                finished_at TEXT
            );
        """)
        count = connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO tasks (title, category, done) VALUES (?, ?, ?)",
                [
                    ("Write API contract", "backend", 1),
                    ("Add database tests", "backend", 1),
                    ("Record demo", "portfolio", 0),
                    ("Audit mobile layout", "portfolio", 1),
                    ("Review eval report", "agent", 0),
                ],
            )


def aggregate_tasks():
    with connect() as connection:
        rows = connection.execute("""
            SELECT
                category,
                COUNT(*) AS total,
                SUM(CASE WHEN done = 1 THEN 1 ELSE 0 END) AS completed,
                SUM(CASE WHEN done = 0 THEN 1 ELSE 0 END) AS open
            FROM tasks
            GROUP BY category
            ORDER BY category
        """).fetchall()
    return [dict(row) for row in rows]
