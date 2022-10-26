from passlib.context import CryptContext
from sanic.config import Config


class DefaultConfig(Config):
    # TODO: os.environ
    HOST: str = "localhost"
    PORT: int = 8001
    SERVER_NAME = f"{HOST}:{PORT}"
    APP_SCHEME: str = "http"

    DB_HOST: str = "localhost"
    DB_NAME: str = "postgres"
    DB_USER: str = "user"
    DB_PASSWORD: str = "hackme"

    SECRET: str = "secret"
    SECURITY_PASSWORD_SALT: str = "salt"

    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")
    JWT_ALGORITHM: str = "HS256"
    CONFIRM_TOKEN_EXPIRE_MINUTES: int = 5
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    DEBUG: bool = True
