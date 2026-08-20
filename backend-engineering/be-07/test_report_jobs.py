import time

import pytest
from fastapi.testclient import TestClient

import database
import pdf_report
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATABASE_PATH", tmp_path / "reports.db")
    monkeypatch.setattr(pdf_report, "REPORTS_DIRECTORY", tmp_path / "generated-reports")
    with TestClient(app) as test_client:
        yield test_client


def wait_for(client, job_id):
    for _ in range(100):
        response = client.get(f"/report-jobs/{job_id}")
        if response.json()["status"] in {"done", "failed"}:
            return response.json()
        time.sleep(0.02)
    raise AssertionError("Report job did not finish")


def test_sql_aggregation(client):
    assert database.aggregate_tasks() == [
        {"category": "agent", "total": 1, "completed": 0, "open": 1},
        {"category": "backend", "total": 2, "completed": 2, "open": 0},
        {"category": "portfolio", "total": 2, "completed": 1, "open": 1},
    ]


def test_report_job_generates_stored_pdf(client):
    response = client.post("/report-jobs", json={"title": "Internship Task Summary"})
    assert response.status_code == 202
    assert response.json()["status"] in {"queued", "running", "done"}
    job = wait_for(client, response.json()["id"])
    assert job["status"] == "done"
    report_response = client.get(job["result"]["report_url"])
    assert report_response.status_code == 200
    assert report_response.headers["content-type"] == "application/pdf"
    assert report_response.content.startswith(b"%PDF")
    assert len(report_response.content) > 1000


def test_unknown_job_and_report_return_404(client):
    assert client.get("/report-jobs/missing").status_code == 404
    assert client.get("/reports/missing.pdf").status_code == 404
    assert client.get("/reports/../reports.db").status_code == 404


def test_generation_failure_is_queryable(client, monkeypatch):
    def fail(*args):
        raise RuntimeError("PDF renderer unavailable")

    monkeypatch.setattr(pdf_report, "generate_report", fail)
    response = client.post("/report-jobs", json={"title": "Failure case"})
    job = wait_for(client, response.json()["id"])
    assert job["status"] == "failed"
    assert job["error"] == "PDF renderer unavailable"
