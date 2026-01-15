import datetime

from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TagReadValueRequest(_message.Message):
    __slots__ = ("names",)
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...

class TagReadValueReply(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[SLValue]
    def __init__(self, values: _Optional[_Iterable[_Union[SLValue, _Mapping]]] = ...) -> None: ...

class SLValue(_message.Message):
    __slots__ = ("double_value", "string_value", "bool_value", "int32_value", "int64_value", "uint32_value", "uint64_value", "time_value")
    DOUBLE_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALUE_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUE_FIELD_NUMBER: _ClassVar[int]
    TIME_VALUE_FIELD_NUMBER: _ClassVar[int]
    double_value: float
    string_value: str
    bool_value: bool
    int32_value: int
    int64_value: int
    uint32_value: int
    uint64_value: int
    time_value: _timestamp_pb2.Timestamp
    def __init__(self, double_value: _Optional[float] = ..., string_value: _Optional[str] = ..., bool_value: bool = ..., int32_value: _Optional[int] = ..., int64_value: _Optional[int] = ..., uint32_value: _Optional[int] = ..., uint64_value: _Optional[int] = ..., time_value: _Optional[_Union[datetime.datetime, _timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class TagWriteValueRequest(_message.Message):
    __slots__ = ("wvs",)
    WVS_FIELD_NUMBER: _ClassVar[int]
    wvs: _containers.RepeatedCompositeFieldContainer[WriteValue]
    def __init__(self, wvs: _Optional[_Iterable[_Union[WriteValue, _Mapping]]] = ...) -> None: ...

class WriteValue(_message.Message):
    __slots__ = ("tag_name", "value", "quality")
    TAG_NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    QUALITY_FIELD_NUMBER: _ClassVar[int]
    tag_name: str
    value: SLValue
    quality: int
    def __init__(self, tag_name: _Optional[str] = ..., value: _Optional[_Union[SLValue, _Mapping]] = ..., quality: _Optional[int] = ...) -> None: ...

class TagWriteValueReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...
