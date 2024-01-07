from fastapi import APIRouter, Depends

from app.core.config import settings
from app.deps import auth_deps
from app.utlis.response_schema import create_response

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
        signin_response=Depends(auth_deps.signin)   # noqa: B008
):
    return create_response(data=signin_response)

@router.get("/refresh")
async def _refresh():
    ...

@router.get("/change_password")
async def _change_password(
):
    ...

@router.put("/update")
async def _update_data():
    ...

@router.delete("/delete")
async def _delete_data():
    ...
