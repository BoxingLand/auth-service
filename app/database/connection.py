from app.core.config import settings
from loguru import logger
from psycopg_pool import AsyncConnectionPool

logger.info(settings.get_db_connection_scheme())
pool = AsyncConnectionPool(conninfo=settings.get_db_connection_scheme(), open=False, max_size=settings.DB_POOL_SIZE)


async def open_pool():
    await pool.open()
    await pool.wait()
    logger.info("Connection Pool Opened")
