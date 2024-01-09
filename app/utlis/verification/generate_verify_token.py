import hashlib
from random import randbytes


def generate_verification_token():
    token = randbytes(10)
    hashed_code = hashlib.sha256()
    hashed_code.update(token)
    verification_token = hashed_code.hexdigest()
    return verification_token
