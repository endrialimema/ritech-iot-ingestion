from .base import BaseTelemetryPayload


class PressurePayload(BaseTelemetryPayload):

    def __init__(self, device_id, value, sensor_type="pressure"):
        super().__init__(device_id, value, sensor_type)
        self._history = {}

    def validate(self) -> bool:
        return 300 <= self._value <= 1100
        
    def normalize(self):
        scaled = (self._value - 300) / 800

        device = self.get_device_id()

        if device not in self._history:
            self._history[device] = []
         
        # store history
        history = self._history[device]
        history.append(scaled)
 
        if len(history) == 1:
            return scaled

        # keep last 5 values only
        if len(history) > 5:
            history.pop(0)

        # moving average
        return sum(history) / len(history)
