import enum
from enum import Enum
from typing import TypedDict

from google.protobuf.internal.containers import RepeatedCompositeFieldContainer

from ingestor.sensor_data_pb2 import TelemetryPoint


class AvailableSensors(Enum):
    """
    Supported sensor types in the system.
    Mapped to database values and sensor factory logic.
    """

    TRAFFIC = "traffic"
    AIR_Q = "air_quality"
    TEMP = "temperature"


class SensorType(enum.Enum):
    AIR = 0
    TEMPERATURE = 1
    TRAFFIC = 2


class SensorDataBatch(TypedDict):
    sn: str
    lat: float
    lon: float
    type: AvailableSensors
    data: RepeatedCompositeFieldContainer[TelemetryPoint]
