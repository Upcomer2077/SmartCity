from datetime import datetime
from random import randint

from common.types import SensorBufferType

from emitter.sensors import BaseSensor


class TemperatureSensor(BaseSensor):
    __slots__ = ()

    def _emit_data(self):
        return SensorBufferType(
            {
                "ts": datetime.now().timestamp(),
                "value": randint(20, 30),
                "sensor_sn": self.sensor_sn,
            }
        )
