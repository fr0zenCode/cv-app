from pathlib import Path

from .sqlalchemy_ext import MappingBase
from pydantic import computed_field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


BASE_DIR = Path(__file__).parent.parent


class JWT(BaseModel):
    public_key_path: Path = BASE_DIR / "auth" / "secret_keys" / "jwt-public.pem"
    private_key_path: Path = BASE_DIR / "auth" / "secret_keys" / "jwt-private.pem"
    algorithm: str = "RS256"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    jwt: JWT = JWT()

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "postgres_cv"
    postgres_pass: str = "postgres_cv"
    postgres_name: str = "postgres_cv"

    SMTP_port: int = 465
    SMTP_host: str = "smtp.gmail.com"
    GMAIL_app_password: str = "ajam nmww kvsb lbeq"
    our_email: str = "cv.updater.ai@gmail.com"

    production_mode: bool = False

    @computed_field
    @property
    def postgres_dsn(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.postgres_user}"
            f":{self.postgres_pass}"
            f"@{self.postgres_host}"
            f"/{self.postgres_name}"
        )


settings = Settings()

engine = create_async_engine(settings.postgres_dsn)
sessionmaker = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase, MappingBase):
    __tablename__: str
    __abstract__: bool

