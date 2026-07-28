# BE-02 - Connecting Your CRUD to the Database

A FastAPI task service backed by SQLite. The API keeps the same CRUD contract while moving all storage from process memory to a database file that survives server restarts.

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- SQLite through Python's built-in `sqlite3` module
- Pytest

## Why SQLite

SQLite was chosen because it stores the complete database in one file, requires no separate database server, and needs no additional Python package. Unlike an in-memory list, it keeps tasks after the API process stops or restarts.

## Project Structure

```text
be-02/
├── database.py
├── main.py
├── requirements.txt
├── test_main.py
├── docs/
│   └── database-view.png
└── sql/
    └── stage-4.sql
```

The database is stored at `be-02/tasks.db`. The file is created automatically when the application starts and is ignored by Git so every clone begins with a fresh local database.

## Setup

```bash
cd be-02
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000` and the interactive documentation is available at `http://127.0.0.1:8000/docs`.

On the first start, the application creates the `tasks` table and inserts exactly three example tasks. The seed transaction runs only when the table is empty, so restarting the server does not duplicate data.

## API Contract

| Method | Path | Success | Invalid Body | Unknown ID |
|---|---|---:|---:|---:|
| GET | `/tasks` | 200 | - | - |
| GET | `/tasks/{id}` | 200 | - | 404 |
| POST | `/tasks` | 201 | 400 | - |
| PUT | `/tasks/{id}` | 200 | 400 | 404 |
| DELETE | `/tasks/{id}` | 204 | - | 404 |

Create a task:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Review SQLite queries\"}"
```

Update a task:

```bash
curl -i -X PUT http://127.0.0.1:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Learn SQLite\",\"done\":true}"
```

Delete a task:

```bash
curl -i -X DELETE http://127.0.0.1:8000/tasks/1
```

Unknown task IDs return:

```json
{"error":"Task not found"}
```

Invalid create requests return:

```json
{"error":"Title is required"}
```

## Persistence

Every create, read, update, and delete operation uses parameterized SQL queries. Values are passed separately through `?` placeholders instead of being joined into SQL strings.

Persistence can be verified by creating a task, stopping Uvicorn, starting it again, and calling `GET /tasks`. The task remains available because it is stored in `tasks.db` rather than process memory.

## Database View

![The tasks table in the SQLite database](docs/database-view.png)

The image shows the generated `tasks.db` file, the `tasks` table schema, and the same seed rows returned by the API.

## SQL Exploration

The Stage 4 statements are stored in `sql/stage-4.sql`. One query executed manually was:

```sql
SELECT * FROM tasks WHERE done = 1;
```

It returned only tasks whose `done` value was `1`. After running `UPDATE tasks SET done = 1`, the same completed state appeared immediately through `GET /tasks` because the API and the direct SQL query use the same database file.

## Tests

```bash
pytest -q
```

The tests verify one-time seeding, all CRUD endpoints, persistence at the SQLite layer, validation errors, missing-resource errors, and the required HTTP status codes.

Identical endpoint tests passing after the storage change demonstrate that persistence is an implementation detail behind the API contract.
