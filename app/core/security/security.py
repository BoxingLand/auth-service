from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def encrypt_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, encrypted_password: str):
    return pwd_context.verify(password, encrypted_password)
