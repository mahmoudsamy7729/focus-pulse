from datetime import date

import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


@pytest.mark.asyncio
async def test_day_detail_returns_empty_payload_for_missing_day(async_session) -> None:
    detail = await DailyLogService(DailyLogRepository(async_session)).get_day_detail(
        DEFAULT_OWNER_ID, date(2026, 4, 15)
    )

    assert detail.total_minutes == 0
    assert detail.tasks == []
    assert detail.empty_state is not None


@pytest.mark.asyncio
async def test_day_detail_orders_active_tasks_and_includes_note(async_session) -> None:
    daily_service = DailyLogService(DailyLogRepository(async_session))
    daily_log = await daily_service.get_or_create_daily_log(DEFAULT_OWNER_ID, date(2026, 4, 15), "csv_import")
    task_service = TaskService(
        TaskRepository(async_session),
        CategoryRepository(async_session),
        NoteService(NoteRepository(async_session)),
    )
    await task_service.create_task(DEFAULT_OWNER_ID, daily_log, "Plan", 30, "Work", ["deep"], "Start here")
    await task_service.create_task(DEFAULT_OWNER_ID, daily_log, "Build", 90, "Work", ["ship"])
    await async_session.commit()

    detail = await daily_service.get_day_detail(DEFAULT_OWNER_ID, date(2026, 4, 15))

    assert detail.display_total == "2h"
    assert [task.timeline_position for task in detail.tasks] == [0, 1]
    assert {task.title: task.note for task in detail.tasks}["Plan"] == "Start here"
