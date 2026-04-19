from datetime import date
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Query, status

from app.api.dependencies import CurrentOwner, require_scope
from app.modules.ai_insights.constants import (
    AI_INSIGHT_DEFAULT_LIMIT,
    AI_INSIGHT_DEFAULT_PAGE,
    AI_INSIGHT_MAX_LIMIT,
)
from app.modules.ai_insights.dependencies import get_ai_insight_run_service
from app.modules.ai_insights.schemas import AIInsightRunCreateRequest
from app.modules.ai_insights.services.ai_insight_run_service import AIInsightRunService
from app.shared.schemas.responses import success_response


router = APIRouter()


@router.post("/runs", status_code=status.HTTP_202_ACCEPTED)
async def create_ai_insight_run(
    owner: Annotated[CurrentOwner, Depends(require_scope("ai_insights:write"))],
    service: Annotated[AIInsightRunService, Depends(get_ai_insight_run_service)],
    payload: AIInsightRunCreateRequest,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
    x_request_id: Annotated[str | None, Header(alias="X-Request-Id")] = None,
) -> dict[str, object]:
    accepted = await service.request_analysis_run(
        owner.owner_id,
        payload.period_granularity,
        payload.anchor_date,
        idempotency_key=idempotency_key,
        request_id=x_request_id,
    )
    return success_response(accepted.model_dump(mode="json"))


@router.get("/runs")
async def list_ai_insight_runs(
    owner: Annotated[CurrentOwner, Depends(require_scope("ai_insights:read"))],
    service: Annotated[AIInsightRunService, Depends(get_ai_insight_run_service)],
    page: Annotated[int, Query(ge=1)] = AI_INSIGHT_DEFAULT_PAGE,
    limit: Annotated[int, Query(ge=1, le=AI_INSIGHT_MAX_LIMIT)] = AI_INSIGHT_DEFAULT_LIMIT,
    period_granularity: Annotated[str | None, Query()] = None,
    status_filter: Annotated[str | None, Query(alias="status")] = None,
    start_date: Annotated[date | None, Query()] = None,
    end_date: Annotated[date | None, Query()] = None,
) -> dict[str, object]:
    result = await service.list_history(
        owner.owner_id,
        page=page,
        limit=limit,
        period_granularity=period_granularity,
        status=status_filter,
        start_date=start_date,
        end_date=end_date,
    )
    return success_response(result.model_dump(mode="json"))


@router.get("/runs/current")
async def get_current_ai_insight_run(
    owner: Annotated[CurrentOwner, Depends(require_scope("ai_insights:read"))],
    service: Annotated[AIInsightRunService, Depends(get_ai_insight_run_service)],
    period_granularity: Annotated[str, Query()],
    anchor_date: Annotated[date, Query()],
) -> dict[str, object]:
    result = await service.get_current_result(owner.owner_id, period_granularity, anchor_date)
    return success_response(result.model_dump(mode="json"))


@router.get("/runs/{ai_insight_run_id}")
async def get_ai_insight_run(
    owner: Annotated[CurrentOwner, Depends(require_scope("ai_insights:read"))],
    service: Annotated[AIInsightRunService, Depends(get_ai_insight_run_service)],
    ai_insight_run_id: UUID,
) -> dict[str, object]:
    result = await service.get_run_detail(owner.owner_id, ai_insight_run_id)
    return success_response(result.model_dump(mode="json"))


@router.post("/runs/{ai_insight_run_id}/rerun", status_code=status.HTTP_202_ACCEPTED)
async def rerun_ai_insight_run(
    owner: Annotated[CurrentOwner, Depends(require_scope("ai_insights:write"))],
    service: Annotated[AIInsightRunService, Depends(get_ai_insight_run_service)],
    ai_insight_run_id: UUID,
    idempotency_key: Annotated[str | None, Header(alias="Idempotency-Key")] = None,
) -> dict[str, object]:
    accepted = await service.request_rerun(owner.owner_id, ai_insight_run_id, idempotency_key=idempotency_key)
    return success_response(accepted.model_dump(mode="json"))
