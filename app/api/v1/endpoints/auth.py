from fastapi import APIRouter, Depends

from app.core.config import settings
from app.deps import auth_deps
from app.utlis.response_schema import create_response

router = APIRouter()
ACCESS_TOKEN_EXPIRES_IN = settings.ACCESS_TOKEN_EXPIRES_IN
REFRESH_TOKEN_EXPIRES_IN = settings.REFRESH_TOKEN_EXPIRES_IN


@router.post("/signup")
async def signup(
        auth_response=Depends(auth_deps.signup)
):
    return create_response(data=auth_response)
