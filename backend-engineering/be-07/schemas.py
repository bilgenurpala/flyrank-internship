from enum import StrEnum

from pydantic import BaseModel, Field


class MessageCategory(StrEnum):
    SUPPORT = "support"
    SALES = "sales"
    FEEDBACK = "feedback"
    OTHER = "other"


class ClassificationRequest(BaseModel):
    message: str = Field(min_length=3, max_length=2000)


class ClassificationResult(BaseModel):
    category: MessageCategory
    confidence: float = Field(ge=0, le=1)
    summary: str = Field(min_length=1, max_length=240)


class ClassificationResponse(ClassificationResult):
    model: str
    attempts: int = Field(ge=1)
