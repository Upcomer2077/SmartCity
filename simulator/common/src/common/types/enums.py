from enum import Enum


class VehicleType(Enum):
    """
    Categories of vehicles for traffic simulation.
    Used to differentiate data points in traffic sensors.
    """

    CAR = 0
    TRUCK = 1
    BUS = 2


class AvailableSensors(Enum):
    """
    Supported sensor types in the system.
    Mapped to database values and sensor factory logic.
    """

    TRAFFIC = "traffic"
    AIR_Q = "air_quality"
    TEMP = "temperature"
