"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 6, 31, 1, '', 'ares_struct.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11ares_struct.proto\x12\x0eares.datamodel"\x8e\x01\n\nAresStruct\x126\n\x06fields\x18\x01 \x03(\x0b2&.ares.datamodel.AresStruct.FieldsEntry\x1aH\n\x0bFieldsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12(\n\x05value\x18\x02 \x01(\x0b2\x19.ares.datamodel.AresValue:\x028\x01"\xea\x03\n\tAresValue\x12/\n\nnull_value\x18\x01 \x01(\x0e2\x19.ares.datamodel.NullValueH\x00\x12\x14\n\nbool_value\x18\x02 \x01(\x08H\x00\x12\x16\n\x0cstring_value\x18\x03 \x01(\tH\x00\x12\x16\n\x0cnumber_value\x18\x04 \x01(\x01H\x00\x12\x15\n\x0bbytes_value\x18\x05 \x01(\x0cH\x00\x129\n\x12string_array_value\x18\x06 \x01(\x0b2\x1b.ares.datamodel.StringArrayH\x00\x129\n\x12number_array_value\x18\x07 \x01(\x0b2\x1b.ares.datamodel.NumberArrayH\x00\x123\n\nlist_value\x18\x08 \x01(\x0b2\x1d.ares.datamodel.AresValueListH\x00\x122\n\x0cstruct_value\x18\t \x01(\x0b2\x1a.ares.datamodel.AresStructH\x00\x12/\n\nunit_value\x18\n \x01(\x0e2\x19.ares.datamodel.UnitValueH\x00\x127\n\x0efunction_value\x18\x0b \x01(\x0b2\x1d.ares.datamodel.FunctionValueH\x00B\x06\n\x04kind"$\n\rFunctionValue\x12\x13\n\x0bfunction_id\x18\x01 \x01(\t"\x1e\n\x0bStringArray\x12\x0f\n\x07strings\x18\x01 \x03(\t"\x1e\n\x0bNumberArray\x12\x0f\n\x07numbers\x18\x02 \x03(\x01":\n\rAresValueList\x12)\n\x06values\x18\x01 \x03(\x0b2\x19.ares.datamodel.AresValue*\x1b\n\tNullValue\x12\x0e\n\nNULL_VALUE\x10\x00*\x1b\n\tUnitValue\x12\x0e\n\nUNIT_VALUE\x10\x00b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ares_struct_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_ARESSTRUCT_FIELDSENTRY']._loaded_options = None
    _globals['_ARESSTRUCT_FIELDSENTRY']._serialized_options = b'8\x01'
    _globals['_NULLVALUE']._serialized_start = 837
    _globals['_NULLVALUE']._serialized_end = 864
    _globals['_UNITVALUE']._serialized_start = 866
    _globals['_UNITVALUE']._serialized_end = 893
    _globals['_ARESSTRUCT']._serialized_start = 38
    _globals['_ARESSTRUCT']._serialized_end = 180
    _globals['_ARESSTRUCT_FIELDSENTRY']._serialized_start = 108
    _globals['_ARESSTRUCT_FIELDSENTRY']._serialized_end = 180
    _globals['_ARESVALUE']._serialized_start = 183
    _globals['_ARESVALUE']._serialized_end = 673
    _globals['_FUNCTIONVALUE']._serialized_start = 675
    _globals['_FUNCTIONVALUE']._serialized_end = 711
    _globals['_STRINGARRAY']._serialized_start = 713
    _globals['_STRINGARRAY']._serialized_end = 743
    _globals['_NUMBERARRAY']._serialized_start = 745
    _globals['_NUMBERARRAY']._serialized_end = 775
    _globals['_ARESVALUELIST']._serialized_start = 777
    _globals['_ARESVALUELIST']._serialized_end = 835