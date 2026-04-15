from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.ai_insights.models import AIInsightRun, AIInsightRunSource


class AIInsightRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, ai_run: AIInsightRun) -> AIInsightRun:
        self.session.add(ai_run)
        await self.session.flush()
        return ai_run

    async def get(self, ai_run_id: UUID) -> AIInsightRun | None:
        result = await self.session.execute(
            select(AIInsightRun)
            .where(AIInsightRun.id == ai_run_id, AIInsightRun.deleted_at.is_(None))
            .options(selectinload(AIInsightRun.sources))
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def add_source(self, source: AIInsightRunSource) -> AIInsightRunSource:
        self.session.add(source)
        await self.session.flush()
        return source
