class SensorRegistry:
    _registry = {}

    @classmethod
    def register(cls, sensor_type, payload_class):
        cls._registry[sensor_type] = payload_class

    @classmethod
    def get_class(cls, sensor_type):
        return cls._registry.get(sensor_type)