from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import Bill


async def get_bill(session: AsyncSession, bill_id: UUID) -> Bill:
    query = select(Bill).where(Bill.id == bill_id)
    result = await session.scalar(query)
    return result


async def add_amount(session: AsyncSession, bill_id: UUID, amount: float):
    query = update(Bill).where(Bill.id == bill_id).values({
        "balance": Bill.balance + amount
    })
    await session.execute(query)
    await session.commit()


async def get_bills_by_user_id(session: AsyncSession, user_id: UUID) -> list[Bill]:
    query = select(Bill).where(Bill.owner_id == user_id)
    result = await session.scalars(query)
    return [bill for bill in result.all()]
