from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class STATUS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DISCONNECTED: _ClassVar[STATUS]
    IDLE: _ClassVar[STATUS]
    INIT: _ClassVar[STATUS]
    START: _ClassVar[STATUS]
    PPS_ON: _ClassVar[STATUS]
    STOP: _ClassVar[STATUS]
    DONE: _ClassVar[STATUS]
    ERROR: _ClassVar[STATUS]
    BLOCKED: _ClassVar[STATUS]

class ERRNO(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_ERROR: _ClassVar[ERRNO]
    NOT_CONNECTED: _ClassVar[ERRNO]
    BUSY: _ClassVar[ERRNO]
    FAIL_KEEP_ALIVE: _ClassVar[ERRNO]
    FAIL_REG_SERVICE: _ClassVar[ERRNO]
    UNINTENDED_ERROR: _ClassVar[ERRNO]
DISCONNECTED: STATUS
IDLE: STATUS
INIT: STATUS
START: STATUS
PPS_ON: STATUS
STOP: STATUS
DONE: STATUS
ERROR: STATUS
BLOCKED: STATUS
NO_ERROR: ERRNO
NOT_CONNECTED: ERRNO
BUSY: ERRNO
FAIL_KEEP_ALIVE: ERRNO
FAIL_REG_SERVICE: ERRNO
UNINTENDED_ERROR: ERRNO

class BasicReq(_message.Message):
    __slots__ = ("uid",)
    UID_FIELD_NUMBER: _ClassVar[int]
    uid: str
    def __init__(self, uid: _Optional[str] = ...) -> None: ...

class DoneReq(_message.Message):
    __slots__ = ("uid", "result")
    UID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    uid: str
    result: bool
    def __init__(self, uid: _Optional[str] = ..., result: bool = ...) -> None: ...

class ErrorData(_message.Message):
    __slots__ = ("msg", "errno")
    MSG_FIELD_NUMBER: _ClassVar[int]
    ERRNO_FIELD_NUMBER: _ClassVar[int]
    msg: str
    errno: int
    def __init__(self, msg: _Optional[str] = ..., errno: _Optional[int] = ...) -> None: ...

class BoolResp(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: bool
    def __init__(self, result: bool = ...) -> None: ...

class StatusResp(_message.Message):
    __slots__ = ("err", "state", "msg")
    ERR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    err: ErrorData
    state: STATUS
    msg: str
    def __init__(self, err: _Optional[_Union[ErrorData, _Mapping]] = ..., state: _Optional[_Union[STATUS, str]] = ..., msg: _Optional[str] = ...) -> None: ...
