import enum

from sqlalchemy import Column, TEXT, Enum, BOOLEAN
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from bank.config.config import DefaultConfig
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

    username = Column(
        "username",
        TEXT,
        unique=True,
        index=True,
        nullable=False,
    )

    hash_password = Column(
        "hash_password",
        TEXT,
        nullable=False,
    )

    role = Column(
        "role",
        Enum(UserRoleEnum),
        default=UserRoleEnum.USER,
        nullable=False,
    )

    confirmed = Column(
        "confirmed",
        BOOLEAN,
        default=False,
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "login": self.username,
            "role": str(self.role.value),
            "hash_password": str(self.hash_password)
        }
