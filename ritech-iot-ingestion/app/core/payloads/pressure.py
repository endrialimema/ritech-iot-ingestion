from .base import BaseTelemetryPayload
from app.core import cpp_normalizer


class PressurePayload(BaseTelemetryPayload):

    # shared C++ instance (IMPORTANT)
    _norm = cpp_normalizer.Normalizer()

    def __init__(self, device_id, value, sensor_type="pressure"):
        super().__init__(device_id, value, sensor_type)

    def validate(self) -> bool:
        return 300 <= self._value <= 1100
        
    def normalize(self):
        return self._norm.normalize_pressure(
            self._value,
            self.get_device_id()
        )
  