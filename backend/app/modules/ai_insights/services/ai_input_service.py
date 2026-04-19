from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date, timedelta
from uuid import UUID

from app.modules.ai_insights.constants import AIInsightTargetPeriod
from app.modules.ai_insights.exceptions import InvalidAIInsightTargetPeriodError
from app.modules.ai_insights.schemas import (
    AnalysisInputSummary,
    DailyMinuteTotal,
    NamedMinuteTotal,
    PreparedAIInput,
    StructuredAIInput,
    StructuredTaskInput,
)
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository


class AIInputService:
    def __init__(self, daily_log_repository: DailyLogRepository) -> None:
        self.daily_log_repository = daily_log_repository

    def resolve_period(self, period_granularity: str, anchor_date: date) -> tuple[date, date]:
        if period_granularity == AIInsightTargetPeriod.DAILY.value:
            return anchor_date, anchor_date
        if period_granularity == AIInsightTargetPeriod.WEEKLY.value:
            start = anchor_date - timedelta(days=anchor_date.weekday())
            return start, start + timedelta(days=6)
        raise InvalidAIInsightTargetPeriodError("period_granularity must be daily or weekly")

    async def prepare_input(
        self,
        owner_id: UUID,
        period_granularity: str,
        anchor_date: date,
        instruction_name: str,
        instruction_version: str,
    ) -> PreparedAIInput:
        period_start, period_end = self.resolve_period(period_granularity, anchor_date)
        daily_logs = await self.daily_log_repository.list_by_range(owner_id, period_start, period_end)
        tasks: list[StructuredTaskInput] = []
        source_daily_log_ids = []

        for daily_log in daily_logs:
            active_tasks = [task for task in daily_log.tasks if task.deleted_at is None]
            if active_tasks:
                source_daily_log_ids.append(daily_log.id)
            for task in active_tasks:
                tasks.append(
                    StructuredTaskInput(
                        task_id=task.id,
                        daily_log_id=daily_log.id,
                        date=daily_log.log_date,
                        title=task.title,
                        minutes=task.time_spent_minutes,
                        category=task.category.name,
                        tags=list(task.tags or []),
                    )
                )

        summary = self._build_summary(period_granularity, period_start, period_end, source_daily_log_ids, tasks)
        provider_input = StructuredAIInput(
            period_granularity=period_granularity,  # type: ignore[arg-type]
            period_start=period_start,
            period_end=period_end,
            tasks=tasks,
            aggregates=summary,
            instruction_name=instruction_name,
            instruction_version=instruction_version,
        )
        return PreparedAIInput(
            provider_input=provider_input,
            source_summary=summary,
            source_daily_log_ids=source_daily_log_ids,
        )

    def _build_summary(
        self,
        period_granularity: str,
        period_start: date,
        period_end: date,
        source_daily_log_ids: list[UUID],
        tasks: list[StructuredTaskInput],
    ) -> AnalysisInputSummary:
        _ = period_granularity
        category_minutes: defaultdict[str, int] = defaultdict(int)
        tag_minutes: defaultdict[str, int] = defaultdict(int)
        daily_minutes: Counter[date] = Counter()

        for task in tasks:
            category_minutes[task.category] += task.minutes
            daily_minutes[task.date] += task.minutes
            for tag in task.tags:
                tag_minutes[tag] += task.minutes

        daily_totals = [
            DailyMinuteTotal(date=period_start + timedelta(days=offset), total_minutes=daily_minutes[period_start + timedelta(days=offset)])
            for offset in range((period_end - period_start).days + 1)
        ]
        return AnalysisInputSummary(
            period_granularity=period_granularity,
            period_start=period_start,
            period_end=period_end,
            source_daily_log_ids=source_daily_log_ids,
            daily_log_count=len(source_daily_log_ids),
            task_count=len(tasks),
            total_minutes=sum(task.minutes for task in tasks),
            category_totals=[
                NamedMinuteTotal(label=label, total_minutes=minutes)
                for label, minutes in sorted(category_minutes.items(), key=lambda item: (-item[1], item[0]))
            ],
            tag_totals=[
                NamedMinuteTotal(label=label, total_minutes=minutes)
                for label, minutes in sorted(tag_minutes.items(), key=lambda item: (-item[1], item[0]))
            ],
            daily_totals=daily_totals,
        )
