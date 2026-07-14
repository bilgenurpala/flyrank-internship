# Week 1 — Build Your First API Endpoint (BE-01)

A minimal FastAPI backend that exposes three JSON GET endpoints, callable from both `curl` and the browser.

## Tech Stack

- **Python 3** + **FastAPI 0.139**
- **Uvicorn** as the ASGI server

## Setup & Run

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn main:app --reload
```

The server starts at `http://127.0.0.1:8000`.

## Endpoints

### `GET /`

Returns a greeting message.

```bash
curl http://127.0.0.1:8000/
```

```json
{ "message": "Hello, from FlyRank!" }
```

### `GET /health`

Returns the service health status.

```bash
curl http://127.0.0.1:8000/health
```

```json
{ "status": "ok" }
```

### `GET /ping`

Simple liveness ping.

```bash
curl http://127.0.0.1:8000/ping
```

```json
{ "ping": "pong" }
```

## How It Works

The entire app lives in a single `main.py` file. It creates a `FastAPI()` application instance and registers three route-handler functions with the `@app.get()` decorator — one for each endpoint. Each handler returns a Python dictionary, which FastAPI automatically serializes to a JSON response. Uvicorn serves the app as an ASGI server and the `--reload` flag enables auto-restart on code changes during development.

## What I Learned

- **FastAPI turns Python dicts into JSON responses automatically** — no manual serialization needed; the framework handles content-type headers and encoding.
- **Decorator-based routing (`@app.get`)** maps URL paths to plain Python functions, making it simple to add new endpoints.
- **Uvicorn's `--reload` flag** watches for file changes and restarts the server, which shortens the edit → test feedback loop during development.
