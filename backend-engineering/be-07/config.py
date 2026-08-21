from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    gemini_api_key: str = Field(min_length=1)
    gemini_model: str = "gemini-3.5-flash-lite"
    ai_timeout_seconds: float = Field(default=10, gt=0, le=60)
    ai_max_attempts: int = Field(default=3, ge=1, le=5)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
