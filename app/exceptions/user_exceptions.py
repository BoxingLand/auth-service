from typing import Any

from fastapi import HTTPException
from starlette import status


class UserEmailExistException(HTTPException):
    def __init__(
            self,
            email: str | None = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        if email:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The email {email} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The email already exists.",
            headers=headers,
        )


class UserPhoneNumberExistException(HTTPException):
    def __init__(
            self,
            phone_number: str | None = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        if phone_number:
            super().__init__(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"The phone number {phone_number} already exists.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="The phone number already exists.",
            headers=headers,
        )

class UserPasswordNotMatchException(HTTPException):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:

        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match.",
            headers=headers,
        )


class UserCreateException(HTTPException):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="User is not create.",
            headers=headers,
        )


class UserEmailNotFoundException(HTTPException):
    def __init__(
            self,
            email: str | None = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        if email:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The email {email} not found.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The email not found.",
            headers=headers,
        )


class UserNotFoundException(HTTPException):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user not found.",
            headers=headers,
        )


class UserPhoneNumberNotFoundException(HTTPException):
    def __init__(
            self,
            phone_number: str | None = None,
            headers: dict[str, Any] | None = None,
    ) -> None:
        if phone_number:
            super().__init__(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"The phone number {phone_number} not found.",
                headers=headers,
            )
            return

        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The phone number not found.",
            headers=headers,
        )

class UserValidateException(HTTPException):
    def __init__(
            self,
            headers: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect login details.",
            headers=headers,
        )
