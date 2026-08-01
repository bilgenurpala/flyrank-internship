# BE-04 - Containerize Your Stack

A layered FastAPI keyword-ranking service backed by PostgreSQL and orchestrated with Docker Compose. The storage implementation changes without rewriting the service or HTTP route layers.

[Back to internship portfolio](../../README.md)

## Architecture

```mermaid
flowchart LR
    C["API client"] -->|"HTTP"| R["FastAPI routes"]
    R --> S["RankingService"]
    S --> P["PostgresRankingRepository"]
    P -->|"Parameterized SQL"| DB[("PostgreSQL 16")]
    V[("Named volume")] --- DB
```

```mermaid
flowchart TB
    DC["docker compose up"] --> APP["app container"]
    DC --> DB["db container"]
    DB --> HC["pg_isready health check"]
    HC --> APP
    DB --> VOL["flyrank_pgdata volume"]
```

## Tech Stack

- Python 3.12
- FastAPI and Uvicorn
- PostgreSQL 16
- psycopg 3
- Docker and Docker Compose

## Layer Responsibilities

| Layer | File | Responsibility |
|---|---|---|
| HTTP | `app/main.py` | Routes, request models, status codes, dependency wiring |
| Business | `app/service.py` | Validation and ranking rules |
| Data | `app/repository.py` | Repository contract and PostgreSQL queries |
| Schema | `db/init.sql` | Automatic database initialization |

The service depends on a repository contract rather than a concrete database. `InMemoryRankingRepository` and `PostgresRankingRepository` expose the same methods and return shapes, so infrastructure can be swapped at the composition root.

## Project Structure

```text
be-04/
├── app/
│   ├── main.py
│   ├── service.py
│   └── repository.py
├── db/
│   └── init.sql
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

## Run the Full Stack

```bash
cd backend-engineering/be-04
docker compose up --build
```

The API is available at `http://localhost:8000`; Swagger UI is at `http://localhost:8000/docs`.

Compose starts both services, waits for PostgreSQL's health check, applies `db/init.sql` during first initialization, and connects the application to database hostname `db` inside the Compose network.

## Configuration

Copy `.env.example` to `.env` when running outside the provided Compose defaults. `.env` remains ignored by Git.

```env
DATABASE_URL=postgresql://flyrank:flyrank_dev@localhost:5432/flyrank
```

The Compose-managed app uses hostname `db` internally; a locally running app connects through the published host port at `localhost`.

## API Reference

| Method | Path | Purpose | Success | Errors |
|---|---|---|---:|---:|
| POST | `/rankings` | Track a keyword position | 201 | 422 |
| GET | `/rankings` | List tracked rankings | 200 | - |
| GET | `/rankings/{id}` | Read one ranking | 200 | 404 |

## Example

```bash
curl -i -X POST http://localhost:8000/rankings \
  -H "Content-Type: application/json" \
  -d "{\"keyword\":\"fastapi hosting\",\"position\":3,\"url\":\"https://example.com\"}"

curl -i http://localhost:8000/rankings
```

## Persistence Proof

1. Create ranking rows through `POST /rankings`.
2. Confirm them with `GET /rankings`.
3. Run `docker compose down` to delete the containers.
4. Run `docker compose up` to recreate them.
5. Confirm that the rows remain available.

The `flyrank_pgdata` named volume exists independently of container lifecycle. Containers are replaceable compute; the volume is durable state.

## Design Evidence

- SQL values are parameterized with psycopg placeholders.
- Database connections use context managers and commit or roll back predictably.
- The application waits for a healthy database before startup.
- Only the composition root selects the concrete repository.

## What I Learned

- Service layers become easier to test when they depend on contracts instead of infrastructure.
- Docker Compose provides repeatable service discovery, startup ordering, and persistent volumes.
- A container can be deleted safely when durable state lives outside its writable layer.
- PostgreSQL can replace memory storage without changing client-facing routes.
