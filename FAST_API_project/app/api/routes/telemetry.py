from fastapi import APIRouter
from ...schemas.telemetry import TelemetryIn
from ...services.telemetry_service import create_telemetry

router = APIRouter()

@router.post("/")
async def ingest(data: TelemetryIn):
    return await create_telemetry(data)