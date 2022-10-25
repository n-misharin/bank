import enum

from sqlalchemy import Column, TEXT, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from bank.db import Base


class UserRoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    login = Column(
        "login",
        TEXT,
        unique=True,
        index=True,
        nullable=False,
    )

    role = Column(
        "role",
        Enum(UserRoleEnum),
        nullable=False,
    )

    def to_dict(self):
        # TODO:
        return {
            "id": str(self.id),
            "login": self.login,
            "role": str(self.role.value),
        }
