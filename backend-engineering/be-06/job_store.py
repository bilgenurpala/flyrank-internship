import sqlite3
from datetime import datetime, timezone
from pathlib import Path


DATABASE_PATH = Path(__file__).with_name("jobs.db")


def now():
    return datetime.now(timezone.utc).isoformat()


def connect():
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def initialize():
    with connect() as connection:
        connection.execute("""
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
            )
        """)


def create(job_id, kind, payload):
    created_at = now()
    with connect() as connection:
        connection.execute("INSERT INTO jobs (id, kind, status, payload, created_at) VALUES (?, ?, 'queued', ?, ?)", (job_id, kind, payload, created_at))
    return get(job_id)


def update(job_id, status, result=None, error=None):
    started_at = now() if status == "running" else None
    finished_at = now() if status in {"done", "failed"} else None
    with connect() as connection:
        connection.execute("UPDATE jobs SET status = ?, result = COALESCE(?, result), error = COALESCE(?, error), started_at = COALESCE(?, started_at), finished_at = COALESCE(?, finished_at) WHERE id = ?", (status, result, error, started_at, finished_at, job_id))


def get(job_id):
    with connect() as connection:
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    return dict(row) if row else None
