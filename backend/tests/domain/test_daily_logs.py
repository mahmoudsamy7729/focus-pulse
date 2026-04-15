from datetime import date
from uuid import uuid4

import pytest

from app.modules.daily_logs.exceptions import InvalidDailyLogRangeError
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService


@pytest.mark.asyncio
async def test_get_or_create_daily_log_reuses_active_date(async_session) -> None:
    service = DailyLogService(DailyLogRepository(async_session))
    owner_id = uuid4()

    first = await service.get_or_create_daily_log(owner_id, date(2026, 4, 15), "manual")
    second = await service.get_or_create_daily_log(owner_id, date(2026, 4, 15), "csv_import")

    assert second.id == first.id
    assert second.source == "manual"


@pytest.mark.asyncio
async def test_list_daily_logs_rejects_inverted_range(async_session) -> None:
    service = DailyLogService(DailyLogRepository(async_session))

    with pytest.raises(InvalidDailyLogRangeError):
        await service.list_daily_logs_by_range(uuid4(), date(2026, 4, 16), date(2026, 4, 15))
