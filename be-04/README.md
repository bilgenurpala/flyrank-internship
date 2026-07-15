# BE-04

A layered FastAPI service (keyword-ranking tracker) whose in-memory repository was swapped for a PostgreSQL repository running in Docker — without touching the service or route layers. The whole stack (API + database) starts with a single `docker compose up`.

## Tech Stack

- **Python 3.12** + **FastAPI** + **Uvicorn**
- **PostgreSQL 16** (official Docker image) + **psycopg 3**
- **Docker Compose** for orchestration

## Architecture

```
main.py (HTTP routes)  →  service.py (business rules)  →  repository.py (data access)
```

- `main.py` — routes, request/response models, HTTP error mapping. Also the composition root: the only place where the concrete repository is chosen.
- `service.py` — validation and business logic. Receives the repository via constructor injection; never knows which implementation it talks to.
- `repository.py` — two implementations of the same contract (`add`, `get_all`, `get_by_id`): `InMemoryRankingRepository` (dict-based) and `PostgresRankingRepository` (psycopg 3, parameterized queries).

### Declaration: service and routes did not change

- The three route handlers, the `RankingIn` model, and the whole of `service.py` are byte-for-byte identical to the in-memory version.
- The swap changed only the wiring lines at the top of `main.py`: `InMemoryRankingRepository()` → `PostgresRankingRepository(os.environ["DATABASE_URL"])`.
- This works because both repositories expose the same method signatures and return types (`dict` / `list[dict]` / `None`), and the service depends on that contract, not on a concrete class.

## Project Structure

```
be-04/
├── app/
│   ├── main.py            # routes + composition root
│   ├── service.py         # business logic
│   └── repository.py      # in-memory + Postgres repositories
├── db/
│   └── init.sql           # schema, auto-applied on first DB startup
├── Dockerfile             # builds the API image
├── docker-compose.yml     # app + db, healthcheck, named volume
├── .env.example           # template for the connection string
└── requirements.txt
```

## Setup & Run

### Full stack with Docker Compose (recommended)

```bash
docker compose up --build
```

- Starts `db` (Postgres 16) and `app` (FastAPI) together.
- `db/init.sql` is mounted into `docker-entrypoint-initdb.d`, so the schema is created automatically the first time the database initializes.
- The app waits for the database healthcheck (`pg_isready`) before starting.
- Inside the compose network the app reaches the database at hostname `db`, not `localhost`.

API docs: `http://localhost:8000/docs`

### Local run (app outside Docker)

```bash
cp .env.example .env   # fill in real values
pip install -r requirements.txt
docker run --name flyrank-db -e POSTGRES_USER=... -e POSTGRES_PASSWORD=... -e POSTGRES_DB=... -p 5432:5432 -v flyrank_pgdata:/var/lib/postgresql/data -d postgres:16
uvicorn app.main:app --reload
```

`.env` is gitignored; only `.env.example` is committed.

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/rankings` | Track a keyword ranking (422 on invalid input) |
| GET | `/rankings` | List all rankings |
| GET | `/rankings/{id}` | Get one ranking (404 if missing) |

## Persistence Proof

1. With the stack running, rows were added via `POST /rankings` and verified via `GET /rankings`.
2. `docker compose down` — containers were **deleted**, not just stopped.
3. `docker compose up` recreated the containers from scratch.
4. `GET /rankings` returned the same rows: Postgres writes its data to the named volume `flyrank_pgdata`, which lives independently of container lifecycle.
5. Counter-experiment: with the in-memory repository, restarting Uvicorn wiped all data (a dict lives in process RAM).