from pydantic import BaseModel, AnyHttpUrl, Field


class UserRegistrationRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=3, max_length=50)


class UserRegistrationResponse(BaseModel):
    confirmed_url: AnyHttpUrl
