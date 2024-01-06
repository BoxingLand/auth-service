from fastapi_mail import ConnectionConfig, MessageSchema, MessageType

from app.core.config import settings

connection_config = ConnectionConfig(
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_USERNAME=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)


def get_message_schema(email: str, token: str) -> MessageSchema:
    return MessageSchema(
        subject="Подтверждение аккаунта",
        recipients=[email],
        body=f"""
            <html>
            <body>
                <p>Для подтверждения аккаунта перейдите по ссылке ниже:</p>
                <a href="http://localhost:8000/api/v1/auth/verify/email?user_email={email}&verify_token={token}">
                Подтвердить аккаунт</a>
            </body>
            </html>
        """,
        subtype=MessageType.html
    )
