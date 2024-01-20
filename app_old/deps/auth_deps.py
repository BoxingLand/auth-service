from typing import Annotated

from fastapi import BackgroundTasks, Query, Request

from app_old.core.security import security
from app_old.core.security.security import TokenType, encrypt_password
from app_old.crud.user import (
    create_user,
    get_verify_token_by_user_email,
    set_verify_token,
    user_email_exists,
    user_phone_number_exists,
    verify_user,
)
from app_old.dto.models.token import Token
from app_old.dto.request.auth import SignupRequestDto, SigninRequestDto
from app_old.exceptions.token_exceptions import TokenIncorrectException
from app_old.exceptions.user_exceptions import (
    UserEmailExistException,
    UserEmailNotFoundException,
    UserPasswordNotMatchException,
    UserPhoneNumberExistException,
    UserPasswordIsEasyException
)
from app_old.utlis.authenticate import authenticate, create_jwt_tokens
from app_old.utlis.verification.generate_verify_token import generate_verification_token
from app_old.utlis.verification.send_verification_mail import send_verification_mail
from app_old.utlis.password_validation import password_validation



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

