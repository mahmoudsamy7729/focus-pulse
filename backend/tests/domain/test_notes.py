from datetime import date
from uuid import uuid4

import pytest

from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.notes.exceptions import ActiveNoteExistsError
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


@pytest.mark.asyncio
async def test_empty_note_input_does_not_create_note(async_session) -> None:
    owner_id = uuid4()
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        owner_id,
        date(2026, 4, 15),
    )
    note_service = NoteService(NoteRepository(async_session))
    task = await TaskService(TaskRepository(async_session), CategoryRepository(async_session)).create_task(
        owner_id,
        daily_log,
        "Plan",
        25,
        "Planning",
    )

    note = await note_service.create_note(owner_id, task.id, "   ")

    assert note is None


@pytest.mark.asyncio
async def test_only_one_active_note_per_task(async_session) -> None:
    owner_id = uuid4()
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        owner_id,
        date(2026, 4, 15),
    )
    note_service = NoteService(NoteRepository(async_session))
    task = await TaskService(TaskRepository(async_session), CategoryRepository(async_session)).create_task(
        owner_id,
        daily_log,
        "Plan",
        25,
        "Planning",
    )

    created = await note_service.create_note(owner_id, task.id, "First note")

    assert created is not None
    with pytest.raises(ActiveNoteExistsError):
        await note_service.create_note(owner_id, task.id, "Second note")
