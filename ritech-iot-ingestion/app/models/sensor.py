from pydantic import BaseModel
from typing import Optional


class Sensor(BaseModel):
    device_id: str
    name: Optional[str] = None
    location: Optional[str] = None
    type: Optional[str] = None
    active: bool = True
