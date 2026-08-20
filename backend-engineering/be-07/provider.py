import asyncio
import json

import httpx
from pydantic import ValidationError

from config import Settings
from schemas import ClassificationResult


class ProviderError(RuntimeError):
    pass


class ProviderUnavailable(ProviderError):
    pass


class InvalidModelResponse(ProviderError):
    pass


class GeminiClassifier:
    retryable_statuses = {429, 500, 502, 503, 504}

    def __init__(self, settings: Settings, client: httpx.AsyncClient | None = None):
        self.settings = settings
        self.client = client

    @property
    def endpoint(self) -> str:
        return f"https://generativelanguage.googleapis.com/v1beta/models/{self.settings.gemini_model}:generateContent"

    def payload(self, message: str) -> dict:
        schema = {
            "type": "OBJECT",
            "properties": {
                "category": {"type": "STRING", "enum": ["support", "sales", "feedback", "other"]},
                "confidence": {"type": "NUMBER", "minimum": 0, "maximum": 1},
                "summary": {"type": "STRING", "maxLength": 240},
            },
            "required": ["category", "confidence", "summary"],
        }
        prompt = (
            "Classify the customer message. Use support for help or fault reports, sales for buying intent, "
            "feedback for opinions, and other when none apply. Return only the requested JSON.\n\n"
            f"Message: {message}"
        )
        return {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0,
                "responseMimeType": "application/json",
                "responseJsonSchema": schema,
            },
        }

    async def classify(self, message: str) -> tuple[ClassificationResult, int]:
        owns_client = self.client is None
        client = self.client or httpx.AsyncClient(timeout=self.settings.ai_timeout_seconds)
        try:
            for attempt in range(1, self.settings.ai_max_attempts + 1):
                try:
                    response = await client.post(
                        self.endpoint,
                        params={"key": self.settings.gemini_api_key},
                        json=self.payload(message),
                    )
                except (httpx.TimeoutException, httpx.NetworkError) as error:
                    if attempt == self.settings.ai_max_attempts:
                        raise ProviderUnavailable("AI provider did not respond in time") from error
                    await asyncio.sleep(0.1 * 2 ** (attempt - 1))
                    continue
                if response.status_code in self.retryable_statuses:
                    if attempt == self.settings.ai_max_attempts:
                        raise ProviderUnavailable("AI provider remained unavailable")
                    await asyncio.sleep(0.1 * 2 ** (attempt - 1))
                    continue
                if response.is_error:
                    raise ProviderError(f"AI provider rejected the request with status {response.status_code}")
                return self.parse(response), attempt
            raise ProviderUnavailable("AI provider remained unavailable")
        finally:
            if owns_client:
                await client.aclose()

    def parse(self, response: httpx.Response) -> ClassificationResult:
        try:
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return ClassificationResult.model_validate(json.loads(text))
        except (ValueError, KeyError, IndexError, TypeError, ValidationError) as error:
            raise InvalidModelResponse("AI provider returned an invalid structured response") from error
