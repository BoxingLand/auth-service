from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router_v1
from app.core.config import settings
from app.core.rabbit.rabbit_connection import rabbit_connection


@asynccontextmanager
async def lifespan(_: FastAPI):
    await rabbit_connection.connect()
    yield
    await rabbit_connection.disconnect()


app = FastAPI(title=settings.API_TITLE, lifespan=lifespan)

app.include_router(api_router_v1, prefix=settings.API_PREFIX)


if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
