from fastapi import APIRouter, Depends

from app_old.deps import auth_deps
from app_old.dto.models.token import Token
from app_old.utlis.response_schema import IGetResponseBase, IPostResponseBase, create_response

router = APIRouter()



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

