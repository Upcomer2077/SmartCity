from common.types.enums import AvailableSensors

from emitter.sensors.air_quality.air_sensor import AirSensor
from emitter.sensors.temperature.temperature_sensor import TemperatureSensor
from emitter.sensors.traffic.traffic_sensor import TrafficSensor


def get_sensor_type(sensor_type: AvailableSensors):
    """
    Factory mapping for sensor class instantiation.

    :param sensor_type: Enum value representing the sensor category.
    :return: Concrete sensor class reference.
    """
    match sensor_type:
        case AvailableSensors.AIR_Q:
            return AirSensor
        case AvailableSensors.TEMP:
            return TemperatureSensor
        case AvailableSensors.TRAFFIC:
            return TrafficSensor
