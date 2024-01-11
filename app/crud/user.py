from uuid import UUID, uuid4

from fastapi import Request
from loguru import logger
from psycopg.rows import class_row

from app.dto.models.user import User
from app.dto.request.signup_dto import SignupRequestDto
from app.exceptions.user_exceptions import UserCreateException, UserEmailNotFoundException


async def create_user(
        signup_data: SignupRequestDto,
        request: Request
) -> UUID | None:
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    WITH user_data AS (
                        INSERT INTO "user" (id, email, phone_number, password, updated_at, created_at, is_active, is_deleted)
                        VALUES ('{uuid4()}',
                                '{signup_data.email.lower()}',
                                '{signup_data.phone_number}',
                                '{signup_data.password}',
                                now()::timestamp,
                                now()::timestamp,
                                FALSE,
                                FALSE
                        )
                        RETURNING id
                    )
                    INSERT INTO "{signup_data.account_type.value}" (id, user_id, updated_at, created_at, is_deleted)
                    VALUES('{uuid4()}',
                            (SELECT id FROM user_data),
                            now()::timestamp,
                            now()::timestamp,
                            FALSE
                    );
                                """)
                await conn.commit()
                # inserted_id = await cur.fetchone()
                # return inserted_id[0]
    except Exception as e:
        logger.error(e)
        await conn.rollback()
        raise UserCreateException()  # noqa: B904


async def get_user_by_id(
        user_id: UUID,
        request: Request
) -> User | None:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor(row_factory=class_row(User)) as cur:
            await cur.execute(f"""
                   SELECT * 
                   FROM "user" 
                   WHERE id = '{user_id}' AND is_deleted = FALSE;
                               """)
            user = await cur.fetchone()
            return user


async def get_user_by_email(
        email: str,
        request: Request
) -> User | None:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor(row_factory=class_row(User)) as cur:
            await cur.execute(f"""
                   SELECT * 
                   FROM "user" 
                   WHERE email = '{email}' AND is_deleted = FALSE;
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
                   WHERE phone_number = '{phone_number}' AND is_deleted = FALSE;
                               """)
            user = await cur.fetchone()
            return user


async def user_email_exists(
        email: str,
        request: Request
) -> str | None:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                SELECT email
                FROM "user"
                WHERE email = '{email}' AND is_deleted = FALSE;
                            """)
            user_email = await cur.fetchone()
            if user_email is None:
                return None
            return user_email[0]


async def user_phone_number_exists(
        phone_number: str,
        request: Request
) -> str | None:
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                SELECT phone_number 
                FROM "user" 
                WHERE phone_number = '{phone_number}' AND is_deleted = FALSE;
                            """)
            user_phone_number = await cur.fetchone()
            if user_phone_number is None:
                return None
            return user_phone_number[0]


async def get_verify_token_by_user_email(
        user_email: str,
        request: Request):
    async with request.app.async_pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"""
                SELECT verify_token 
                FROM "user"
                WHERE email = '{user_email}' AND is_deleted = FALSE;
                            """)
            user_verify_token = await cur.fetchone()
            return user_verify_token[0]


async def set_verify_token(
        email: str,
        verify_token: str,
        request: Request
):
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    UPDATE "user"
                    SET verify_token = '{verify_token}'
                    WHERE email = '{email}' AND is_deleted = FALSE; 
                                """)
                await conn.commit()

    except Exception as e:
        logger.error(e)
        await conn.rollback()
        raise UserEmailNotFoundException(email=email)  # noqa: B904


async def verify_user(
        user_email: str,
        request: Request
) -> None:
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    UPDATE "user"
                    SET is_active = True
                    WHERE email = '{user_email}' AND is_deleted = FALSE;
                                """)
                await conn.commit()


    except Exception as e:
        logger.error(e)
        await conn.rollback()


async def update_user_password(
        user_id: UUID,
        new_password: str,
        request: Request,
) -> None:
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    UPDATE "user"
                    SET password = '{new_password}'
                    WHERE id = '{user_id}' AND is_deleted = FALSE;
                                """)
                await conn.commit()


    except Exception as e:
        logger.error(e)
        await conn.rollback()


async def delete_user(
        user_id: UUID,
        request: Request,
):
    try:
        async with request.app.async_pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute(f"""
                    UPDATE "user"
                    SET is_deleted = TRUE
                    WHERE id = '{user_id}';
                                """)
                await conn.commit()


    except Exception as e:
        logger.error(e)
        await conn.rollback()
