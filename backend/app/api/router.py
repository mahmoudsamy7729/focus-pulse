from fastapi import APIRouter

from app.modules.analytics.router import router as analytics_router
from app.modules.daily_logs.router import router as daily_logs_router
from app.modules.imports.router import router as imports_router


api_router = APIRouter()
api_router.include_router(analytics_router, prefix="/analytics", tags=["analytics"])
api_router.include_router(daily_logs_router, prefix="/daily-logs", tags=["daily-logs"])
api_router.include_router(imports_router, prefix="/imports", tags=["imports"])
