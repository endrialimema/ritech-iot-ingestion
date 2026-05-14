from abc import ABC, abstractmethod


class BaseTelemetryPayload(ABC):

    def __init__(self, device_id: str, value: float, sensor_type: str):
        self._device_id = device_id
        self._value = value
        self._sensor_type = sensor_type
    
    
    @abstractmethod
    def validate(self) -> bool:
        pass

    def get_device_id(self):
        return self._device_id

    def get_value(self):
        return self._value
    
    def get_sensor_type(self):
        return self._sensor_type