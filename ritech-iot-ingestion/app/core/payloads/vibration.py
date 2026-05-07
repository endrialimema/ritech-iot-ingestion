from .base import BaseTelemetryPayload


class VibrationPayload(BaseTelemetryPayload):

    def validate(self) -> bool:
        return self._value >= 0