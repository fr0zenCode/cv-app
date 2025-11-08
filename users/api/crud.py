from starlette import status
from fastapi import APIRouter

from ..dependencies.user_dep import CurrentUser
from ..models.users import User


user_crud_router = APIRouter()


@user_crud_router.post("/users", response_model=None)
async def create_user(input_schema: User.InputSchema) -> User:
    return await User.create(**input_schema.model_dump())



@user_crud_router.get("/users/user/me", response_model=None)
async def my_profile(user: CurrentUser):
    return user


@user_crud_router.patch("/users/user/me")
async def update_my_data(user: CurrentUser):
    #update email
    #update username
    #update password
    ...

@user_crud_router.delete("/users/user/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_account(user: CurrentUser) -> None:
    await user.delete()
