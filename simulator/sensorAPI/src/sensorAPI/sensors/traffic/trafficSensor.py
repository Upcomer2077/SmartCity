from datetime import datetime
from random import choice, random

from common.types import SensorBufferType
from common.types.enums import VehicleType
from sensorapi.sensors.baseSensor import BaseSensor


class TrafficSensor(BaseSensor):
    __slots__ = ()

    def _generate_sensor_data(self):
        return (
            SensorBufferType(
                {
                    "sensor_id": self.sensor_id,
                    "value": choice([*VehicleType]).value,
                    "ts": datetime.now().timestamp(),
                }
            )
            if random() > 0.2
            else None
        )
