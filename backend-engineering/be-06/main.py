import json
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import job_store
from jobs import runner


class JobRequest(BaseModel):
    message: str = "Job completed"
    seconds: float = 0.1
    fail: bool = False


def serialize(job):
    if job and job["result"]:
        job["result"] = json.loads(job["result"])
    if job:
        job["payload"] = json.loads(job["payload"])
    return job


@asynccontextmanager
async def lifespan(application):
    job_store.initialize()
    yield


app = FastAPI(title="FlyRank BE-06", lifespan=lifespan)


@app.post("/jobs", status_code=202)
def create_job(request: JobRequest):
    job_id = str(uuid4())
    payload = request.model_dump()
    job = job_store.create(job_id, "demonstration", json.dumps(payload))
    runner.enqueue(job_id, payload)
    return serialize(job)


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = job_store.get(job_id)
    if job is None:
        return JSONResponse(status_code=404, content={"error": "Job not found"})
    return serialize(job)
