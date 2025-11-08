from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader

JWTHeader = Annotated[
    str | None,
    Depends(
        APIKeyHeader(
            name="Authorization",
            auto_error=False
        )
    ),
]


async def jwt_header_proxy(jwt: JWTHeader) -> str:
    return jwt


JWTFromHeader = Annotated[str, Depends(jwt_header_proxy)]
