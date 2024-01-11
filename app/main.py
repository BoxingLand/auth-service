from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from psycopg_pool import AsyncConnectionPool
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router_v1
from app.core.config import settings


def get_conn_str():
    return f"""
    dbname={settings.DATABASE_NAME}
    user={settings.DATABASE_USER}
    password={settings.DATABASE_PASSWORD}
    host={settings.DATABASE_HOST}
    port={settings.DATABASE_PORT}
    """


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.async_pool = AsyncConnectionPool(conninfo=get_conn_str())
    yield
    await app.async_pool.close()


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

Instrumentator().instrument(app).expose(app)
