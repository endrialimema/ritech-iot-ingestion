from pydantic import BaseModel
from datetime import datetime
from typing import List

class TelemetryRequest(BaseModel):
    device_id: str
    value: float

class TelemetryReading(BaseModel):
    ts: datetime
    value: float


class TelemetryBucket(BaseModel):
    device_id: str
    bucket_start: datetime
    bucket_end: datetime
    readings: List[TelemetryReading] = []
