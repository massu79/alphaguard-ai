from fastapi import APIRouter

from app.api.v1.endpoints import analysis, backtests, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(backtests.router, prefix="/backtests", tags=["backtests"])
