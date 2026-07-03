from datetime import datetime
from random import randint

from common.types import SensorBufferType

from emitter.sensors import BaseSensor


class AirSensor(BaseSensor):
    __slots__ = ()

    def _emit_data(self):
        return SensorBufferType(
            {
                "sensor_sn": self.sensor_sn,
                "value": randint(60, 80),
                "ts": datetime.now().timestamp(),
            }
        )
