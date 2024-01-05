import json
from dataclasses import dataclass

from aio_pika import connect_robust, Message
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustChannel, AbstractRobustConnection
from loguru import logger

from app.core.config import settings
from app.core.rabbit.queues import rmq_settings


@dataclass
class RabbitConnection:
    connection: AbstractRobustConnection | None = None
    channel: AbstractRobustChannel | None = None

    def status(self) -> bool:

        """
            Checks if connection established

            :return: True if connection established

        """
        if self.connection.is_closed or self.channel.is_closed:
            return False
        return True

    async def _clear(self) -> None:
        if not self.channel.is_closed:
            await self.channel.close()
        if not self.connection.is_closed:
            await self.connection.close()

        self.connection = None
        self.channel = None


    async def connect(self) -> None:

        """
        Establish connection with the RabbitMQ

        :return: None

        """
        logger.info('Connecting to the RabbitMQ...')
        try:
            self.connection = await connect_robust(settings.RABBITMQ_URL)
            self.channel = await self.connection.channel(publisher_confirms=False)

            logger.info('Successfully connected to the RabbitMQ!')

            await self.declare_queue()
            # await self.consume_queue()

        except Exception as e:
            await self._clear()
            logger.error(e)

    async def declare_queue(self) -> None:

        """
        Declare queue

        :return: None

        """
        await self.channel.set_qos(prefetch_count=1)
        await self.channel.declare_queue(
            name=rmq_settings.user_confirm.queue,
            auto_delete=rmq_settings.user_confirm.auto_delete,
            durable=rmq_settings.user_confirm.durable
        )
        logger.info('Declared queue "{}"', rmq_settings.user_confirm.queue)


    async def consume_queue(self) -> None:

        """
        Get queues

        :return: None
        """

        receive_queue_user_confirm = await self.channel.get_queue(rmq_settings.user_confirm.queue)
        await receive_queue_user_confirm.consume(self.receive_processing_projects)

    async def receive_processing_projects(self, message: AbstractIncomingMessage) -> None:

        """
        Get project from message

        :param message: AbstractIncomingMessage
        :return: None
        """

        await message.ack()

    async def send_message(
            self,
            headers: dict,
            message: dict,
            routing_key: str
    ) -> None:
        if not self.channel:
            raise RuntimeError('The message could not be sent because the connection with RabbitMQ is not established')

        if not self.channel:
            raise RuntimeError('The message could not be sent because the connection with RabbitMQ is not established')

        async with self.channel.transaction():
            message = Message(
                headers=headers,
                body=json.dumps(message).encode()
            )

            await self.channel.default_exchange.publish(
                message,
                routing_key=routing_key,
            )
        logger.info(f"Message sent to {routing_key}")


    async def disconnect(self) -> None:

        """
        Disconnect and clear connections from RabbitMQ

        :return: None
        """

        await self._clear()



rabbit_connection = RabbitConnection()
