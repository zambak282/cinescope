import datetime

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo

from constants.roles import Roles


class UserModel(BaseModel):
    email: str
    fullName: str
    password: str = Field(..., min_length=1, max_length=20)
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Passwords must match")
    roles: list[Roles] = [Roles.USER] # мб тут ошибка
    verified: bool | None
    banned: bool | None

    @field_validator("passwordRepeat")
    @classmethod
    def validate_passwords_match(cls, value: str, info: ValidationInfo) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Passwords must match")
        return value


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    roles: list[Roles]
    verified: bool
    banned: bool
    createdAt: str

    @field_validator("createdAt")
    @classmethod
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("CreatedAt must be a date")
        return value