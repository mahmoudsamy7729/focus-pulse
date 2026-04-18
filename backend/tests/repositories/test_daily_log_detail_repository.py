from datetime import date, datetime
from uuid import uuid4

import pytest

from app.modules.daily_logs.models import DailyLog
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.notes.models import Note
from app.modules.tasks.models import Category, Task


@pytest.mark.asyncio
async def test_daily_log_repository_loads_day_detail_with_active_notes_only(async_session) -> None:
    owner_id = uuid4()
    log = DailyLog(owner_id=owner_id, log_date=date(2026, 4, 15), source="csv_import")
    category = Category(owner_id=owner_id, name="Work", normalized_name="work")
    async_session.add_all([log, category])
    await async_session.flush()
    task = Task(
        owner_id=owner_id,
        daily_log_id=log.id,
        category_id=category.id,
        title="Task",
        normalized_title="task",
        time_spent_minutes=30,
        tags=[],
        source="csv_import",
    )
    async_session.add(task)
    await async_session.flush()
    note = Note(owner_id=owner_id, task_id=task.id, content="Visible")
    deleted_note = Note(owner_id=owner_id, task_id=task.id, content="Deleted", deleted_at=datetime.utcnow())
    async_session.add_all([note, deleted_note])
    await async_session.commit()

    loaded = await DailyLogRepository(async_session).get_with_entries(owner_id, date(2026, 4, 15))

    assert loaded is not None
    assert loaded.tasks[0].note.content == "Visible"
