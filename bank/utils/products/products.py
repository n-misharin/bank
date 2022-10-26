from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bank.utils.biil.bill import write_off
from bank.utils.biil.database import get_bill, BaseInvalidDataError, InvalidBillError
from bank.utils.products.database import get_product


class InvalidProductError(BaseInvalidDataError):
    pass


class InvalidOwnerError(BaseInvalidDataError):
    pass


async def buy_product(
        session: AsyncSession,
        product_id: UUID,
        bill_id: UUID,
        user_id: UUID,
) -> None:
    bill = await get_bill(session, bill_id)
    if bill is None:
        raise InvalidBillError(f"Invalid bill_id = `{bill_id}`.")
    if bill.owner_id != user_id:
        raise InvalidOwnerError(f"Invalid owner_id = `{user_id}`")

    product = await get_product(session, product_id)
    if product is None:
        raise InvalidProductError(f"Invalid product_id = `{product_id}`.")

    await write_off(session, bill_id, product.cost)
