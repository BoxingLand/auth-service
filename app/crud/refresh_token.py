from datetime import datetime
from uuid import UUID, uuid4

from loguru import logger

from app.database.connection import pool


async def set_refresh_token(
        user_id: UUID,
        refresh_token: str
) -> None:
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    INSERT INTO "refresh_token" (id, user_id, refresh_token, created_at)
                    VALUES('{uuid4()}',
                           '{user_id}',
                           '{refresh_token}',
                           '{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}'
                           );
                                """)
                await conn.commit()
    except Exception as e:
        logger.error(e)
        await conn.rollback()


async def delete_all_refresh_tokens(
        user_id: UUID
):
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    DELETE FROM "refresh_token"
                    WHERE user_id = '{user_id}';
                                """)
                await conn.commit()
    except Exception as e:
        logger.error(e)
        await conn.rollback()
