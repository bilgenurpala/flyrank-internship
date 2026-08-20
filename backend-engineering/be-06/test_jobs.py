import time

import pytest
from fastapi.testclient import TestClient

import job_store
from main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(job_store, "DATABASE_PATH", tmp_path / "jobs.db")
    with TestClient(app) as test_client:
        yield test_client


def wait_for(client, job_id):
    for _ in range(100):
        response = client.get(f"/jobs/{job_id}")
        if response.json()["status"] in {"done", "failed"}:
            return response
        time.sleep(0.01)
    raise AssertionError("Job did not finish")


def test_request_returns_accepted_and_job_finishes(client):
    response = client.post("/jobs", json={"message": "Report ready", "seconds": 0})
    assert response.status_code == 202
    assert response.json()["status"] in {"queued", "running", "done"}
    finished = wait_for(client, response.json()["id"])
    assert finished.json()["status"] == "done"
    assert finished.json()["result"] == {"message": "Report ready"}


def test_failure_is_visible(client):
    response = client.post("/jobs", json={"fail": True, "seconds": 0})
    finished = wait_for(client, response.json()["id"])
    assert finished.json()["status"] == "failed"
    assert finished.json()["error"] == "Requested demonstration failure"


def test_unknown_job_returns_404(client):
    assert client.get("/jobs/missing").status_code == 404
