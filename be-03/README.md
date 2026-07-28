# BE-03 - Auth: Login and Protect

A FastAPI service that delegates user authentication to Supabase Auth, returns JWT access tokens after login, verifies bearer tokens before protected requests, and documents the security flow in Swagger UI.

## Tech Stack

- Python 3.10+
- FastAPI and Uvicorn
- Supabase Auth and the Supabase Python SDK
- JWT bearer authentication
- python-dotenv
- Pytest

## Security Model

The API never stores passwords and does not implement password hashing or token signing. Credentials are sent directly to Supabase Auth, which manages accounts and issues signed JSON Web Tokens. Protected requests are accepted only after `supabase.auth.get_user(token)` validates the supplied access token with Supabase.

The project uses the public Supabase anon key. A Supabase `service_role` key must never be used because it bypasses Row Level Security and other authorization controls.

## Project Structure

```text
be-03/
├── config.py
├── main.py
├── supabase_client.py
├── test_main.py
├── requirements.txt
├── .env.example
└── docs/
    └── swagger-ui.png
```

## Supabase Setup

1. Create a project at [Supabase](https://supabase.com).
2. Open the project API settings and copy the project URL and anon key.
3. For this practice project, open the Email authentication provider settings and disable email confirmation so a newly registered account can log in immediately. Production applications should normally keep email confirmation enabled.
4. Copy `.env.example` to `.env` and add your own values:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
PORT=8000
```

The `.env` file is ignored by Git. Only `.env.example`, which contains placeholders, is committed.

## Install

```bash
cd be-03
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

```bash
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --reload
```

The API starts at `http://127.0.0.1:8000`. Swagger UI is available at `http://127.0.0.1:8000/docs`.

## API Reference

| Method | Path | Authentication | Success | Errors |
|---|---|---|---:|---:|
| GET | `/health` | None | 200 | - |
| POST | `/auth/signup` | None | 201 | 400 |
| POST | `/auth/login` | None | 200 | 400, 401 |
| POST | `/auth/logout` | Bearer JWT | 204 | 401 |
| GET | `/public/info` | None | 200 | - |
| GET | `/protected/profile` | Bearer JWT | 200 | 401 |
| GET | `/protected/dashboard` | Bearer JWT | 200 | 401 |

The dashboard is a second protected endpoint that demonstrates reuse of the same authentication dependency without duplicating token-verification logic.

## Authentication Flow

Create an account:

```bash
curl -i -X POST http://127.0.0.1:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

Log in and copy the returned `access_token`:

```bash
curl -i -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}"
```

Call a protected endpoint:

```bash
curl -i http://127.0.0.1:8000/protected/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Log out:

```bash
curl -i -X POST http://127.0.0.1:8000/auth/logout \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Missing or malformed authorization returns:

```json
{"error":"Access token required"}
```

An invalid, altered, or expired token returns:

```json
{"error":"Invalid or expired token"}
```

## Swagger UI

![Swagger UI showing bearer-protected routes](docs/swagger-ui.png)

Click **Authorize**, paste a Supabase access token, and use **Try it out** on a protected endpoint. The lock icons identify routes that require an `Authorization: Bearer <token>` header.

## Tests

```bash
pytest -q
```

The automated suite uses a fake Supabase Auth client and verifies:

- signup and login success responses
- missing credential and invalid login errors
- public access without a token
- missing, malformed, invalid, and valid bearer tokens
- reusable protection on profile and dashboard routes
- protected logout with an empty 204 response
- OpenAPI bearer security definitions and protected-route declarations

Real end-to-end signup and login require your own Supabase project values in `.env`. No credentials, access tokens, or passwords are included in the repository.

## Logout Note

Supabase revokes refresh tokens when a session is signed out. An already issued access token can remain cryptographically valid until its short expiry time, which is why access tokens are intentionally short-lived.
