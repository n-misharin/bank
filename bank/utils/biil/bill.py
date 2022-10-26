from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bank.utils.biil.database import get_bill, add_amount, InsufficientFundsError


async def can_write_off(session: AsyncSession, bill_id: UUID, amount: float) -> bool:
    bill = await get_bill(session, bill_id)
    return bill.balance >= amount


async def write_off(session: AsyncSession, bill_id: UUID, amount: float) -> None:
    if not can_write_off(session, bill_id, amount):
        raise InsufficientFundsError("Insufficient funds.")
    await add_amount(session, bill_id, -amount)
