from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VerifyEmailRequest(_message.Message):
    __slots__ = ("user_email", "verify_token")
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    VERIFY_TOKEN_FIELD_NUMBER: _ClassVar[int]
    user_email: str
    verify_token: str
    def __init__(self, user_email: _Optional[str] = ..., verify_token: _Optional[str] = ...) -> None: ...

class VerifyEmailResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class VerifyEmailNewRequest(_message.Message):
    __slots__ = ("user_email",)
    USER_EMAIL_FIELD_NUMBER: _ClassVar[int]
    user_email: str
    def __init__(self, user_email: _Optional[str] = ...) -> None: ...

class VerifyEmailNewResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class RefreshRequest(_message.Message):
    __slots__ = ("refresh_token",)
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    refresh_token: str
    def __init__(self, refresh_token: _Optional[str] = ...) -> None: ...

class RefreshResponse(_message.Message):
    __slots__ = ("token_type", "access_token", "refresh_token")
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    token_type: str
    access_token: str
    refresh_token: str
    def __init__(self, token_type: _Optional[str] = ..., access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...

class AccessRequest(_message.Message):
    __slots__ = ("access_token",)
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    access_token: str
    def __init__(self, access_token: _Optional[str] = ...) -> None: ...

class AccessResponse(_message.Message):
    __slots__ = ("exp", "sub", "type")
    EXP_FIELD_NUMBER: _ClassVar[int]
    SUB_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    exp: int
    sub: str
    type: str
    def __init__(self, exp: _Optional[int] = ..., sub: _Optional[str] = ..., type: _Optional[str] = ...) -> None: ...

class CreateTokensRequest(_message.Message):
    __slots__ = ("user_id",)
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    def __init__(self, user_id: _Optional[str] = ...) -> None: ...

class CreateTokensResponse(_message.Message):
    __slots__ = ("token_type", "access_token", "refresh_token")
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    REFRESH_TOKEN_FIELD_NUMBER: _ClassVar[int]
    token_type: str
    access_token: str
    refresh_token: str
    def __init__(self, token_type: _Optional[str] = ..., access_token: _Optional[str] = ..., refresh_token: _Optional[str] = ...) -> None: ...
