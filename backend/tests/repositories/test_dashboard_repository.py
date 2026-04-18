from datetime import date
from datetime import datetime
from uuid import uuid4

import pytest

from app.modules.analytics.repositories.dashboard_repository import DashboardRepository
from app.modules.daily_logs.models import DailyLog
from app.modules.tasks.models import Category, Task


@pytest.mark.asyncio
async def test_dashboard_repository_excludes_soft_deleted_tasks(async_session) -> None:
    owner_id = uuid4()
    log = DailyLog(owner_id=owner_id, log_date=date(2026, 4, 15), source="csv_import")
    category = Category(owner_id=owner_id, name="Work", normalized_name="work")
    async_session.add_all([log, category])
    await async_session.flush()
    active = Task(
        owner_id=owner_id,
        daily_log_id=log.id,
        category_id=category.id,
        title="Active",
        normalized_title="active",
        time_spent_minutes=40,
        tags=[],
        source="csv_import",
    )
    deleted = Task(
        owner_id=owner_id,
        daily_log_id=log.id,
        category_id=category.id,
        title="Deleted",
        normalized_title="deleted",
        time_spent_minutes=20,
        tags=[],
        source="csv_import",
    )
    async_session.add_all([active, deleted])
    await async_session.flush()
    deleted.deleted_at = datetime.utcnow()
    await async_session.commit()

    rows = await DashboardRepository(async_session).list_task_rows(owner_id, date(2026, 4, 15), date(2026, 4, 15))

    assert [row.title for row in rows] == ["Active"]
    assert await DashboardRepository(async_session).latest_tracked_day(owner_id) == date(2026, 4, 15)
