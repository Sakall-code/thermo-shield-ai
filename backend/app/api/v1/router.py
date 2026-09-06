from fastapi import APIRouter

from app.api.v1.endpoints import wards, forecast, risk, alerts, health

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(wards.router, prefix="/wards", tags=["wards"])
api_router.include_router(forecast.router, prefix="/forecast", tags=["forecast"])
api_router.include_router(risk.router, prefix="/risk", tags=["risk"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
