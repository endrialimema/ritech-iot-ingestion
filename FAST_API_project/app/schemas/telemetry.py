from pydantic import BaseModel

class TelemetryIn(BaseModel):
    sensor_id: str
    value: float