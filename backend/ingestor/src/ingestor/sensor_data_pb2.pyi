from collections.abc import Iterable as _Iterable
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf.internal import containers as _containers

DESCRIPTOR: _descriptor.FileDescriptor

class TelemetryPoint(_message.Message):
    __slots__ = ("ts", "value")
    TS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ts: float
    value: float
    def __init__(self, ts: float | None = ..., value: float | None = ...) -> None: ...

class DeviceDataBatch(_message.Message):
    __slots__ = ("data", "lat", "lon", "sensor_sn", "type")
    SENSOR_SN_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    sensor_sn: str
    type: str
    lat: float
    lon: float
    data: _containers.RepeatedCompositeFieldContainer[TelemetryPoint]
    def __init__(
        self,
        sensor_sn: str | None = ...,
        type: str | None = ...,
        lat: float | None = ...,
        lon: float | None = ...,
        data: _Iterable[TelemetryPoint | _Mapping] | None = ...,
    ) -> None: ...

class BulkIngestionPayload(_message.Message):
    __slots__ = ("batches",)
    BATCHES_FIELD_NUMBER: _ClassVar[int]
    batches: _containers.RepeatedCompositeFieldContainer[DeviceDataBatch]
    def __init__(
        self, batches: _Iterable[DeviceDataBatch | _Mapping] | None = ...
    ) -> None: ...
