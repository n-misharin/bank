from pydantic import BaseModel, validator, Field

from bank.config.config import DefaultConfig


class UserAuthenticationRequest(BaseModel):
    username: str
    password: str


class UserAuthenticationResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
