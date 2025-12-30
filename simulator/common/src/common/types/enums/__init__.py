from enum import Enum


class VehicleType(Enum):
    CAR = "car"
    TRUCK = "truck"
    BUS = "bus"


class SensorEnum(str, Enum):
    TRAFFIC = "traffic"
    AIR_Q = "air_quality"
    TEMP = "temperature"
