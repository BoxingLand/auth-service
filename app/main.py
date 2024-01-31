import asyncio
import logging

import grpc
from loguru import logger

from app.auth import auth_pb2_grpc
from app.auth.auth_server import Auth
from app.core.config import settings
from app.database.connection import open_pool


async def serve() -> None:
    await open_pool()
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServicer_to_server(Auth(), server)
    listen_addr = f"[::]:{settings.SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
