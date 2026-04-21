"""AI analysis schedule persistence placeholder for Phase 6 automation."""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession


class AIAnalysisScheduleRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
