from typing import Required, TypedDict

from sqlalchemy import UUID


class SensorBufferType(TypedDict):
    """
    Standardized dictionary for sensor measurement buffering.
    Matches the schema for bulk database insertion.
    """

    ts: Required[float]
    value: Required[float]
    sensor_sn: Required[UUID]
