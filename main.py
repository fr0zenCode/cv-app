from typing import Callable, Awaitable

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from common.config import sessionmaker
from common.sqlalchemy_ext import session_context
from auth.api.auth import auth_router
from users.api.admin_panel import admin_panel_users
from users.api.crud import user_crud_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_crud_router)

app.include_router(admin_panel_users)


@app.middleware("http")
async def database_session_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    async with sessionmaker.begin() as session:
        session_context.set(session)
        return await call_next(request)


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="localhost", reload=True)
