from fastapi import APIRouter
from .routes import telemetry, sensor, stats

api_router = APIRouter()
api_router.include_router(telemetry.router, prefix="/telemetry", tags=["Telemetry"])
api_router.include_router(sensor.router, prefix="/sensors", tags=["Sensors"])
api_router.include_router(stats.router, prefix="/stats", tags=["Stats"])