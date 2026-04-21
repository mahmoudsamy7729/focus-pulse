"""AI analysis schedule management placeholder for Phase 6 automation."""

from __future__ import annotations

from app.modules.ai_insights.repositories.ai_analysis_schedule_repository import AIAnalysisScheduleRepository


class AIAnalysisScheduleService:
    def __init__(self, repository: AIAnalysisScheduleRepository) -> None:
        self.repository = repository
