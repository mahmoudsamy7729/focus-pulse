from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.settings.ai import AISettings
from app.settings.app import AppSettings
from app.settings.celery import CelerySettings
from app.settings.database import DatabaseSettings
from app.settings.redis import RedisSettings


class Settings(BaseSettings):
    """Application settings aggregate."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    ai: AISettings = AISettings()

    @property
    def app_name(self) -> str:
        return self.app.name

    @property
    def environment(self) -> str:
        return self.app.environment


@lru_cache
def get_settings() -> Settings:
    return Settings()
