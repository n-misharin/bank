from sqlalchemy import Column, FLOAT, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from bank.db import Base


class Bill(Base):
    __tablename__ = "bills"
    __table_args__ = (
        CheckConstraint("balance >= 0"),
    )

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    balance = Column(
        "balance",
        FLOAT,
        nullable=False,
        default=0,
    )

    owner_id = Column(
        "owner_id",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
