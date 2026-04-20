from datetime import UTC, date, datetime
from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.ai_insights.models import AIInsightRun, AIInsightRunSource
from app.shared.enums.run_status import RunStatus


class AIInsightRunRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _active_query() -> Select[tuple[AIInsightRun]]:
        return select(AIInsightRun).where(AIInsightRun.deleted_at.is_(None))

    async def add(self, ai_run: AIInsightRun) -> AIInsightRun:
        self.session.add(ai_run)
        await self.session.flush()
        return ai_run

    async def get(self, ai_run_id: UUID) -> AIInsightRun | None:
        result = await self.session.execute(
            self._active_query()
            .where(AIInsightRun.id == ai_run_id)
            .options(selectinload(AIInsightRun.sources))
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def get_for_owner(self, owner_id: UUID, ai_run_id: UUID) -> AIInsightRun | None:
        result = await self.session.execute(
            self._active_query()
            .where(AIInsightRun.owner_id == owner_id, AIInsightRun.id == ai_run_id)
            .options(selectinload(AIInsightRun.sources))
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def add_source(self, source: AIInsightRunSource) -> AIInsightRunSource:
        self.session.add(source)
        await self.session.flush()
        return source

    async def replace_sources(self, ai_run: AIInsightRun, daily_log_ids: list[UUID]) -> None:
        existing = {source.daily_log_id: source for source in ai_run.sources}
        for daily_log_id in daily_log_ids:
            if daily_log_id not in existing:
                source = AIInsightRunSource(
                    owner_id=ai_run.owner_id,
                    ai_insight_run_id=ai_run.id,
                    daily_log_id=daily_log_id,
                    created_at=datetime.now(UTC),
                )
                source.ai_insight_run = ai_run
                self.session.add(source)
        await self.session.flush()

    async def find_by_idempotency_key(
        self,
        owner_id: UUID,
        target_period_type: str,
        period_start: date,
        period_end: date,
        idempotency_key: str,
    ) -> AIInsightRun | None:
        result = await self.session.execute(
            self._active_query()
            .where(
                AIInsightRun.owner_id == owner_id,
                AIInsightRun.target_period_type == target_period_type,
                AIInsightRun.period_start == period_start,
                AIInsightRun.period_end == period_end,
                AIInsightRun.idempotency_key == idempotency_key,
            )
            .options(selectinload(AIInsightRun.sources))
        )
        return result.scalar_one_or_none()

    async def find_in_flight(
        self,
        owner_id: UUID,
        target_period_type: str,
        period_start: date,
        period_end: date,
    ) -> AIInsightRun | None:
        result = await self.session.execute(
            self._active_query()
            .where(
                AIInsightRun.owner_id == owner_id,
                AIInsightRun.target_period_type == target_period_type,
                AIInsightRun.period_start == period_start,
                AIInsightRun.period_end == period_end,
                AIInsightRun.status.in_([RunStatus.PENDING.value, RunStatus.PROCESSING.value]),
            )
            .order_by(AIInsightRun.created_at.desc())
        )
        return result.scalars().first()

    async def find_current_result(
        self,
        owner_id: UUID,
        target_period_type: str,
        period_start: date,
        period_end: date,
    ) -> AIInsightRun | None:
        result = await self.session.execute(
            self._active_query()
            .where(
                AIInsightRun.owner_id == owner_id,
                AIInsightRun.target_period_type == target_period_type,
                AIInsightRun.period_start == period_start,
                AIInsightRun.period_end == period_end,
                AIInsightRun.status == RunStatus.COMPLETED.value,
                AIInsightRun.output_outcome.is_not(None),
            )
            .order_by(AIInsightRun.completed_at.desc().nullslast(), AIInsightRun.created_at.desc())
            .options(selectinload(AIInsightRun.sources))
        )
        return result.scalars().first()

    async def find_completed_source_analysis(
        self,
        owner_id: UUID,
        target_period_type: str,
        period_start: date,
        period_end: date,
        ai_run_id: UUID | None = None,
    ) -> AIInsightRun | None:
        query = (
            self._active_query()
            .where(
                AIInsightRun.owner_id == owner_id,
                AIInsightRun.target_period_type == target_period_type,
                AIInsightRun.period_start == period_start,
                AIInsightRun.period_end == period_end,
                AIInsightRun.status == RunStatus.COMPLETED.value,
                AIInsightRun.output_outcome.is_not(None),
                AIInsightRun.output_summary.is_not(None),
            )
            .options(selectinload(AIInsightRun.sources))
            .order_by(AIInsightRun.completed_at.desc().nullslast(), AIInsightRun.created_at.desc())
        )
        if ai_run_id is not None:
            query = query.where(AIInsightRun.id == ai_run_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def list_for_owner(
        self,
        owner_id: UUID,
        *,
        page: int,
        limit: int,
        target_period_type: str | None = None,
        status: str | None = None,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> tuple[list[AIInsightRun], int]:
        query = self._filtered_owner_query(owner_id, target_period_type, status, start_date, end_date)
        count_result = await self.session.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()
        result = await self.session.execute(
            query.order_by(AIInsightRun.created_at.desc()).offset((page - 1) * limit).limit(limit)
        )
        return list(result.scalars().unique()), int(total)

    def _filtered_owner_query(
        self,
        owner_id: UUID,
        target_period_type: str | None,
        status: str | None,
        start_date: date | None,
        end_date: date | None,
    ) -> Select[tuple[AIInsightRun]]:
        query = self._active_query().where(AIInsightRun.owner_id == owner_id).options(selectinload(AIInsightRun.sources))
        if target_period_type is not None:
            query = query.where(AIInsightRun.target_period_type == target_period_type)
        if status is not None:
            query = query.where(AIInsightRun.status == status)
        if start_date is not None:
            query = query.where(AIInsightRun.period_start >= start_date)
        if end_date is not None:
            query = query.where(AIInsightRun.period_end <= end_date)
        return query
