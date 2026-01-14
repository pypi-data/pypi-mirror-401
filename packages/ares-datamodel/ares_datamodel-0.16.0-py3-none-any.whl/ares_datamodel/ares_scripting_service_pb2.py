"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(_runtime_version.Domain.PUBLIC, 6, 31, 1, '', 'ares_scripting_service.proto')
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1cares_scripting_service.proto\x12\rares.services"(\n\x16ScriptExecutionRequest\x12\x0e\n\x06script\x18\x01 \x01(\t"\'\n\x15ScriptExecutionOutput\x12\x0e\n\x06output\x18\x01 \x01(\t2v\n\x14AresScriptingService\x12^\n\rExecuteScript\x12%.ares.services.ScriptExecutionRequest\x1a$.ares.services.ScriptExecutionOutput0\x01b\x06proto3')
_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'ares_scripting_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
    DESCRIPTOR._loaded_options = None
    _globals['_SCRIPTEXECUTIONREQUEST']._serialized_start = 47
    _globals['_SCRIPTEXECUTIONREQUEST']._serialized_end = 87
    _globals['_SCRIPTEXECUTIONOUTPUT']._serialized_start = 89
    _globals['_SCRIPTEXECUTIONOUTPUT']._serialized_end = 128
    _globals['_ARESSCRIPTINGSERVICE']._serialized_start = 130
    _globals['_ARESSCRIPTINGSERVICE']._serialized_end = 248