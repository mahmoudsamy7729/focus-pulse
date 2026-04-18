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
async def test_dashboard_api_returns_success_envelope_and_latest_day(api_client, async_session) -> None:
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        DEFAULT_OWNER_ID, date(2026, 4, 15), "csv_import"
    )
    await TaskService(
        TaskRepository(async_session),
        CategoryRepository(async_session),
        NoteService(NoteRepository(async_session)),
    ).create_task(DEFAULT_OWNER_ID, daily_log, "Plan", 75, "Work", ["deep"])
    await async_session.commit()

    response = await api_client.get("/api/v1/analytics/dashboard")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["period"]["anchor_date"] == "2026-04-15"
    assert body["data"]["summary"]["display_total"] == "1h 15m"
