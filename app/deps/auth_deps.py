from app.dto.request.signup_dto import SignupDto


async def signup(
        signup_data: SignupDto
):
    return signup_data


async def user_exists(signup_data: SignupDto):
    ...
