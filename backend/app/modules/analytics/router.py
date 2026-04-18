from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import CurrentOwner, require_scope
from app.modules.analytics.dependencies import get_dashboard_service
from app.modules.analytics.services.dashboard_service import DashboardService
from app.shared.schemas.responses import success_response

router = APIRouter()


@router.get("/dashboard")
async def get_dashboard_overview(
    owner: Annotated[CurrentOwner, Depends(require_scope("analytics:read"))],
    service: Annotated[DashboardService, Depends(get_dashboard_service)],
    period_type: Annotated[str, Query()] = "day",
    anchor_date: Annotated[date | None, Query()] = None,
) -> dict[str, object]:
    dashboard = await service.get_dashboard_overview(owner.owner_id, period_type, anchor_date)
    return success_response(dashboard.model_dump(mode="json"))
