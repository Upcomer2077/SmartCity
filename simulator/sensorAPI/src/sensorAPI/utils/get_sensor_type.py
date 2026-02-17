from common.types.enums import AvailableSensors
from sensorapi.sensors.air_quality.airSensor import AirSensor
from sensorapi.sensors.temperature.temperatureSensor import TemperatureSensor
from sensorapi.sensors.traffic.trafficSensor import TrafficSensor


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
