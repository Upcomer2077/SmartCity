import pytest
from common.types.enums import AvailableSensors
from emitter.sensors.air_quality.air_sensor import AirSensor
from emitter.sensors.temperature.temperature_sensor import TemperatureSensor
from emitter.sensors.traffic.traffic_sensor import TrafficSensor
from emitter.utils.get_sensor_type import get_sensor_type


class TestGetSensorType:
    @pytest.mark.parametrize(
        "sensor_type, expected_class",
        [
            (AvailableSensors.AIR_Q, AirSensor),
            (AvailableSensors.TEMP, TemperatureSensor),
            (AvailableSensors.TRAFFIC, TrafficSensor),
        ],
    )
    def test_get_sensor_type_valid(self, sensor_type, expected_class):
        assert get_sensor_type(sensor_type) is expected_class

    def test_get_sensor_type_invalid(self):

        with pytest.raises(ValueError):
            # DON'T remove ignore directive
            assert get_sensor_type(sensor_type="Error") is None  # type: ignore
