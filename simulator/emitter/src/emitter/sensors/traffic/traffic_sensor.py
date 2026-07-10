from datetime import datetime
from random import choice

from common.types import SensorBufferType
from common.types.enums import VehicleType

from emitter.sensors import BaseSensor


class TrafficSensor(BaseSensor):
    __slots__ = ()

    def _emit_data(self):
        return SensorBufferType(
            {
                "sensor_sn": self.sensor_sn,
                "value": choice([*VehicleType]).value,
                "ts": datetime.now().timestamp(),
            }
        )
