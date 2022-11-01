from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import Bill, Transaction


class BaseInvalidDataError(Exception):
    pass


class InsufficientFundsError(BaseInvalidDataError):
    pass


class InvalidProductError(BaseInvalidDataError):
    pass


class InvalidOwnerError(BaseInvalidDataError):
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


async def get_bill_history(session: AsyncSession, bill_id: UUID) -> list[Transaction]:
    query = select(Transaction).where(Transaction.bill_id == bill_id)
    result = await session.scalars(query)
    return [transaction for transaction in result.all()]


async def add_bill(session: AsyncSession, user_id: UUID) -> Bill:
    new_bill = Bill(balance=0, owner_id=user_id)
    session.add(new_bill)
    try:
        await session.commit()
        await session.refresh(new_bill)
    except IntegrityError:
        raise InvalidOwnerError("Invalid owner.")
    return new_bill
