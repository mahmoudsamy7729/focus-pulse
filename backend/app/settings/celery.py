from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class CelerySettings(BaseSettings):
    """Celery broker/result backend settings."""

    model_config = SettingsConfigDict(
        env_prefix="CELERY_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    broker_url: str = Field(default="redis://localhost:6379/1")
    result_backend: str = Field(default="redis://localhost:6379/2")
    default_queue: str = Field(default="focuspulse")
    task_always_eager: bool = Field(default=False)
    scheduler_enabled: bool = Field(default=True)
    beat_schedule_interval_seconds: int = Field(default=60, ge=10)
    schedule_retention_days: int = Field(default=90, ge=1)
    max_scheduled_run_attempts: int = Field(default=3, ge=1)
