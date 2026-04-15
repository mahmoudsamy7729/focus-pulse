from datetime import date
from uuid import uuid4

import pytest

from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.exceptions import InvalidTaskError
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


@pytest.mark.asyncio
async def test_create_task_normalizes_category_tags_and_duration(async_session) -> None:
    owner_id = uuid4()
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        owner_id,
        date(2026, 4, 15),
    )
    service = TaskService(
        TaskRepository(async_session),
        CategoryRepository(async_session),
        NoteService(NoteRepository(async_session)),
    )

    task = await service.create_task(
        owner_id=owner_id,
        daily_log=daily_log,
        title="  Write Plan  ",
        time_spent_minutes=45,
        category_name="  Planning ",
        tags=[" Deep Work ", "deep work", "", "Docs"],
    )
    second = await service.create_task(
        owner_id=owner_id,
        daily_log=daily_log,
        title="Review",
        time_spent_minutes=30,
        category_name="planning",
    )

    assert task.normalized_title == "write plan"
    assert task.tags == ["deep work", "docs"]
    assert second.category_id == task.category_id


@pytest.mark.asyncio
async def test_create_task_rejects_empty_title_and_non_positive_duration(async_session) -> None:
    owner_id = uuid4()
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        owner_id,
        date(2026, 4, 15),
    )
    service = TaskService(TaskRepository(async_session), CategoryRepository(async_session))

    with pytest.raises(InvalidTaskError):
        await service.create_task(owner_id, daily_log, " ", 10, "Planning")

    with pytest.raises(InvalidTaskError):
        await service.create_task(owner_id, daily_log, "Plan", 0, "Planning")
