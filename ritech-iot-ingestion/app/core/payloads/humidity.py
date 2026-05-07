from .base import BaseTelemetryPayload


class HumidityPayload(BaseTelemetryPayload):

    def __init__(self, device_id, value, sensor_type="humidity"):
        super().__init__(device_id, value, sensor_type)
        self._history = {}

    def validate(self) -> bool:
        return 0 <= self._value <= 100
    
    def normalize(self):
        scaled = self._value / 100

        device = self.get_device_id()

        if device not in self._history:
            self._history[device] = []
         
        # store history
        history = self._history[device]
        history.append(scaled)
 
        if len(history) == 1:
            return scaled

        # keep last 5 values only
        return sum(history) / len(history)