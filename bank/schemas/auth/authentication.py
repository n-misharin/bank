from pydantic import BaseModel, validator, Field


class UserAuthenticationRequest(BaseModel):
    username: str
    password: str

    @validator("username")
    def validate_username(cls, username: str):
        return username.lower()


class UserAuthenticationResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer")
