from typing import Required, TypedDict

from sqlalchemy import UUID

from common.types.enums import AvailableSensors


class SensorBufferType(TypedDict):
    """
    Standardized dictionary for sensor measurement buffering.
    Matches the schema for bulk database insertion.
    """

    ts: Required[float]
    value: Required[float]
    sensor_sn: Required[UUID]


class _TelemetryPoint(TypedDict):
    ts: float
    value: float
    _rowid: int
    _created_at: float


class SensorDataBatch(TypedDict):
    sn: str
    lat: float
    lon: float
    type: AvailableSensors
    data: list[_TelemetryPoint]
