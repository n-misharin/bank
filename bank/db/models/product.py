from sqlalchemy import Column, FLOAT, String, TEXT, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from bank.db import Base


class Product(Base):
    __tablename__ = "products"
    __table_args__ = (
        CheckConstraint("cost >= 0"),
    )

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=func.gen_random_uuid(),
    )

    title = Column(
        "title",
        String(50),
        index=True,
        nullable=False,
    )

    cost = Column(
        "cost",
        FLOAT,
        nullable=False,
    )

    description = Column(
        "description",
        TEXT,
        nullable=True,
    )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "title": self.title,
            "cost": str(self.cost),
            "description": self.description,
        }
