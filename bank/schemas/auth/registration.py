from pydantic import BaseModel, AnyHttpUrl, Field, validator


class UserRegistrationRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, regex=r"^[0-9a-zA-Z_]*$")
    password: str = Field(min_length=3, max_length=50)

    @validator("username")
    def validate_username(cls, username: str):
        return username.lower()


class UserRegistrationResponse(BaseModel):
    confirmed_url: AnyHttpUrl
