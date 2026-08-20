from fastapi import Depends, FastAPI, HTTPException

from config import Settings, get_settings
from provider import GeminiClassifier, InvalidModelResponse, ProviderError, ProviderUnavailable
from schemas import ClassificationRequest, ClassificationResponse


app = FastAPI(title="FlyRank BE-07: Connect to an AI API")


def get_classifier(settings: Settings = Depends(get_settings)) -> GeminiClassifier:
    return GeminiClassifier(settings)


@app.post("/classify", response_model=ClassificationResponse)
async def classify_message(
    request: ClassificationRequest,
    classifier: GeminiClassifier = Depends(get_classifier),
) -> ClassificationResponse:
    try:
        result, attempts = await classifier.classify(request.message)
    except ProviderUnavailable as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    except InvalidModelResponse as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except ProviderError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    return ClassificationResponse(**result.model_dump(), model=classifier.settings.gemini_model, attempts=attempts)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
