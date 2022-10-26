from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bank.utils.biil.database import get_bill, add_amount


async def can_write_off(session: AsyncSession, bill_id: UUID, amount: float) -> bool:
    bill = await get_bill(session, bill_id)
    return bill.balance >= amount


async def write_off(session: AsyncSession, bill_id: UUID, amount: float) -> None:
    bill = await get_bill(session, bill_id)
    if not bill:
        raise Exception(f"Incorrect bill id: `{bill_id}`.")
    try:
        await add_amount(session, bill_id, -amount)
    except Exception as exc:
        raise Exception("?")
