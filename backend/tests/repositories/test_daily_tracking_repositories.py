from datetime import date
from uuid import uuid4

import pytest

from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.notes.repositories.note_repository import NoteRepository
from app.modules.notes.services.note_service import NoteService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


@pytest.mark.asyncio
async def test_daily_tracking_repositories_persist_relationships(async_session) -> None:
    owner_id = uuid4()
    daily_repo = DailyLogRepository(async_session)
    daily_log = await DailyLogService(daily_repo).get_or_create_daily_log(owner_id, date(2026, 4, 15))
    note_service = NoteService(NoteRepository(async_session))
    task_service = TaskService(TaskRepository(async_session), CategoryRepository(async_session), note_service)

    task = await task_service.create_task(
        owner_id,
        daily_log,
        "Write tests",
        40,
        "Engineering",
        ["Tests"],
        "Covered service behavior",
    )
    await async_session.commit()

    loaded = await daily_repo.get_with_entries(owner_id, date(2026, 4, 15))
    assert loaded is not None
    assert loaded.tasks[0].id == task.id
    assert loaded.tasks[0].category.normalized_name == "engineering"
    assert loaded.tasks[0].note.content == "Covered service behavior"
