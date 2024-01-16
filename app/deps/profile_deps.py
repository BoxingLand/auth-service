from typing import Annotated

from fastapi import Query, Request

from app.core.security import security
from app.core.security.security import TokenType, encrypt_password, verify_password
from app.crud import user
from app.crud.user import add_role_to_user, get_user_by_id, is_user_role_exist, update_user_by_id, update_user_password
from app.dto.request.profile import AddRoleDto, ChangePasswordDto, UpdateUserDto
from app.exceptions.token_exceptions import TokenIncorrectException
from app.exceptions.user_exceptions import UserNotFoundException, UserPasswordNotMatchException, UserValidateException, \
    UserRoleExist
from app.utlis.authenticate import create_jwt_tokens


async def change_password(
        change_password_data: ChangePasswordDto,
        request: Request,
):
    if change_password_data.new_password != change_password_data.new_password_confirm:
        raise UserPasswordNotMatchException()

    access_token_decoded = security.decode_token(
        token=change_password_data.access_token)
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
        new_password=encrypt_password(
            password=change_password_data.new_password),
        request=request,
    )

    token_data = await create_jwt_tokens(
        user_id=user.id,
        request=request,
    )

    return token_data


async def add_role(
        add_role_data: AddRoleDto,
        request: Request
):
    access_token_decoded = security.decode_token(token=add_role_data.access_token)
    if access_token_decoded["type"] != TokenType.access_token:
        raise TokenIncorrectException()

    if await is_user_role_exist(user_id=access_token_decoded["sub"],
                                role=add_role_data.account_type.value,
                                request=request) is not None:
        raise UserRoleExist(role=add_role_data.account_type.value)

    await add_role_to_user(
        user_id=access_token_decoded["sub"],
        role_data=add_role_data,
        request=request
    )

    return "Role added successfully"


async def update_user(
        update_data: UpdateUserDto,
        request: Request
) -> str:
    access_token_decoded = security.decode_token(token=update_data.access_token)
    if access_token_decoded["type"] != TokenType.access_token:
        raise TokenIncorrectException()

    await update_user_by_id(
        user_id=access_token_decoded["sub"],
        update_data=update_data,
        request=request
    )

    return "User updated"


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
