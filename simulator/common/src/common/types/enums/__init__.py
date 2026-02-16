from enum import Enum


class VehicleType(Enum):
    CAR = 0
    TRUCK = 1
    BUS = 2


class AvailableSensors(Enum):
    TRAFFIC = "traffic"
    AIR_Q = "air_quality"
    TEMP = "temperature"
