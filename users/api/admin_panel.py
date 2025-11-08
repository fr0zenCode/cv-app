from starlette import status
from fastapi import APIRouter

from ..models.users import User

admin_panel_users = APIRouter(prefix="/admin/users", tags=["Admin Panel", "Users"])


@admin_panel_users.get("/user", response_model=None)
async def get_user_by_id(user_id: int) -> User:
    return await User.find_first_by_id(user_id)

@admin_panel_users.delete("/user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int) -> None:
    user = await User.find_first_by_id(user_id)
    await user.delete()
