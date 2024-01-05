from app.core.config import settings
from app.core.rabbit.rabbit_connection import rabbit_connection
from app.dto.request.signup_dto import SignupDto


async def signup(
        signup_data: SignupDto
):
    await rabbit_connection.send_message(
        headers={
            "email": signup_data.email
        },
        message=dict(signup_data),
        routing_key=settings.USER_CONFIRM_QUEUE_RECEIVE
    )
    return signup_data


async def user_exists(signup_data: SignupDto):
    ...
