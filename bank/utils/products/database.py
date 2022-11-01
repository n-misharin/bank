from uuid import UUID

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import Product
from bank.schemas.product.products import AddProductRequest, UpdateProductRequest


async def get_product(session: AsyncSession, product_id: UUID) ->  Product:
    result = await session.scalar(select(Product).where(Product.id == product_id))
    return result


async def get_all_products(session: AsyncSession) -> list[Product]:
    result = await session.scalars(select(Product))
    return result.all()


async def remove_product(session: AsyncSession, product_id: UUID) -> None:
    query = delete(Product).where(Product.id == product_id)
    result = await session.execute(query)
    await session.commit()


async def insert_product(session: AsyncSession, data: AddProductRequest) -> Product:
    product = Product(**data.dict())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def update_product(session: AsyncSession, data: UpdateProductRequest, product_id: UUID) -> None:
    update_values = dict()
    for key, val in data.dict().items():
        if val is not None:
            update_values[key] = val
    query = update(Product).where(product_id == Product.id).values(update_values)
    await session.execute(query)
    await session.commit()
