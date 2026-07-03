from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TelemetryPoint(_message.Message):
    __slots__ = ("ts", "value")
    TS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ts: float
    value: float
    def __init__(self, ts: _Optional[float] = ..., value: _Optional[float] = ...) -> None: ...

class DeviceDataBatch(_message.Message):
    __slots__ = ("sensor_sn", "type", "lat", "lon", "data")
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
    def __init__(self, sensor_sn: _Optional[str] = ..., type: _Optional[str] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., data: _Optional[_Iterable[_Union[TelemetryPoint, _Mapping]]] = ...) -> None: ...

class BulkIngestionPayload(_message.Message):
    __slots__ = ("batches",)
    BATCHES_FIELD_NUMBER: _ClassVar[int]
    batches: _containers.RepeatedCompositeFieldContainer[DeviceDataBatch]
    def __init__(self, batches: _Optional[_Iterable[_Union[DeviceDataBatch, _Mapping]]] = ...) -> None: ...
