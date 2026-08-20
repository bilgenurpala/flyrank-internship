import json
import time
from concurrent.futures import ThreadPoolExecutor

import job_store


class JobRunner:
    def __init__(self, max_workers=2):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def enqueue(self, job_id, payload):
        self.executor.submit(self.run, job_id, payload)

    def run(self, job_id, payload):
        job_store.update(job_id, "running")
        try:
            seconds = float(payload.get("seconds", 0.1))
            if seconds < 0 or seconds > 10:
                raise ValueError("seconds must be between 0 and 10")
            if payload.get("fail"):
                raise RuntimeError("Requested demonstration failure")
            time.sleep(seconds)
            job_store.update(job_id, "done", result=json.dumps({"message": payload.get("message", "Job completed")}))
        except Exception as error:
            job_store.update(job_id, "failed", error=str(error))


runner = JobRunner()
