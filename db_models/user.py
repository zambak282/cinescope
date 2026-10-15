import enum
from typing import Any, Dict

from sqlalchemy import Column, String, DateTime, Boolean, ARRAY, Enum
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class RoleEnum(str, enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"


class UserDBModel(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String)
    full_name = Column(String)
    password = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    verified = Column(Boolean)
    banned = Column(Boolean)
    roles = Column(ARRAY(Enum(RoleEnum, name="Role", create_type=False)))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "password": self.password,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "verified": self.verified,
            "banned": self.banned,
            "roles": self.roles,
        }

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}')>"