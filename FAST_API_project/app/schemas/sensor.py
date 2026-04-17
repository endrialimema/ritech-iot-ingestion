from pydantic import BaseModel
from typing import Optional


class SensorCreate(BaseModel):
    sensor_id: str
    name: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None


class SensorResponse(BaseModel):
    sensor_id: str
    name: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    active: bool = True