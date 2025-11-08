from pydantic import BaseModel, EmailStr


class UserCredentialsSchema(BaseModel):
    email: EmailStr
    password: str

class JWTResponseSchema(BaseModel):
    jwt: str
    token_type: str
