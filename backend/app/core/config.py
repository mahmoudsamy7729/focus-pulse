from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.settings.database import DatabaseSettings


class Settings(BaseSettings):
    """Application settings aggregate."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "FocusPulse"
    environment: str = "local"
    database: DatabaseSettings = DatabaseSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
