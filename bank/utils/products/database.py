from uuid import UUID

from sqlalchemy import select, exc, update
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import Product


async def get_product(session: AsyncSession, product_id: UUID) ->  Product:
    result = await session.scalar(select(Product).where(Product.id == product_id))
    return result


async def get_all_products(session: AsyncSession) -> list[Product]:
    result = await session.scalars(select(Product))
    return result.all()
