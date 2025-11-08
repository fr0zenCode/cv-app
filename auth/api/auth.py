from starlette import status
from fastapi import APIRouter, HTTPException

from auth.jwt_core.core import create_jwt
from auth.schemas import UserCredentialsSchema, JWTResponseSchema
from users.models.users import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/login")
async def login(credentials: UserCredentialsSchema) -> JWTResponseSchema:
    user = await User.find_first_by_kwargs(email=str(credentials.email))
    if user and user.is_password_valid(credentials.password):
        jwt = create_jwt(user=user)
        return JWTResponseSchema(jwt=jwt, token_type="Bearer")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incorrect email or password")

@auth_router.post("/logout")
async def logout():
    ...
