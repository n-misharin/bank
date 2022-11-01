from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bank.schemas.bill.bill import AddAmountRequest
from bank.utils.biil.database import get_bill, add_amount, InsufficientFundsError, BaseInvalidDataError, \
    InvalidOwnerError, InvalidBillError, add_bill
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


async def credit_to(session: AsyncSession, data: AddAmountRequest) -> None:
    if data.amount < 0:
        raise BaseInvalidDataError("Invalid amount.")

    user = await get_user_by_id(session, data.user_id)
    if user is None:
        raise InvalidOwnerError(f"Invalid owner_id = `{data.user_id}`")

    bill = await get_bill(session, data.bill_id)
    if bill is None:
        try:
            bill = await add_bill(session, data.user_id, bill_id=data.bill_id)
        except Exception:
            raise InvalidBillError(f"Invalid bill_id = `{data.bill_id}`.")

    await add_amount(session, data.bill_id, data.amount)
