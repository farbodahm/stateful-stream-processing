# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model/twitter.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13model/twitter.proto\x12\x07twitter\x1a\x1fgoogle/protobuf/timestamp.proto\"d\n\x05Tweet\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x0c\n\x04text\x18\x03 \x01(\t\x12\x30\n\x0ctweeted_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\xc0\x01\n\x04User\x12\n\n\x02id\x18\x01 \x01(\t\x12\x12\n\nfirst_name\x18\x02 \x01(\t\x12\x11\n\tlast_name\x18\x03 \x01(\t\x12\r\n\x05\x65mail\x18\x04 \x01(\t\x12$\n\x06gender\x18\x05 \x01(\x0e\x32\x14.twitter.User.Gender\x12\x30\n\x0c\x63reated_date\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"\x1e\n\x06Gender\x12\n\n\x06\x46\x45MALE\x10\x00\x12\x08\n\x04MALE\x10\x01\"j\n\tTweetLike\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08tweet_id\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12.\n\nliked_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"z\n\x07\x43omment\x12\n\n\x02id\x18\x01 \x01(\t\x12\x10\n\x08tweet_id\x18\x02 \x01(\t\x12\x0f\n\x07user_id\x18\x03 \x01(\t\x12\x0c\n\x04text\x18\x04 \x01(\t\x12\x32\n\x0e\x63ommented_date\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"u\n\nUserFollow\x12\n\n\x02id\x18\x01 \x01(\t\x12\x13\n\x0b\x66ollowed_id\x18\x02 \x01(\t\x12\x13\n\x0b\x66ollower_id\x18\x03 \x01(\t\x12\x31\n\rfollowed_date\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.Timestampb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'model.twitter_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_TWEET']._serialized_start=65
  _globals['_TWEET']._serialized_end=165
  _globals['_USER']._serialized_start=168
  _globals['_USER']._serialized_end=360
  _globals['_USER_GENDER']._serialized_start=330
  _globals['_USER_GENDER']._serialized_end=360
  _globals['_TWEETLIKE']._serialized_start=362
  _globals['_TWEETLIKE']._serialized_end=468
  _globals['_COMMENT']._serialized_start=470
  _globals['_COMMENT']._serialized_end=592
  _globals['_USERFOLLOW']._serialized_start=594
  _globals['_USERFOLLOW']._serialized_end=711
# @@protoc_insertion_point(module_scope)
