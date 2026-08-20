import json
from datetime import datetime, timezone

import database


def now():
    return datetime.now(timezone.utc).isoformat()


def create(job_id, payload):
    created_at = now()
    with database.connect() as connection:
        connection.execute(
            "INSERT INTO jobs (id, kind, status, payload, created_at) VALUES (?, 'pdf-report', 'queued', ?, ?)",
            (job_id, json.dumps(payload), created_at),
        )
    return get(job_id)


def update(job_id, status, result=None, error=None):
    started_at = now() if status == "running" else None
    finished_at = now() if status in {"done", "failed"} else None
    with database.connect() as connection:
        connection.execute(
            "UPDATE jobs SET status = ?, result = COALESCE(?, result), error = COALESCE(?, error), started_at = COALESCE(?, started_at), finished_at = COALESCE(?, finished_at) WHERE id = ?",
            (status, json.dumps(result) if result is not None else None, error, started_at, finished_at, job_id),
        )


def get(job_id):
    with database.connect() as connection:
        row = connection.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
    if row is None:
        return None
    job = dict(row)
    job["payload"] = json.loads(job["payload"])
    job["result"] = json.loads(job["result"]) if job["result"] else None
    return job
