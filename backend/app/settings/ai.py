from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.modules.ai_insights.constants import AI_INSIGHT_MAX_ATTEMPTS


class AISettings(BaseSettings):
    """AI provider configuration sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="AI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    provider: str = Field(default="deterministic")
    model: str = Field(default="focuspulse-deterministic-v1")
    api_key: str | None = Field(default=None)
    request_timeout_seconds: float = Field(default=30.0, gt=0)
    max_attempts: int = Field(default=AI_INSIGHT_MAX_ATTEMPTS, ge=1, le=AI_INSIGHT_MAX_ATTEMPTS)
