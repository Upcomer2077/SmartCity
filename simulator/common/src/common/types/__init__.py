from typing import TypedDict

from sqlalchemy import UUID


class CoordsType(TypedDict):
    lon: float
    lat: float


class SensorBufferType(TypedDict):
    ts: float
    value: float
    sensor_sn: UUID
