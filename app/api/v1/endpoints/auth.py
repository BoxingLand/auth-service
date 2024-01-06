from fastapi import APIRouter, Depends

from app.core.config import settings
from app.deps import auth_deps
from app.utlis.response_schema import create_response

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post("/signup")
async def _signup(
        auth_response=Depends(auth_deps.signup)
):
    return create_response(data=auth_response)


@router.get("/verify/email")
async def _verify_email(
        verify_response=Depends(auth_deps.verify_email)
):
    return create_response(data=verify_response)


@router.get("/verify/email/new")
async def _verify_email_new(
        verify_response=Depends(auth_deps.verify_email_new)
):
    return create_response(data=verify_response)


@router.get("/signin")
async def _login():
    ...

@router.get("/refresh")
async def _refresh():
    ...

@router.get("/change_password")
async def _change_password():
    ...

@router.put("/update")
async def _update_data():
    ...

@router.delete("/delete")
async def _delete_data():
    ...
