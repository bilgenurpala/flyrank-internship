import asyncio

import httpx
import pytest
from fastapi.testclient import TestClient

from config import Settings
from main import app, get_classifier
from provider import GeminiClassifier, InvalidModelResponse, ProviderError, ProviderUnavailable


def settings(attempts=3):
    return Settings(gemini_api_key="test-key", ai_max_attempts=attempts)


def gemini_response(category="support", confidence=0.95, summary="Customer needs help"):
    return {
        "candidates": [
            {
                "content": {
                    "parts": [
                        {"text": f'{{"category":"{category}","confidence":{confidence},"summary":"{summary}"}}'}
                    ]
                }
            }
        ]
    }


@pytest.fixture
def client():
    transport = httpx.MockTransport(lambda request: httpx.Response(200, json=gemini_response()))
    async_client = httpx.AsyncClient(transport=transport)
    classifier = GeminiClassifier(settings(), async_client)
    app.dependency_overrides[get_classifier] = lambda: classifier
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_classification_returns_valid_schema(client):
    response = client.post("/classify", json={"message": "I cannot access my account"})
    assert response.status_code == 200
    assert response.json() == {
        "category": "support",
        "confidence": 0.95,
        "summary": "Customer needs help",
        "model": "gemini-3.5-flash-lite",
        "attempts": 1,
    }


def test_short_message_is_rejected(client):
    assert client.post("/classify", json={"message": "hi"}).status_code == 422


def test_retryable_error_then_success():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        if calls == 1:
            return httpx.Response(429)
        return httpx.Response(200, json=gemini_response("sales", 0.9, "Customer wants pricing"))

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            return await GeminiClassifier(settings(), client).classify("How much does it cost?")

    result, attempts = asyncio.run(run())
    assert result.category == "sales"
    assert attempts == 2


def test_non_retryable_error_stops_immediately():
    calls = 0

    def handler(request):
        nonlocal calls
        calls += 1
        return httpx.Response(400)

    async def run():
        async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
            return await GeminiClassifier(settings(), client).classify("Classify this message")

    with pytest.raises(ProviderError, match="status 400"):
        asyncio.run(run())
    assert calls == 1


def test_retries_stop_at_configured_limit():
    async def run():
        transport = httpx.MockTransport(lambda request: httpx.Response(503))
        async with httpx.AsyncClient(transport=transport) as client:
            return await GeminiClassifier(settings(attempts=2), client).classify("Classify this message")

    with pytest.raises(ProviderUnavailable):
        asyncio.run(run())


def test_invalid_json_is_rejected():
    classifier = GeminiClassifier(settings())
    response = httpx.Response(200, json={"candidates": [{"content": {"parts": [{"text": "not-json"}]}}]})
    with pytest.raises(InvalidModelResponse):
        classifier.parse(response)


def test_out_of_range_confidence_is_rejected():
    classifier = GeminiClassifier(settings())
    response = httpx.Response(200, json=gemini_response(confidence=1.2))
    with pytest.raises(InvalidModelResponse):
        classifier.parse(response)
