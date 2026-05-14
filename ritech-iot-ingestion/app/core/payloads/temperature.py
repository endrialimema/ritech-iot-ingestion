from .base import BaseTelemetryPayload
from app.core import cpp_normalizer


class TemperaturePayload(BaseTelemetryPayload):

    # shared C++ instance (IMPORTANT)
    _norm = cpp_normalizer.Normalizer()

    def __init__(self, device_id, value, sensor_type="temperature"):
        super().__init__(device_id, value, sensor_type)

    def validate(self) -> bool:
        return -50 <= self._value <= 150

    def normalize(self):
        return self._norm.normalize_temperature(
            self._value,
            self.get_device_id()
        )