from typing import Annotated

from fastapi import Query, Request

from app.core.security import security
from app.core.security.security import TokenType, encrypt_password, verify_password
from app.crud import user
from app.crud.user import get_user_by_id, update_user_password
from app.dto.request.change_password_dto import ChangePasswordDto
from app.exceptions.token_exceptions import TokenIncorrectException
from app.exceptions.user_exceptions import UserNotFoundException, UserPasswordNotMatchException, UserValidateException
from app.utlis.authenticate import create_jwt_tokens


async def change_password(
        change_password_data: ChangePasswordDto,
        request: Request,
):
    if change_password_data.new_password != change_password_data.new_password_confirm:
        raise UserPasswordNotMatchException()

    access_token_decoded = security.decode_token(token=change_password_data.access_token)
    if access_token_decoded["type"] != TokenType.access_token:
        raise TokenIncorrectException()

    user = await get_user_by_id(
        user_id=access_token_decoded["sub"],
        request=request,
    )
    if user is None:
        raise UserNotFoundException()

    if not verify_password(change_password_data.current_password, user.password):
        raise UserValidateException()

    await update_user_password(
        user_id=user.id,
        new_password=encrypt_password(password=change_password_data.new_password),
        request=request,
    )

    token_data = await create_jwt_tokens(
        user_id=user.id,
        acc_type=access_token_decoded["acc_type"],
        request=request,
    )

    return token_data


async def delete_user(
        access_token: Annotated[str, Query(description="Delete user")],
        request: Request
):
    access_token_decoded = security.decode_token(token=access_token)
    if access_token_decoded["type"] != TokenType.access_token:
        raise TokenIncorrectException()

    await user.delete_user(
        user_id=access_token_decoded["sub"],
        request=request,
    )
    return "User deleted"
