from psycopg_pool import AsyncConnectionPool

from app.core.config import settings


def get_conn_str():
    return f"""
    dbname={settings.DATABASE_NAME}
    user={settings.DATABASE_USER}
    password={settings.DATABASE_PASSWORD}
    host={settings.DATABASE_HOST}
    port={settings.DATABASE_PORT}
    """


pool = AsyncConnectionPool(conninfo=get_conn_str(), open=False, max_size=settings.DB_POOL_SIZE)


async def open_pool():
    await pool.open()
    await pool.wait()
    print("Connection Pool Opened")
