from pydantic import BaseModel, validator

from bank.config.config import DefaultConfig


class RegistrationUserForm(BaseModel):
    login: str
    password: str

    @validator("password")
    def validate_password(cls, password):
        return DefaultConfig.PWD_CONTEXT.hash(password)
