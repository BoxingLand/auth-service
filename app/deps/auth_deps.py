from typing import Annotated

from fastapi import Query, Request
from loguru import logger

from app.core.security.security import encrypt_password
from app.crud.user import (
    create_user,
    get_verify_token_by_user_email,
    set_verify_token,
    user_email_exists,
    user_phone_number_exists,
    verify_user,
)
from app.dto.request.signup_dto import SignupDto
from app.exceptions.user_exceptions import (
    UserCreateException,
    UserEmailExistException,
    UserEmailNotFoundException,
    UserPhoneNumberExistException, UserPasswordNotMatchException,
)
from app.utlis.generate_verify_token import generate_verify_token
from app.utlis.send_verification_mail import send_verification_mail


async def signup(
        signup_data: SignupDto,
        request: Request,
):
    if signup_data.password != signup_data.password_confirm:
        raise UserPasswordNotMatchException()

    if await user_email_exists(email=signup_data.email, request=request) is True:
        raise UserEmailExistException(email=signup_data.email)

    if await user_phone_number_exists(phone_number=signup_data.phone_number, request=request) is True:
        raise UserPhoneNumberExistException(phone_number=signup_data.phone_number)


    signup_data.password = encrypt_password(password=signup_data.password)
    user_id = await create_user(signup_data=signup_data, request=request)

    if user_id is None:
        raise UserCreateException()
    verification_token = await generate_verify_token()

    is_set_verify_token = await set_verify_token(
        email=signup_data.email,
        verify_token=verification_token,
        request=request
    )

    if is_set_verify_token is False:
        raise UserEmailNotFoundException(email=signup_data.email)

    await send_verification_mail(
        email=signup_data.email,
        verification_token=verification_token
    )
    return user_id


async def verify_email(
        user_email: Annotated[str, Query(description="The str email of user")],
        verify_token: Annotated[str, Query(description="The str verify_token of user verify account")],
        request: Request
):
    user_verify_token = await get_verify_token_by_user_email(user_email=user_email, request=request)
    if user_verify_token is not None and user_verify_token == verify_token:
        logger.info("TRFYGDYUFDYIFOD")
        await verify_user(user_email=user_email, request=request)


async def verify_email_new(
        user_email: Annotated[str, Query(description="The str email of user")],
        request: Request
):
    verification_token = await generate_verify_token()

    is_set_verify_token = await set_verify_token(
        email=user_email,
        verify_token=verification_token,
        request=request
    )
    if is_set_verify_token is False:
        raise UserEmailNotFoundException(email=user_email)

    await send_verification_mail(
        email=user_email,
        verification_token=verification_token
    )
