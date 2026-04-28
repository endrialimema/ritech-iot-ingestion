from fastapi import APIRouter

from app.schemas.sensor import SensorCreate, SensorResponse

print("SENSOR ROUTE LOADED")

router = APIRouter(tags=["Sensors"])

@router.post("/", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate):
    return SensorResponse(
        device_id=sensor.device_id,
        name=sensor.name,
        location=sensor.location,
        type=sensor.type,
        active=True
    )
