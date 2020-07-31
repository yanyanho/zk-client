# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api/prover.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from api import zeth_messages_pb2 as api_dot_zeth__messages__pb2
from api import snark_messages_pb2 as api_dot_snark__messages__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='api/prover.proto',
  package='zeth_proto',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x10\x61pi/prover.proto\x12\nzeth_proto\x1a\x1bgoogle/protobuf/empty.proto\x1a\x17\x61pi/zeth_messages.proto\x1a\x18\x61pi/snark_messages.proto2\x94\x01\n\x06Prover\x12K\n\x12GetVerificationKey\x12\x16.google.protobuf.Empty\x1a\x1b.zeth_proto.VerificationKey\"\x00\x12=\n\x05Prove\x12\x17.zeth_proto.ProofInputs\x1a\x19.zeth_proto.ExtendedProof\"\x00\x62\x06proto3')
  ,
  dependencies=[google_dot_protobuf_dot_empty__pb2.DESCRIPTOR,api_dot_zeth__messages__pb2.DESCRIPTOR,api_dot_snark__messages__pb2.DESCRIPTOR,])



_sym_db.RegisterFileDescriptor(DESCRIPTOR)



_PROVER = _descriptor.ServiceDescriptor(
  name='Prover',
  full_name='zeth_proto.Prover',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=113,
  serialized_end=261,
  methods=[
  _descriptor.MethodDescriptor(
    name='GetVerificationKey',
    full_name='zeth_proto.Prover.GetVerificationKey',
    index=0,
    containing_service=None,
    input_type=google_dot_protobuf_dot_empty__pb2._EMPTY,
    output_type=api_dot_snark__messages__pb2._VERIFICATIONKEY,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Prove',
    full_name='zeth_proto.Prover.Prove',
    index=1,
    containing_service=None,
    input_type=api_dot_zeth__messages__pb2._PROOFINPUTS,
    output_type=api_dot_snark__messages__pb2._EXTENDEDPROOF,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_PROVER)

DESCRIPTOR.services_by_name['Prover'] = _PROVER

# @@protoc_insertion_point(module_scope)
