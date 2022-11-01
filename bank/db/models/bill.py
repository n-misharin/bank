from sqlalchemy import Column, FLOAT, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
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
        ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    owner = relationship("User", back_populates="bills")

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "balance": str(self.balance),
            "owner_id": str(self.owner_id)
        }
