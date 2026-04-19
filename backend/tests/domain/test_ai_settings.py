from app.core.config import Settings
from app.modules.ai_insights.constants import AI_INSIGHT_MAX_ATTEMPTS


def test_ai_settings_are_composed_with_safe_defaults() -> None:
    settings = Settings()

    assert settings.ai.provider == "deterministic"
    assert settings.ai.model
    assert settings.ai.request_timeout_seconds > 0
    assert settings.ai.max_attempts == AI_INSIGHT_MAX_ATTEMPTS
