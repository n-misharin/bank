import os

from passlib.context import CryptContext
from sanic.config import Config


class DefaultConfig(Config):
    APP_HOST: str = os.environ.get("APP_HOST", "localhost")
    APP_PORT: int = os.environ.get("APP_PORT", 8000)
    APP_SCHEME: str = "http"
    PATH_PREFIX: str = os.environ.get("PATH_PREFIX", "")

    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_NAME: str = os.environ.get("DB_NAME", "postgres")
    DB_USER: str = os.environ.get("DB_USER", "user")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "hackme")
    DB_PORT: int = os.environ.get("DB_PORT", 5432)

    SECRET: str = os.environ.get("SECRET", "secret")
    SECURITY_PASSWORD_SALT: str = os.environ.get("SECURITY_PASSWORD_SALT", "salt")

    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    JWT_ALGORITHM: str = os.environ.get("JWT_ALGORITHM", "HS256")

    CONFIRM_TOKEN_EXPIRE_MINUTES: int = os.environ.get("CONFIRM_TOKEN_EXPIRE_MINUTES", 5)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24)

    DEBUG: bool = True

    def get_db_uri(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class ProductionConfig(DefaultConfig):
    DEBUG: bool = False
