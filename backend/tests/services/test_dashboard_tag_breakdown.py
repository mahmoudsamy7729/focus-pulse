from datetime import date

import pytest

from app.api.dependencies import DEFAULT_OWNER_ID
from app.modules.analytics.repositories.dashboard_repository import DashboardRepository
from app.modules.analytics.services.dashboard_service import DashboardService
from app.modules.daily_logs.repositories.daily_log_repository import DailyLogRepository
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.modules.tasks.repositories.task_repository import CategoryRepository, TaskRepository
from app.modules.tasks.services.task_service import TaskService


@pytest.mark.asyncio
async def test_dashboard_tag_breakdown_includes_untagged_and_multi_tag_notice(async_session) -> None:
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        DEFAULT_OWNER_ID, date(2026, 4, 15), "csv_import"
    )
    task_service = TaskService(TaskRepository(async_session), CategoryRepository(async_session))
    await task_service.create_task(DEFAULT_OWNER_ID, daily_log, "Tagged", 60, "Work", ["deep", "client"])
    await task_service.create_task(DEFAULT_OWNER_ID, daily_log, "No tag", 30, "Work", [])
    await async_session.commit()

    dashboard = await DashboardService(DashboardRepository(async_session)).get_dashboard_overview(
        DEFAULT_OWNER_ID, "day", date(2026, 4, 15)
    )

    labels = {item.label for item in dashboard.tag_breakdown}
    assert {"deep", "client", "untagged"}.issubset(labels)
    assert dashboard.tag_total_notice is not None


@pytest.mark.asyncio
async def test_dashboard_tag_breakdown_groups_other_bucket(async_session) -> None:
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        DEFAULT_OWNER_ID, date(2026, 4, 15), "csv_import"
    )
    task_service = TaskService(TaskRepository(async_session), CategoryRepository(async_session))
    for index in range(12):
        await task_service.create_task(DEFAULT_OWNER_ID, daily_log, f"Task {index}", 10 + index, "Work", [f"tag-{index}"])
    await async_session.commit()

    dashboard = await DashboardService(DashboardRepository(async_session)).get_dashboard_overview(
        DEFAULT_OWNER_ID, "day", date(2026, 4, 15)
    )

    assert len(dashboard.tag_breakdown) == 11
    assert dashboard.tag_breakdown[-1].label == "Other"
