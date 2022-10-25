from passlib.context import CryptContext
from sanic.config import Config


class DefaultConfig(Config):
    # TODO: os.environ
    DB_HOST: str = "localhost"
    DB_NAME: str = "postgres"
    DB_USER: str = "user"
    DB_PASSWORD: str = "hackme"

    SECRET: str = "secret"
    PWD_CONTEXT: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

