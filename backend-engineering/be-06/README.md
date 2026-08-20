# BE-06: Your First Background Job

This FastAPI service accepts a small demonstration job, returns `202 Accepted` immediately, runs the work in a bounded thread pool, and exposes its state through a polling endpoint. SQLite keeps job metadata across application restarts.

## Job lifecycle

`queued → running → done` or `queued → running → failed`

`POST /jobs` stores the queued record before handing it to the runner. `GET /jobs/{job_id}` returns timestamps, input, result, and a safe error message. The runner uses two worker threads, so HTTP request threads do not perform the long-running work.

## Run

```bash
cd backend-engineering/be-06
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

```bash
curl -X POST http://127.0.0.1:8000/jobs -H 'Content-Type: application/json' -d '{"message":"Report ready","seconds":2}'
curl http://127.0.0.1:8000/jobs/JOB_ID
python -m pytest -q
```

## Failure and retry policy

Exceptions move a job to `failed` and preserve the reason for inspection. Automatic retries are intentionally disabled: a generic runner cannot know whether arbitrary work is idempotent, and retrying tomorrow's PDF generation could create duplicate artifacts. A later production version should add job-specific idempotency keys, retryable error categories, attempt counts, and exponential backoff before enabling retries.

This is a single-process learning implementation, not a durable distributed queue. A process crash while a job is running leaves it in `running`; multiple app processes would each have their own executor. Production alternatives include a database-backed worker system such as Celery or Dramatiq with Redis or RabbitMQ.
