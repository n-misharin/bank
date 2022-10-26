from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bank.utils.biil.database import get_bill, add_amount, InsufficientFundsError, BaseInvalidDataError, \
    InvalidOwnerError, InvalidBillError
from bank.utils.user.database import get_user_by_id


async def can_write_off(session: AsyncSession, bill_id: UUID, amount: float) -> bool:
    bill = await get_bill(session, bill_id)
    return bill.balance >= amount


async def write_off(session: AsyncSession, bill_id: UUID, amount: float) -> None:
    if not can_write_off(session, bill_id, amount):
        raise InsufficientFundsError("Insufficient funds.")
    if amount < 0:
        raise BaseInvalidDataError("Invalid amount.")
    await add_amount(session, bill_id, -amount)


async def credit_to(session: AsyncSession, bill_id: UUID, user_id: UUID, amount: float) -> None:
    if amount < 0:
        raise BaseInvalidDataError("Invalid amount.")
    bill = await get_bill(session, bill_id)
    if bill is None:
        raise InvalidBillError(f"Invalid bill_id = `{bill_id}`.")
    if bill.owner_id != user_id:
        raise InvalidOwnerError(f"Invalid owner_id = `{user_id}`")

    await add_amount(session, bill_id, amount)
