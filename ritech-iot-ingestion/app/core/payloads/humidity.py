from .base import BaseTelemetryPayload
from app.core import cpp_normalizer


class HumidityPayload(BaseTelemetryPayload):

    # shared C++ instance (IMPORTANT)
    _norm = cpp_normalizer.Normalizer()

    def __init__(self, device_id, value, sensor_type="humidity"):
        super().__init__(device_id, value, sensor_type)

    def validate(self) -> bool:
        return 0 <= self._value <= 100
    
    def normalize(self):
        return self._norm.normalize_humidity(
            self._value,
            self.get_device_id()
        )
           