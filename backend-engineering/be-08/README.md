# BE-08: PDF Report Generator

This FastAPI service queries task data with SQL aggregation, queues report creation outside the HTTP request, stores the generated PDF on disk, and returns a download URL through a queryable job record.

## Reused job pattern

BE-08 deliberately reuses the BE-06 lifecycle instead of introducing a second orchestration model:

`queued → running → done` or `queued → running → failed`

The API stores the job before handing it to a bounded two-thread worker pool. `GET /report-jobs/{id}` exposes timestamps, input, result, and failure state. The result contains a stored report URL rather than transporting the PDF through the job payload.

## Data flow

```text
POST /report-jobs
  → persist queued job
  → aggregate tasks by category in SQLite
  → render PDF with ReportLab
  → store generated-reports/task-summary-{job_id}.pdf
  → mark job done with /reports/{filename}
```

## Run

```bash
cd backend-engineering/be-08
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

```bash
curl -X POST http://127.0.0.1:8000/report-jobs \
  -H 'Content-Type: application/json' \
  -d '{"title":"Internship Task Summary"}'
curl http://127.0.0.1:8000/report-jobs/JOB_ID
curl --output report.pdf http://127.0.0.1:8000/reports/REPORT_FILENAME
python -m pytest -q
```

## Failure and retry policy

A renderer, query, or storage exception moves the job to `failed` and leaves the failure queryable. Automatic retry remains disabled because repeated report generation creates duplicate files unless the request has an idempotency key. Scheduling is intentionally outside the assignment's on-demand scope.

## Limitations

This is a single-process learning implementation. SQLite persists metadata, but a process crash can leave a running job unresolved. Multiple API processes would not share the in-memory executor, generated files use local storage, old reports are not automatically deleted, and the API has no authentication or per-user report isolation.
