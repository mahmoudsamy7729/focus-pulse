from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.settings.celery import CelerySettings
from app.settings.database import DatabaseSettings
from app.settings.redis import RedisSettings


class Settings(BaseSettings):
    """Application settings aggregate."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "FocusPulse"
    environment: str = "local"
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
