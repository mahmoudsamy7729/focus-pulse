from app.core.config import Settings
from app.modules.ai_insights.providers.base import AIAnalysisProvider, DeterministicAIAnalysisProvider


def get_configured_ai_provider(_: Settings | None = None) -> AIAnalysisProvider:
    """Return the configured provider adapter.

    Phase 4 keeps production SDK integration behind this boundary. The default
    deterministic adapter is intentionally local and network-free.
    """

    return DeterministicAIAnalysisProvider()
