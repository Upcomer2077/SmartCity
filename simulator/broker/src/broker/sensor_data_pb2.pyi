from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorDTO(_message.Message):
    __slots__ = ("ts", "sensor_sn", "value")
    TS_FIELD_NUMBER: _ClassVar[int]
    SENSOR_SN_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    ts: float
    sensor_sn: str
    value: float
    def __init__(self, ts: _Optional[float] = ..., sensor_sn: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...

class SensorBatch(_message.Message):
    __slots__ = ("records",)
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    records: _containers.RepeatedCompositeFieldContainer[SensorDTO]
    def __init__(self, records: _Optional[_Iterable[_Union[SensorDTO, _Mapping]]] = ...) -> None: ...
