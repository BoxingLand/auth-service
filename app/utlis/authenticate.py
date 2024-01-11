from uuid import UUID

from fastapi import Request

from app.core.security import security
from app.core.security.security import verify_password
from app.crud.refresh_token import delete_all_refresh_tokens, set_refresh_token
from app.crud.user import get_user_by_email, get_user_by_phone_number
from app.dto.models.token import Token
from app.dto.models.user import User
from app.dto.request.signin_dto import SigninRequestDto
from app.exceptions.user_exceptions import UserValidateException, UserNotFoundException


async def authenticate(
        signin_data: SigninRequestDto,
        request: Request,
) -> User | None:
    user: User
    if signin_data.email is not None:
        user = await get_user_by_email(email=signin_data.email, request=request)
        if user is None:
            raise UserNotFoundException()
    elif signin_data.phone_number is not None:
        user = await get_user_by_phone_number(phone_number=signin_data.phone_number, request=request)
        if user is None:
            raise UserNotFoundException()
    else:
        ...

    if not verify_password(signin_data.password, user.password):
        raise UserValidateException()

    return user


async def create_jwt_tokens(
        user_id: UUID,
        request: Request,
) -> Token:
    access_token = security.create_access_token(subject=user_id)
    refresh_token = security.create_refresh_token(subject=user_id)

    token_data = Token(
        token_type="bearer",
        access_token=access_token,
        refresh_token=refresh_token,
    )
    await delete_all_refresh_tokens(
        user_id=user_id,
        request=request,
    )

    await set_refresh_token(
        user_id=user_id,
        refresh_token=token_data.refresh_token,
        request=request,
    )

    return token_data
