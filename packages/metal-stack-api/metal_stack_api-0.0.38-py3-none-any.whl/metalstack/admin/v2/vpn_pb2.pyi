import datetime

from buf.validate import validate_pb2 as _validate_pb2
from google.protobuf import duration_pb2 as _duration_pb2
from metalstack.api.v2 import common_pb2 as _common_pb2
from metalstack.api.v2 import vpn_pb2 as _vpn_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VPNServiceAuthKeyRequest(_message.Message):
    __slots__ = ("project", "ephemeral", "expires")
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    EPHEMERAL_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_FIELD_NUMBER: _ClassVar[int]
    project: str
    ephemeral: bool
    expires: _duration_pb2.Duration
    def __init__(self, project: _Optional[str] = ..., ephemeral: _Optional[bool] = ..., expires: _Optional[_Union[datetime.timedelta, _duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class VPNServiceAuthKeyResponse(_message.Message):
    __slots__ = ("address", "auth_key")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    AUTH_KEY_FIELD_NUMBER: _ClassVar[int]
    address: str
    auth_key: str
    def __init__(self, address: _Optional[str] = ..., auth_key: _Optional[str] = ...) -> None: ...

class VPNServiceListNodesRequest(_message.Message):
    __slots__ = ("project",)
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    project: str
    def __init__(self, project: _Optional[str] = ...) -> None: ...

class VPNServiceListNodesResponse(_message.Message):
    __slots__ = ("nodes",)
    NODES_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[_vpn_pb2.VPNNode]
    def __init__(self, nodes: _Optional[_Iterable[_Union[_vpn_pb2.VPNNode, _Mapping]]] = ...) -> None: ...
