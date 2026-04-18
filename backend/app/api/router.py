from fastapi import APIRouter

from app.modules.imports.router import router as imports_router


api_router = APIRouter()
api_router.include_router(imports_router, prefix="/imports", tags=["imports"])
