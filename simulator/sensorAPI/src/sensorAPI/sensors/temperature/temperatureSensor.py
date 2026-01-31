from datetime import datetime
from random import randint, random

from common.types import SensorBufferType
from sensorapi.sensors.baseSensor import BaseSensor


class TemperatureSensor(BaseSensor):
    __slots__ = ()

    def _generate_sensor_data(self):
        return (
            SensorBufferType(
                {
                    "ts": datetime.now().timestamp(),
                    "value": randint(20, 30),
                    "sensor_id": self.sensor_id,
                }
            )
            if random() > 0.2
            else None
        )
