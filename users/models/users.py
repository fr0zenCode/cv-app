from typing import Annotated

import bcrypt
import pydantic_core
from pydantic_marshals.sqlalchemy import MappedModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, VARCHAR
from pydantic import AfterValidator, validate_email, EmailStr
from fastapi import HTTPException
from starlette import status

from common.config import Base


class User(Base):
    __tablename__ = "users"


    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(36))
    email: Mapped[str] = mapped_column(VARCHAR(255))
    password: Mapped[str] = mapped_column(String(100))
    email_confirmed: Mapped[bool] = mapped_column(default=False)


    @staticmethod
    def hash_password(password: str):
        hashed_pw = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt(14))
        return hashed_pw.decode("UTF-8")

    @staticmethod
    def email_validator(email: str) -> str:
        try:
            return validate_email(email)[1]
        except pydantic_core._pydantic_core.PydanticCustomError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email format")


    def is_password_valid(self, plain_text_pw: str) -> bool:
        real_pw_bytes = self.password.encode("UTF-8")
        plain_text_pw_bytes = plain_text_pw.encode("UTF-8")
        return bcrypt.checkpw(plain_text_pw_bytes, real_pw_bytes)


    PasswordType = Annotated[
        str,
        AfterValidator(hash_password),
    ]

    EmailType = Annotated[
        str,
        AfterValidator(email_validator),
    ]


    InputSchema = MappedModel.create(
        columns=[
            username,
            (email, EmailType),
            (password, PasswordType)
        ]
    )

    ResponseSchema = MappedModel.create(
        columns=[
            id,
            username,
            email,
            email_confirmed
        ]
    )

    LoginSchema = MappedModel.create(
        columns=[
            email,
            password
        ]
    )
