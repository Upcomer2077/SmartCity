from typing import TypedDict


class SensorDTO(TypedDict):
    ts: float
    sensor_id: str
    value: str
