from datetime import datetime
from random import randint, random

from common.types import SensorBufferType
from sensorapi.sensors.baseSensor import BaseSensor


class AirSensor(BaseSensor):
    __slots__ = ()

    def _generate_sensor_data(self):
        return (
            SensorBufferType(
                {
                    "sensor_sn": self.sensor_sn,
                    "value": randint(60, 80),
                    "ts": datetime.now().timestamp(),
                }
            )
            if random() > 0.2
            else None
        )
