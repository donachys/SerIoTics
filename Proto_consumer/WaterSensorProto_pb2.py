# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: WaterSensorProto.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='WaterSensorProto.proto',
  package='com.SerIoTics.data_generation',
  serialized_pb=_b('\n\x16WaterSensorProto.proto\x12\x1d\x63om.SerIoTics.data_generation\"\xfe\x01\n\x0bWaterSensor\x12\x0f\n\x07minType\x18\x01 \x01(\t\x12\x0f\n\x07majType\x18\x02 \x01(\t\x12\x13\n\x0bitem_sensed\x18\x03 \x01(\t\x12\x18\n\x10subject_measured\x18\x04 \x01(\t\x12\x1c\n\x14sensor_location_name\x18\x05 \x01(\t\x12\x11\n\tunique_id\x18\x06 \x01(\x03\x12\x0f\n\x07runtime\x18\x07 \x01(\x03\x12\x10\n\x08quantity\x18\x08 \x01(\x02\x12\x16\n\x0emajor_area_num\x18\t \x01(\x05\x12\x16\n\x0eminor_area_num\x18\n \x01(\x05\x12\x1a\n\x12time_since_turn_on\x18\x0b \x01(\x05\x42-\n\x1d\x63om.SerIoTics.data_generationB\x0cSensorProtos')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_WATERSENSOR = _descriptor.Descriptor(
  name='WaterSensor',
  full_name='com.SerIoTics.data_generation.WaterSensor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='minType', full_name='com.SerIoTics.data_generation.WaterSensor.minType', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='majType', full_name='com.SerIoTics.data_generation.WaterSensor.majType', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='item_sensed', full_name='com.SerIoTics.data_generation.WaterSensor.item_sensed', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='subject_measured', full_name='com.SerIoTics.data_generation.WaterSensor.subject_measured', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='sensor_location_name', full_name='com.SerIoTics.data_generation.WaterSensor.sensor_location_name', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='unique_id', full_name='com.SerIoTics.data_generation.WaterSensor.unique_id', index=5,
      number=6, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='runtime', full_name='com.SerIoTics.data_generation.WaterSensor.runtime', index=6,
      number=7, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='quantity', full_name='com.SerIoTics.data_generation.WaterSensor.quantity', index=7,
      number=8, type=2, cpp_type=6, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='major_area_num', full_name='com.SerIoTics.data_generation.WaterSensor.major_area_num', index=8,
      number=9, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='minor_area_num', full_name='com.SerIoTics.data_generation.WaterSensor.minor_area_num', index=9,
      number=10, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='time_since_turn_on', full_name='com.SerIoTics.data_generation.WaterSensor.time_since_turn_on', index=10,
      number=11, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=58,
  serialized_end=312,
)

DESCRIPTOR.message_types_by_name['WaterSensor'] = _WATERSENSOR

WaterSensor = _reflection.GeneratedProtocolMessageType('WaterSensor', (_message.Message,), dict(
  DESCRIPTOR = _WATERSENSOR,
  __module__ = 'WaterSensorProto_pb2'
  # @@protoc_insertion_point(class_scope:com.SerIoTics.data_generation.WaterSensor)
  ))
_sym_db.RegisterMessage(WaterSensor)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('\n\035com.SerIoTics.data_generationB\014SensorProtos'))
# @@protoc_insertion_point(module_scope)
