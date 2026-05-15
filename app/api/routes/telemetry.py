from fastapi import APIRouter
from ...schemas.telemetry import TelemetryRequest
from ...services.telemetry_service import create_telemetry

router = APIRouter()

@router.post("/")
async def ingest(data: TelemetryRequest):
    return await create_telemetry(data)