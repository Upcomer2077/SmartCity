from datetime import datetime
from random import randint, random

from common.types import SensorBufferType
from common.types.enums import SensorEnum
from sensorAPI.sensors.baseSensor import BaseSensor


class TemperatureSensor(BaseSensor):
    __slots__ = ()

    def __init__(self, sensor_id, location):
        super().__init__(sensor_id, location, type=SensorEnum.TEMP)

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
