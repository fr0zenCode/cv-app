from datetime import datetime, timedelta

from jwt import encode, decode

from users.models.users import User
from common.config import settings


def create_jwt(user: User) -> str:
    payload = {
        "iss": "cv-updater",
        "sub": str(user.id),
        "exp": datetime.now() + timedelta(minutes=60),
        "iat": datetime.now(),
        "username": user.username
    }
    encoded_payload = encode(
        payload=payload.copy(),
        key=settings.jwt.private_key_path.read_text(),
        algorithm=settings.jwt.algorithm
    )
    return encoded_payload


def decode_jwt(
        jwt: str,
        key: str = settings.jwt.public_key_path.read_text(),
        algorithm: str = settings.jwt.algorithm
) -> dict:
    decoded_jwt = decode(jwt, key, algorithm)
    return decoded_jwt
