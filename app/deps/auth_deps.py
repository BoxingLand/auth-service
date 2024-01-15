from typing import Annotated

from fastapi import BackgroundTasks, Query, Request

from app.core.security import security
from app.core.security.security import TokenType, encrypt_password
from app.crud.user import (
    create_user,
    get_verify_token_by_user_email,
    set_verify_token,
    user_email_exists,
    user_phone_number_exists,
    verify_user,
)
from app.dto.models.token import Token
from app.dto.request.signin_dto import SigninRequestDto
from app.dto.request.signup_dto import SignupRequestDto
from app.exceptions.token_exceptions import TokenIncorrectException
from app.exceptions.user_exceptions import (
    UserEmailExistException,
    UserEmailNotFoundException,
    UserPasswordNotMatchException,
    UserPhoneNumberExistException,
    UserPasswordIsEasyException
)
from app.utlis.authenticate import authenticate, create_jwt_tokens
from app.utlis.verification.generate_verify_token import generate_verification_token
from app.utlis.verification.send_verification_mail import send_verification_mail
from app.utlis.password_validation import password_validation


async def signup(
        signup_data: SignupRequestDto,
        request: Request,
        background_tasks: BackgroundTasks,
):
    if signup_data.password != signup_data.password_confirm:
        raise UserPasswordNotMatchException()
    
    password_check = await password_validation(signup_data.password)
    if len(password_check):
        raise UserPasswordIsEasyException(details=password_check)

    email_exists = await user_email_exists(email=signup_data.email, request=request)
    if email_exists == signup_data.email and signup_data.email is not None:
        raise UserEmailExistException(email=signup_data.email)

    phone_number_exists = await user_phone_number_exists(phone_number=signup_data.phone_number, request=request)
    if phone_number_exists == signup_data.phone_number and signup_data.phone_number is not None:
        raise UserPhoneNumberExistException(phone_number=signup_data.phone_number)

    signup_data.password = encrypt_password(password=signup_data.password)
    await create_user(signup_data=signup_data, request=request)

    verification_token = generate_verification_token()

    await set_verify_token(
        email=signup_data.email,
        verify_token=verification_token,
        request=request,
    )
    background_tasks.add_task(send_verification_mail, signup_data.email, verification_token)
    return "Success"


async def signin(
        signin_data: SigninRequestDto,
        request: Request,
) -> Token:
    user = await authenticate(signin_data=signin_data, request=request, )

    token_data = await create_jwt_tokens(
        user_id=user.id,
        request=request,
    )

    return token_data


async def verify_email(
        user_email: Annotated[str, Query(description="The str email of user")],
        verify_token: Annotated[str, Query(description="The str verify_token of user verify account")],
        request: Request,
):
    user_verify_token = await get_verify_token_by_user_email(user_email=user_email, request=request)
    if user_verify_token is not None and user_verify_token == verify_token:
        await verify_user(user_email=user_email, request=request)


async def verify_email_new(
        user_email: Annotated[str, Query(description="The str email of user")],
        request: Request,
        background_tasks: BackgroundTasks,
):
    verification_token = generate_verification_token()

    is_set_verify_token = await set_verify_token(
        email=user_email,
        verify_token=verification_token,
        request=request,
    )
    if is_set_verify_token is False:
        raise UserEmailNotFoundException(email=user_email)

    background_tasks.add_task(send_verification_mail, user_email, verification_token)


async def update_refresh_token(
        refresh_token: Annotated[str, Query(description="Update refresh token of user")],
        request: Request
):
    refresh_token_decoded = security.decode_token(token=refresh_token)
    if refresh_token_decoded["type"] != TokenType.refresh_token:
        raise TokenIncorrectException()

    token_data = await create_jwt_tokens(
        user_id=refresh_token_decoded["sub"],
        request=request,
    )

    return token_data
