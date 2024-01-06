from fastapi_mail import FastMail

from app.core.mail_sender.config import connection_config

fast_mail = FastMail(connection_config)
