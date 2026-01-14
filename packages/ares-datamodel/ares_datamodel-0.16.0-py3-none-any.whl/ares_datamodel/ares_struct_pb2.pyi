from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NullValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NULL_VALUE: _ClassVar[NullValue]

class UnitValue(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNIT_VALUE: _ClassVar[UnitValue]
NULL_VALUE: NullValue
UNIT_VALUE: UnitValue

class AresStruct(_message.Message):
    __slots__ = ("fields",)
    class FieldsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: AresValue
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[AresValue, _Mapping]] = ...) -> None: ...
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    fields: _containers.MessageMap[str, AresValue]
    def __init__(self, fields: _Optional[_Mapping[str, AresValue]] = ...) -> None: ...

class AresValue(_message.Message):
    __slots__ = ("null_value", "bool_value", "string_value", "number_value", "bytes_value", "string_array_value", "number_array_value", "list_value", "struct_value", "unit_value", "function_value")
    NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_VALUE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_VALUE_FIELD_NUMBER: _ClassVar[int]
    BYTES_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    NUMBER_ARRAY_VALUE_FIELD_NUMBER: _ClassVar[int]
    LIST_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRUCT_VALUE_FIELD_NUMBER: _ClassVar[int]
    UNIT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_VALUE_FIELD_NUMBER: _ClassVar[int]
    null_value: NullValue
    bool_value: bool
    string_value: str
    number_value: float
    bytes_value: bytes
    string_array_value: StringArray
    number_array_value: NumberArray
    list_value: AresValueList
    struct_value: AresStruct
    unit_value: UnitValue
    function_value: FunctionValue
    def __init__(self, null_value: _Optional[_Union[NullValue, str]] = ..., bool_value: bool = ..., string_value: _Optional[str] = ..., number_value: _Optional[float] = ..., bytes_value: _Optional[bytes] = ..., string_array_value: _Optional[_Union[StringArray, _Mapping]] = ..., number_array_value: _Optional[_Union[NumberArray, _Mapping]] = ..., list_value: _Optional[_Union[AresValueList, _Mapping]] = ..., struct_value: _Optional[_Union[AresStruct, _Mapping]] = ..., unit_value: _Optional[_Union[UnitValue, str]] = ..., function_value: _Optional[_Union[FunctionValue, _Mapping]] = ...) -> None: ...

class FunctionValue(_message.Message):
    __slots__ = ("function_id",)
    FUNCTION_ID_FIELD_NUMBER: _ClassVar[int]
    function_id: str
    def __init__(self, function_id: _Optional[str] = ...) -> None: ...

class StringArray(_message.Message):
    __slots__ = ("strings",)
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    strings: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, strings: _Optional[_Iterable[str]] = ...) -> None: ...

class NumberArray(_message.Message):
    __slots__ = ("numbers",)
    NUMBERS_FIELD_NUMBER: _ClassVar[int]
    numbers: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, numbers: _Optional[_Iterable[float]] = ...) -> None: ...

class AresValueList(_message.Message):
    __slots__ = ("values",)
    VALUES_FIELD_NUMBER: _ClassVar[int]
    values: _containers.RepeatedCompositeFieldContainer[AresValue]
    def __init__(self, values: _Optional[_Iterable[_Union[AresValue, _Mapping]]] = ...) -> None: ...
