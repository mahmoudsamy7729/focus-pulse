from datetime import date

import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.modules.analytics.repositories.dashboard_repository import DashboardRepository
from app.modules.analytics.services.dashboard_service import DashboardService
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


async def _task(async_session, log_date: date, title: str, minutes: int, category: str, tags: list[str] | None = None):
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        DEFAULT_OWNER_ID, log_date, "csv_import"
    )
    service = TaskService(
        TaskRepository(async_session),
        CategoryRepository(async_session),
        NoteService(NoteRepository(async_session)),
    )
    return await service.create_task(DEFAULT_OWNER_ID, daily_log, title, minutes, category, tags or [])


@pytest.mark.asyncio
async def test_dashboard_defaults_to_latest_tracked_day(async_session) -> None:
    await _task(async_session, date(2026, 4, 14), "Older", 30, "Planning")
    await _task(async_session, date(2026, 4, 16), "Latest", 90, "Build")
    await async_session.commit()

    result = await DashboardService(DashboardRepository(async_session)).get_dashboard_overview(DEFAULT_OWNER_ID)

    assert result.period.anchor_date == date(2026, 4, 16)
    assert result.summary.total_minutes == 90
    assert result.daily_logs[0].date == date(2026, 4, 16)


@pytest.mark.asyncio
async def test_dashboard_resolves_monday_to_sunday_week(async_session) -> None:
    await _task(async_session, date(2026, 4, 13), "Monday", 45, "Build")
    await _task(async_session, date(2026, 4, 19), "Sunday", 15, "Build")
    await async_session.commit()

    result = await DashboardService(DashboardRepository(async_session)).get_dashboard_overview(
        DEFAULT_OWNER_ID, "week", date(2026, 4, 15)
    )

    assert result.period.start_date == date(2026, 4, 13)
    assert result.period.end_date == date(2026, 4, 19)
    assert result.summary.total_minutes == 60
    assert len(result.period_timeline) == 7
