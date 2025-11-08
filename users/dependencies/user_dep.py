from typing import Annotated

from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from starlette import status

from auth.jwt_core.core import decode_jwt
from common.dependencies.authorization_dependencies import JWTFromHeader
from..models.users import User

http_bearer = HTTPBearer()


async def get_user_by_email(email: str):
    try:
        return await User.find_first_by_kwargs(email=email)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

UserByEmail = Annotated[User, Depends(get_user_by_email)]


async def get_user_by_id():
    ...

async def get_user_by_username():
    ...


#async def get_current_user(jwt: JWTFromHeader) -> User:
async def get_current_user(jwt: Depends(http_bearer)) -> User:
    decoded_jwt = decode_jwt(jwt)
    return await User.find_first_by_id(decoded_jwt["sub"])

CurrentUser = Annotated[User, Depends(get_current_user)]
