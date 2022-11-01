from uuid import UUID

from sqlalchemy import select, exc, update
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import User


async def get_user(session: AsyncSession, username: str) -> User | None:
    query = select(User).where(User.username == username)
    return await session.scalar(query)


async def get_user_by_id(session: AsyncSession, user_id: UUID) -> User | None:
    query = select(User).where(User.id == user_id)
    return await session.scalar(query)


async def add_user(session: AsyncSession, username: str, hash_password: str) -> bool:
    user = User(username=username, hash_password=hash_password)
    session.add(user)
    try:
        await session.commit()
    except exc.IntegrityError:
        return False
    return True


async def confirm_user(session: AsyncSession, username: str) -> bool:
    user = await get_user(session, username)
    if not user:
        return False
    query = update(User).where(User.id == user.id).values(confirmed=True)

    await session.execute(query)
    await session.commit()

    return True


async def get_all_users(session: AsyncSession) -> list[User]:
    result = await session.scalars(select(User))
    return [user for user in result.all()]
