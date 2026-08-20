# BE-07: Connect to an AI API

This FastAPI service sends customer messages to the Google Gemini API and returns a small, validated classification instead of exposing untrusted model text directly. The response is constrained to `support`, `sales`, `feedback`, or `other`, with a bounded confidence value and summary.

## Trust boundary

The provider is asked for JSON matching an explicit schema. Pydantic validates the result again before the API returns it. Malformed model output becomes `502 Bad Gateway`; provider timeouts and exhausted transient failures become `503 Service Unavailable`. Authentication and other non-transient 4xx errors are not retried.

Retries are limited to three attempts by default and apply only to network failures, timeouts, `429`, and selected `5xx` responses. Exponential backoff prevents a tight retry loop. The API key is read from the environment and never returned to clients or committed.

## Run

```bash
cd backend-engineering/be-07
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

Create a Gemini API key in Google AI Studio and set `GEMINI_API_KEY` in `.env` before starting the server.

```bash
curl -X POST http://127.0.0.1:8000/classify \
  -H 'Content-Type: application/json' \
  -d '{"message":"I cannot sign in to my account"}'
```

```json
{
  "category": "support",
  "confidence": 0.98,
  "summary": "Customer cannot access their account",
  "model": "gemini-2.5-flash-lite",
  "attempts": 1
}
```

## Test

```bash
python -m pytest -q
```

The eight tests cover health, schema-valid output, input validation, transient retry, non-retryable errors, retry exhaustion, malformed JSON, and invalid confidence values. Provider calls use an HTTP mock, so the suite is deterministic and does not spend API quota.

## Limits

Structured output narrows the response shape but does not prove that a classification is correct. Confidence is self-reported by the model and is not calibrated. This service has no authentication, persistent audit log, rate limiter, moderation layer, or fallback provider. Production use would also need observability, request identifiers, privacy review, and an evaluation dataset tied to the real domain.
