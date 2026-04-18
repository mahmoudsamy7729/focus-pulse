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
async def test_dashboard_category_breakdown_groups_top_10_plus_other(async_session) -> None:
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        DEFAULT_OWNER_ID, date(2026, 4, 15), "csv_import"
    )
    task_service = TaskService(TaskRepository(async_session), CategoryRepository(async_session))
    for index in range(12):
        await task_service.create_task(
            DEFAULT_OWNER_ID,
            daily_log,
            f"Task {index}",
            120 - index,
            f"Category {index}",
            [],
        )
    await async_session.commit()

    dashboard = await DashboardService(DashboardRepository(async_session)).get_dashboard_overview(
        DEFAULT_OWNER_ID, "day", date(2026, 4, 15)
    )

    assert len(dashboard.category_breakdown) == 11
    assert dashboard.category_breakdown[-1].label == "Other"
    assert sum(item.total_minutes for item in dashboard.category_breakdown) == dashboard.summary.total_minutes


@pytest.mark.asyncio
async def test_dashboard_category_share_values_reconcile_to_total(async_session) -> None:
    daily_log = await DailyLogService(DailyLogRepository(async_session)).get_or_create_daily_log(
        DEFAULT_OWNER_ID, date(2026, 4, 15), "csv_import"
    )
    task_service = TaskService(TaskRepository(async_session), CategoryRepository(async_session))
    await task_service.create_task(DEFAULT_OWNER_ID, daily_log, "Build", 90, "Work", [])
    await task_service.create_task(DEFAULT_OWNER_ID, daily_log, "Read", 30, "Learn", [])
    await async_session.commit()

    dashboard = await DashboardService(DashboardRepository(async_session)).get_dashboard_overview(
        DEFAULT_OWNER_ID, "day", date(2026, 4, 15)
    )

    shares = {item.label: item.share_of_total for item in dashboard.category_breakdown}
    assert shares == {"Work": 0.75, "Learn": 0.25}
