from .base import BaseTelemetryPayload


class TemperaturePayload(BaseTelemetryPayload):

    def __init__(self, device_id, value, sensor_type="temperature"):
        super().__init__(device_id, value, sensor_type)
        self._history = {}

    def validate(self) -> bool:
        return -50 <= self._value <= 150
    
    def normalize(self):
        scaled = (self._value + 50) / 200

        device = self.get_device_id()

        if device not in self._history:
            self._history[device] = []
         
        # store history
        history = self._history[device]
        history.append(scaled)
 
        if len(history) == 1:
            return scaled


        # moving average
        return sum(history) / len(history)
