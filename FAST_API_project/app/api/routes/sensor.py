from fastapi import APIRouter

from app.schemas.sensor import SensorCreate, SensorResponse

router = APIRouter(prefix="/sensors", tags=["Sensors"])


@router.post("/", response_model=SensorResponse)
def create_sensor(sensor: SensorCreate):
    return SensorResponse(
        sensor_id=sensor.sensor_id,
        name=sensor.name,
        location=sensor.location,
        type=sensor.type,
        active=True
    )