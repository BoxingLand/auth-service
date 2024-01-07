import json
from datetime import datetime
from uuid import UUID, uuid4

import psycopg
from fastapi import Request
from loguru import logger
from psycopg.rows import class_row

from app.dto.models.user import User
from app.dto.request.signup_dto import SignupRequestDto


async def create_user(
        signup_data: SignupRequestDto,
        request: Request
) -> UUID | None:
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    INSERT INTO "user" (id, email, phone_number, password, is_active, updated_at, created_at, is_deleted)
                    VALUES('{uuid4()}',
                           '{signup_data.email.lower()}',
                           '{signup_data.phone_number}',
                           '{signup_data.password}',
                           '{False}',
                           '{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}',
                           '{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}',
                           '{False}'
                           )
                    RETURNING id;
                                """)
                await conn.commit()
                inserted_id = await cur.fetchone()
                return inserted_id[0]
    except Exception as e:
        logger.error(e)
        await conn.rollback()
        return None


async def get_user_by_email(
        email: str,
        request: Request
) -> User | None:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor(row_factory=class_row(User)) as cur:
            await cur.execute(f"""
                   SELECT *
                   FROM "user" 
                   WHERE email = '{email}';
                               """)
            user = await cur.fetchone()
            return user

async def get_user_by_phone_number(
        phone_number: str,
        request: Request
) -> User | None:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor(row_factory=class_row(User)) as cur:
            await cur.execute(f"""
                   SELECT * 
                   FROM "user" 
                   WHERE phone_number = '{phone_number}';
                               """)
            user = await cur.fetchone()
            return user


async def user_email_exists(
        email: str,
        request: Request
) -> bool:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                SELECT email FROM "user" WHERE email = '{email}';
                            """)
            user_email = await cur.fetchone()
            return True if user_email is not None else False


async def user_phone_number_exists(
        phone_number: str,
        request: Request
) -> bool:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                SELECT phone_number FROM "user" WHERE phone_number = '{phone_number}';
                            """)
            user_phone_number = await cur.fetchone()
            return True if user_phone_number is not None else False


async def get_verify_token_by_user_email(
        user_email: str,
        request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                SELECT verify_token
                FROM "user"
                WHERE email = '{user_email}';
                            """)
            user_verify_token = await cur.fetchone()
            return user_verify_token[0]


async def set_verify_token(
        email: str,
        verify_token: str,
        request: Request
) -> bool:
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    UPDATE "user"
                    SET verify_token = '{verify_token}'
                    WHERE email = '{email}'
                                """)
                await conn.commit()
                return True

    except Exception as e:
        logger.error(e)
        await conn.rollback()
        return False


async def verify_user(user_email: str, request: Request) -> None:
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    UPDATE "user"
                    SET is_active = '{True}'
                    WHERE email = '{user_email}'
                                """)
                await conn.commit()


    except Exception as e:
        logger.error(e)
        await conn.rollback()
