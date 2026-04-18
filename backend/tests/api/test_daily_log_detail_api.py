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
async def test_day_detail_api_returns_success_envelope(api_client, async_session) -> None:
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        DEFAULT_OWNER_ID, date(2026, 4, 15), "csv_import"
    )
    await TaskService(
        TaskRepository(async_session),
        CategoryRepository(async_session),
        NoteService(NoteRepository(async_session)),
    ).create_task(DEFAULT_OWNER_ID, daily_log, "Plan", 45, "Work", ["deep"], "Notes")
    await async_session.commit()

    response = await api_client.get("/api/v1/daily-logs/2026-04-15")
    body = response.json()

    assert response.status_code == 200
    assert body["success"] is True
    assert body["data"]["display_total"] == "45m"
    assert body["data"]["tasks"][0]["note"] == "Notes"


@pytest.mark.asyncio
async def test_day_detail_api_returns_empty_day_payload(api_client) -> None:
    response = await api_client.get("/api/v1/daily-logs/2026-04-16")
    body = response.json()

    assert response.status_code == 200
    assert body["data"]["task_count"] == 0
    assert body["data"]["empty_state"]["code"] == "NO_DAY_DETAIL_DATA"
