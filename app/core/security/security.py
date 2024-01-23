from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from uuid import UUID

import jwt
from jwt import DecodeError, ExpiredSignatureError, MissingRequiredClaimError
from passlib.context import CryptContext

from app.core.config import settings
from app.crud.refresh_token import delete_all_refresh_tokens, set_refresh_token
from app.exceptions.token_exceptions import (
    TokenDecodeException,
    TokenExpiredSignatureException,
    TokenMissingRequiredClaimException,
)
from app.models.token import Token


class TokenType(str, Enum):
    refresh_token = "refresh_token"
    access_token = "access_token"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, encrypted_password: str):
    return pwd_context.verify(password, encrypted_password)


def create_access_token(subject: str | Any) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject), "type": TokenType.access_token}

    return jwt.encode(
        payload=to_encode,
        key=settings.ENCRYPT_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def create_refresh_token(subject: str | Any) -> str:
    expire = datetime.utcnow() + timedelta(
        minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject), "type": TokenType.refresh_token}

    return jwt.encode(
        payload=to_encode,
        key=settings.ENCRYPT_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


async def create_jwt_tokens(
        user_id: UUID,
) -> Token:
    access_token = create_access_token(subject=user_id)
    refresh_token = create_refresh_token(subject=user_id)

    token_data = Token(
        token_type="bearer",
        access_token=access_token,
        refresh_token=refresh_token,
    )
    await delete_all_refresh_tokens(user_id=user_id)

    await set_refresh_token(
        user_id=user_id,
        refresh_token=token_data.refresh_token
    )

    return token_data


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(
            jwt=token,
            key=settings.ENCRYPT_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except ExpiredSignatureError as e:
        raise TokenExpiredSignatureException() from e
    except DecodeError as e:
        raise TokenDecodeException() from e
    except MissingRequiredClaimError as e:
        raise TokenMissingRequiredClaimException() from e
