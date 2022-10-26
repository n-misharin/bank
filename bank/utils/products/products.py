from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from bank.utils.biil.bill import write_off
from bank.utils.biil.database import get_bill
from bank.utils.products.database import get_product


async def buy_product(
        session: AsyncSession,
        product_id: UUID,
        bill_id: UUID,
        user_id: UUID,
) -> None:
    product = await get_product(session, product_id)
    bill = await get_bill(session, bill_id)
    if bill.owner_id != user_id:
        raise Exception("Incorrect owner.")

    await write_off(session, bill_id, product.cost)
