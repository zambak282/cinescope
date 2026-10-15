import datetime

from pydantic import BaseModel, Field, field_validator, ConfigDict
from pydantic_core.core_schema import ValidationInfo

from constants.roles import Roles


class RegisterUserRequest(BaseModel):
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    password: str = Field(..., min_length=1, max_length=20)
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Passwords must match")

    @field_validator("passwordRepeat")
    @classmethod
    def validate_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Passwords must match")
        return value


class RegisterUserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles]
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


class UserInLoginResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    roles: list[Roles]
    verified: bool | None = None
    banned: bool | None = None


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")

    user: UserInLoginResponse
    accessToken: str
    expiresIn: int