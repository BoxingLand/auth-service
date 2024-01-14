from fastapi import APIRouter, Depends

from app.deps import profile_deps
from app.dto.models.token import Token
from app.utlis.response_schema import IDeleteResponseBase, IGetResponseBase, IPutResponseBase, create_response

router = APIRouter()


@router.post("/change_password")
async def _change_password(
        change_password_response=Depends(profile_deps.change_password)  # noqa: B008
) -> IGetResponseBase[Token]:
    return create_response(data=change_password_response)


@router.put("/update")
async def _update_data(
    update_user_response=Depends(profile_deps.update_user)
) -> IPutResponseBase[str]:
    return create_response(data=update_user_response)


@router.post("/add_role")
async def _add_role():
    ...


@router.delete("/delete")
async def _delete_data(
        delete_user_response=Depends(profile_deps.delete_user)  # noqa: B008
) -> IDeleteResponseBase[str]:
    return create_response(data=delete_user_response)
