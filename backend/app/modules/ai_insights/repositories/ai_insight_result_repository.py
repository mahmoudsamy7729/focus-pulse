from __future__ import annotations

from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import Select, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.ai_insights.constants import InsightResultStatus
from app.modules.ai_insights.models import AIInsightResult, AIInsightResultSource


class AIInsightResultRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _active_query() -> Select[tuple[AIInsightResult]]:
        return select(AIInsightResult).where(AIInsightResult.deleted_at.is_(None))

    async def add(self, result: AIInsightResult) -> AIInsightResult:
        self.session.add(result)
        await self.session.flush()
        return result

    async def add_sources(self, result: AIInsightResult, daily_log_ids: list[UUID]) -> None:
        for daily_log_id in dict.fromkeys(daily_log_ids):
            source = AIInsightResultSource(
                owner_id=result.owner_id,
                ai_insight_result_id=result.id,
                daily_log_id=daily_log_id,
                created_at=datetime.now(UTC),
            )
            source.ai_insight_result = result
            self.session.add(source)
        await self.session.flush()

    async def get_for_owner(self, owner_id: UUID, result_id: UUID) -> AIInsightResult | None:
        query = (
            self._active_query()
            .where(AIInsightResult.owner_id == owner_id, AIInsightResult.id == result_id)
            .options(selectinload(AIInsightResult.sources))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def find_current(
        self,
        owner_id: UUID,
        period_granularity: str,
        period_start: date,
        period_end: date,
    ) -> AIInsightResult | None:
        query = (
            self._active_query()
            .where(
                AIInsightResult.owner_id == owner_id,
                AIInsightResult.period_granularity == period_granularity,
                AIInsightResult.period_start == period_start,
                AIInsightResult.period_end == period_end,
                AIInsightResult.status == InsightResultStatus.COMPLETED.value,
                AIInsightResult.is_current.is_(True),
            )
            .order_by(AIInsightResult.generated_at.desc(), AIInsightResult.created_at.desc())
            .options(selectinload(AIInsightResult.sources))
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def find_default_reuse(
        self,
        owner_id: UUID,
        period_granularity: str,
        period_start: date,
        period_end: date,
        source_ai_insight_run_id: UUID,
    ) -> AIInsightResult | None:
        query = (
            self._active_query()
            .where(
                AIInsightResult.owner_id == owner_id,
                AIInsightResult.period_granularity == period_granularity,
                AIInsightResult.period_start == period_start,
                AIInsightResult.period_end == period_end,
                AIInsightResult.source_ai_insight_run_id == source_ai_insight_run_id,
                AIInsightResult.status == InsightResultStatus.COMPLETED.value,
                AIInsightResult.is_current.is_(True),
            )
            .order_by(AIInsightResult.generated_at.desc())
            .options(selectinload(AIInsightResult.sources))
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def find_by_idempotency_key(self, owner_id: UUID, idempotency_key: str) -> AIInsightResult | None:
        result = await self.session.execute(
            self._active_query()
            .where(AIInsightResult.owner_id == owner_id, AIInsightResult.idempotency_key == idempotency_key)
            .options(selectinload(AIInsightResult.sources))
        )
        return result.scalar_one_or_none()

    async def clear_current(
        self,
        owner_id: UUID,
        period_granularity: str,
        period_start: date,
        period_end: date,
    ) -> None:
        await self.session.execute(
            update(AIInsightResult)
            .where(
                AIInsightResult.owner_id == owner_id,
                AIInsightResult.period_granularity == period_granularity,
                AIInsightResult.period_start == period_start,
                AIInsightResult.period_end == period_end,
                AIInsightResult.deleted_at.is_(None),
                AIInsightResult.is_current.is_(True),
            )
            .values(is_current=False)
        )
        await self.session.flush()

    async def list_for_owner(
        self,
        owner_id: UUID,
        *,
        page: int,
        limit: int,
        period_granularity: str | None = None,
        status: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> tuple[list[AIInsightResult], int]:
        query = self._filtered_owner_query(owner_id, period_granularity, status, start_date, end_date)
        count_result = await self.session.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()
        result = await self.session.execute(
            query.order_by(AIInsightResult.generated_at.desc(), AIInsightResult.created_at.desc())
            .offset((page - 1) * limit)
            .limit(limit)
        )
        return list(result.scalars().unique()), int(total)

    def _filtered_owner_query(
        self,
        owner_id: UUID,
        period_granularity: str | None,
        status: str | None,
        start_date: date | None,
        end_date: date | None,
    ) -> Select[tuple[AIInsightResult]]:
        query = self._active_query().where(AIInsightResult.owner_id == owner_id).options(selectinload(AIInsightResult.sources))
        if period_granularity is not None:
            query = query.where(AIInsightResult.period_granularity == period_granularity)
        if status is not None:
            query = query.where(AIInsightResult.status == status)
        if start_date is not None:
            query = query.where(AIInsightResult.period_start >= start_date)
        if end_date is not None:
            query = query.where(AIInsightResult.period_end <= end_date)
        return query
