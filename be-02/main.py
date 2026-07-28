from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from database import get_connection, initialize_database


def task_from_row(row):
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@asynccontextmanager
async def lifespan(application: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="FlyRank BE-02", lifespan=lifespan)


@app.get("/tasks")
def list_tasks():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()
    return [task_from_row(row) for row in rows]


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT id, title, done FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()
    if row is None:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    return task_from_row(row)
