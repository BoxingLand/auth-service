from fastapi_mail import FastMail

from app_old.core.mail_sender.config import connection_config

fast_mail = FastMail(connection_config)
