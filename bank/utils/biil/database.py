from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import Bill, Transaction


class BaseInvalidDataError(Exception):
    pass


class InsufficientFundsError(Exception):
    pass


class InvalidBillError(BaseInvalidDataError):
    pass


async def get_bill(session: AsyncSession, bill_id: UUID) -> Bill:
    query = select(Bill).where(Bill.id == bill_id)
    result = await session.scalar(query)
    return result


async def add_amount(session: AsyncSession, bill_id: UUID, amount: float):
    query = update(Bill).where(Bill.id == bill_id).values({
        "balance": Bill.balance + amount
    })
    try:
        await session.execute(query)
    except IntegrityError:
        raise InsufficientFundsError("Insufficient funds.")

    try:
        transaction = Transaction(amount=amount, bill_id=bill_id)
        session.add(transaction)

        await session.commit()
    except IntegrityError:
        raise InvalidBillError(f"Invalid bill: id={bill_id}.")


async def get_bills_by_user_id(session: AsyncSession, user_id: UUID) -> list[Bill]:
    query = select(Bill).where(Bill.owner_id == user_id)
    result = await session.scalars(query)
    return [bill for bill in result.all()]
