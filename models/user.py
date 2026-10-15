import datetime

from pydantic import BaseModel, Field, field_validator

from constants.roles import Roles


class CreateUserRequest(BaseModel):
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    password: str = Field(..., min_length=1, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: bool | None
    banned: bool | None


class CreateUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles] = [Roles.USER]
    verified: bool | None = None
    banned: bool | None = None
    createdAt: str

    @field_validator("createdAt")
    @classmethod
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("CreatedAt must be a date")
        return value


class GetUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles] = [Roles.USER]
    verified: bool | None = None
    banned: bool | None = None
    createdAt: str

    @field_validator("createdAt")
    @classmethod
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("CreatedAt must be a date")
        return value