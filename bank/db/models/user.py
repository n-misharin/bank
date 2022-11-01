import enum

from sqlalchemy import Column, String, Enum, BOOLEAN, TEXT
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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

    username = Column(
        "username",
        String(50),
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

    bills = relationship("Bill", back_populates="owner", lazy="selectin")

    def to_dict(self) -> dict:

        return {
            "id": str(self.id),
            "login": self.username,
            "role": str(self.role.value),
            "hash_password": str(self.hash_password),
            "confirmed": str(self.confirmed),
            "bills": [bill.to_dict() for bill in self.bills]
        }
