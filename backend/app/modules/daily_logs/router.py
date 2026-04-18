from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import CurrentOwner, require_scope
from app.modules.daily_logs.dependencies import get_daily_log_service
from app.modules.daily_logs.services.daily_log_service import DailyLogService
from app.shared.schemas.responses import success_response


router = APIRouter()


@router.get("/{log_date}")
async def get_day_detail(
    owner: Annotated[CurrentOwner, Depends(require_scope("daily_logs:read"))],
    service: Annotated[DailyLogService, Depends(get_daily_log_service)],
    log_date: date,
) -> dict[str, object]:
    detail = await service.get_day_detail(owner.owner_id, log_date)
    return success_response(detail.model_dump(mode="json"))
