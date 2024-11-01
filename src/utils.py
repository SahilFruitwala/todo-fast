import bcrypt
from datetime import datetime, timezone


def utc_time():
    return datetime.now(timezone.utc)


def get_hashed_password(password: str) -> bytes:
    encoded_pass = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(encoded_pass, salt)

def check_password(password: str, hashed_password: bytes) -> bool:
    encoded_pass = password.encode('utf-8')
    return bcrypt.checkpw(encoded_pass, hashed_password)
