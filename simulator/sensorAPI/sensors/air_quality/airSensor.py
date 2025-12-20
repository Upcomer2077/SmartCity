from datetime import datetime
from random import randint, random

from common.types import SensorBufferType
from common.types.enums import SensorEnum
from sensorAPI.sensors.baseSensor import BaseSensor


class AirSensor(BaseSensor):
    __slots__ = ()

    def __init__(self, sensor_id, location):
        super().__init__(sensor_id, location, type=SensorEnum.AIR_Q)

    def _generate_sensor_data(self):
        return (
            SensorBufferType(
                {
                    "sensor_id": self.sensor_id,
                    "value": randint(60, 80),
                    "ts": datetime.now().timestamp(),
                }
            )
            if random() > 0.2
            else None
        )
