from contextlib import asynccontextmanager
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field

import database
import job_store
import pdf_report
from jobs import runner


class ReportRequest(BaseModel):
    title: str = Field(default="Task Summary Report", min_length=1, max_length=120)


@asynccontextmanager
async def lifespan(application):
    database.initialize()
    yield


app = FastAPI(title="FlyRank BE-08", lifespan=lifespan)


@app.post("/report-jobs", status_code=202)
def create_report_job(request: ReportRequest):
    job_id = str(uuid4())
    payload = request.model_dump()
    job = job_store.create(job_id, payload)
    runner.enqueue(job_id, payload)
    return job


@app.get("/report-jobs/{job_id}")
def get_report_job(job_id: str):
    job = job_store.get(job_id)
    if job is None:
        return JSONResponse(status_code=404, content={"error": "Job not found"})
    return job


@app.get("/reports/{filename}")
def download_report(filename: str):
    safe_name = Path(filename).name
    path = pdf_report.REPORTS_DIRECTORY / safe_name
    if safe_name != filename or not path.is_file():
        return JSONResponse(status_code=404, content={"error": "Report not found"})
    return FileResponse(path, media_type="application/pdf", filename=safe_name)
