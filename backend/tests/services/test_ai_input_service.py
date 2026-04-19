from datetime import date
from uuid import uuid4

import pytest

from app.modules.ai_insights.services.ai_input_service import AIInputService
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


@pytest.mark.asyncio
async def test_ai_input_service_resolves_weekly_period_and_excludes_note_text(async_session) -> None:
    owner_id = uuid4()
    daily_service = DailyLogService(DailyLogRepository(async_session))
    task_service = TaskService(
        TaskRepository(async_session),
        CategoryRepository(async_session),
        NoteService(NoteRepository(async_session)),
    )
    daily_log = await daily_service.get_or_create_daily_log(owner_id, date(2026, 4, 15))
    await task_service.create_task(
        owner_id,
        daily_log,
        "Write launch plan",
        45,
        "Work",
        ["Launch"],
        note="private note should not appear",
    )

    prepared = await AIInputService(DailyLogRepository(async_session)).prepare_input(
        owner_id,
        "weekly",
        date(2026, 4, 15),
        "weekly_combined_analysis",
        "test",
    )
    serialized = prepared.model_dump_json()

    assert prepared.provider_input.period_start == date(2026, 4, 13)
    assert prepared.provider_input.period_end == date(2026, 4, 19)
    assert prepared.source_summary.total_minutes == 45
    assert "Write launch plan" in serialized
    assert "private note" not in serialized
