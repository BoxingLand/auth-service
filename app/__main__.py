import asyncio
import logging

import grpc
import prometheus_client
from app.auth import auth_pb2_grpc
from app.auth.auth_server import Auth
from app.core.config import settings
from app.database.connection import open_pool
from grpc_health.v1 import health, health_pb2, health_pb2_grpc
from loguru import logger


async def serve() -> None:
    await open_pool()
    server = grpc.aio.server()
    auth_pb2_grpc.add_AuthServicer_to_server(Auth(), server)
    listen_addr = f"[::]:{settings.SERVER_PORT}"
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting server on {listen_addr}")

    health_servicer = health.HealthServicer()
    health_servicer.set("instance_id", health_pb2.HealthCheckResponse.SERVING)
    health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)

    prometheus_client.start_http_server(settings.METRICS_PORT)

    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
