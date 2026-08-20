from concurrent.futures import ThreadPoolExecutor

import database
import job_store
import pdf_report


class ReportJobRunner:
    def __init__(self, max_workers=2):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def enqueue(self, job_id, payload):
        self.executor.submit(self.run, job_id, payload)

    def run(self, job_id, payload):
        job_store.update(job_id, "running")
        try:
            rows = database.aggregate_tasks()
            path = pdf_report.generate_report(job_id, rows, payload["title"])
            job_store.update(
                job_id,
                "done",
                result={"report_url": f"/reports/{path.name}", "rows": rows},
            )
        except Exception as error:
            job_store.update(job_id, "failed", error=str(error))


runner = ReportJobRunner()
