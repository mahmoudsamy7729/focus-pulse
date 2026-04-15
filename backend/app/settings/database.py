from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    """Database configuration sourced from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="DATABASE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    url: str = Field(
        default="postgresql+asyncpg://focuspulse:focuspulse@localhost:5432/focuspulse",
        description="Async SQLAlchemy database URL.",
    )
    echo: bool = Field(default=False, description="Enable SQLAlchemy SQL logging.")
    pool_size: int = Field(default=5, ge=1)
    max_overflow: int = Field(default=10, ge=0)
