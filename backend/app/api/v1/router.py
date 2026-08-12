from fastapi import APIRouter

from app.api.v1.endpoints import health

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(health.router)
