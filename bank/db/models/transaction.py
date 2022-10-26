from sqlalchemy import Column, FLOAT, INTEGER, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from bank.db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        "id",
        INTEGER,
        primary_key=True,
        autoincrement=True,
    )

    amount = Column(
        "amount",
        FLOAT,
        nullable=False,
    )

    bill_id = Column(
        "bill_id",
        UUID(as_uuid=True),
        ForeignKey("bills.id"),
        nullable=False,
    )
