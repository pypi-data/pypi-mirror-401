from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from typing import ClassVar as _ClassVar

DESCRIPTOR: _descriptor.FileDescriptor

class AresDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNSPECIFIED_TYPE: _ClassVar[AresDataType]
    NULL: _ClassVar[AresDataType]
    BOOLEAN: _ClassVar[AresDataType]
    STRING: _ClassVar[AresDataType]
    NUMBER: _ClassVar[AresDataType]
    STRING_ARRAY: _ClassVar[AresDataType]
    NUMBER_ARRAY: _ClassVar[AresDataType]
    LIST: _ClassVar[AresDataType]
    STRUCT: _ClassVar[AresDataType]
    BYTE_ARRAY: _ClassVar[AresDataType]
    ANY: _ClassVar[AresDataType]
    UNIT: _ClassVar[AresDataType]
UNSPECIFIED_TYPE: AresDataType
NULL: AresDataType
BOOLEAN: AresDataType
STRING: AresDataType
NUMBER: AresDataType
STRING_ARRAY: AresDataType
NUMBER_ARRAY: AresDataType
LIST: AresDataType
STRUCT: AresDataType
BYTE_ARRAY: AresDataType
ANY: AresDataType
UNIT: AresDataType
