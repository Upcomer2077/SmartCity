from datetime import datetime
from random import choice, random

from common.types import SensorBufferType
from common.types.enums import SensorEnum, VehicleType
from sensorAPI.sensors.baseSensor import BaseSensor


class TrafficSensor(BaseSensor):
    __slots__ = ()

    def __init__(self, sensor_id, location):
        super().__init__(sensor_id, location, type=SensorEnum.TRAFFIC)

    def _generate_sensor_data(self):
        return (
            SensorBufferType(
                {
                    "sensor_id": self.sensor_id,
                    "value": choice(
                        [VehicleType.CAR, VehicleType.TRUCK, VehicleType.BUS]
                    ).value,
                    "ts": datetime.now().timestamp(),
                }
            )
            if random() > 0.2
            else None
        )
