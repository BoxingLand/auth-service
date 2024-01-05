from functools import lru_cache

from pydantic_settings import BaseSettings

from app.core.config import settings


class RabbitServerSettings(BaseSettings):
    url: str = settings.RABBITMQ_URL


class UserConfirmQueueReceive(RabbitServerSettings):
    queue: str = settings.USER_CONFIRM_QUEUE_RECEIVE
    auto_delete: bool = False
    durable: bool = False


class RabbitSettings:
    basic = RabbitServerSettings()
    user_confirm = UserConfirmQueueReceive()



def get_rmq_settings() -> RabbitSettings:
    return RabbitSettings()


rmq_settings = get_rmq_settings()
