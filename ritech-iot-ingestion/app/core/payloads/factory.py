from .humidity import HumidityPayload
from .pressure import PressurePayload
from .temperature import TemperaturePayload
from .registry import SensorRegistry

SensorRegistry.register("temperature", TemperaturePayload)
SensorRegistry.register("humidity", HumidityPayload)
SensorRegistry.register("pressure", PressurePayload)

class TelemetryFactory:

    @staticmethod
    def create(sensor_type, device_id, value):

        payload_class = SensorRegistry.get_class(sensor_type)

        if payload_class is None:
            return None

        print("sensor_type:", sensor_type)
        print("class:", payload_class)

        return payload_class(device_id, value, sensor_type)