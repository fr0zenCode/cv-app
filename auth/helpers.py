from .jwt_core.core import decode_jwt
from ..users.models.users import User


def get_user_id_by_jwt(jwt: str) -> int:
    decoded_jwt = decode_jwt(jwt)
    return decoded_jwt["sub"]

def get_username_by_jwt(jwt: str) -> str:
    decoded_jwt = decode_jwt(jwt)
    return decoded_jwt["username"]

async def get_user_by_jwt(jwt: str) -> User:
    return await User.find_first_by_id(get_user_id_by_jwt(jwt))
