from typing import TypedDict


class CoordsType(TypedDict):
    lon: float
    lat: float


class SensorBufferType(TypedDict):
    ts: float
    value: float | str
    sensor_id: str
