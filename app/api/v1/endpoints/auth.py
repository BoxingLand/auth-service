from fastapi import APIRouter, Depends

from app.deps import auth_deps
from app.dto.models.token import Token
from app.utlis.response_schema import IGetResponseBase, IPostResponseBase, create_response

router = APIRouter()


@router.post("/signup")
async def _signup(
        auth_response=Depends(auth_deps.signup)  # noqa: B008
):
    return create_response(data=auth_response)


@router.get("/verify/email")
async def _verify_email(
        verify_response=Depends(auth_deps.verify_email)  # noqa: B008
):
    return create_response(data=verify_response)


@router.get("/verify/email/new")
async def _verify_email_new(
        verify_response=Depends(auth_deps.verify_email_new)  # noqa: B008
):
    return create_response(data=verify_response)


@router.post("/signin")
async def _signin(
        signin_response=Depends(auth_deps.signin)  # noqa: B008
) -> IPostResponseBase[Token]:
    return create_response(data=signin_response)


@router.get("/refresh")
async def _refresh(
        refresh_response=Depends(auth_deps.update_refresh_token)  # noqa: B008
) -> IGetResponseBase[Token]:
    return create_response(data=refresh_response)
