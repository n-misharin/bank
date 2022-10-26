from datetime import timedelta, datetime
from functools import wraps

import jwt
from sanic import Request, exceptions
from sqlalchemy.ext.asyncio import AsyncSession

from bank.config.config import DefaultConfig
from bank.db.models import User
from bank.utils.user.database import get_user, add_user


def create_token(data: dict, expire_delta: timedelta) -> str:
    expire = datetime.utcnow() + expire_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, DefaultConfig.SECRET, algorithm=DefaultConfig.JWT_ALGORITHM)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return DefaultConfig.PWD_CONTEXT.verify(plain_password, hash_password)


async def authenticate_user(session: AsyncSession, username: str, password: str) -> User | None:
    # TODO: What to do for not confirmed user?
    user = await get_user(session, username)
    if not user:
        return None

    if not verify_password(password, user.hash_password):
        return None

    return user


async def register_user(session: AsyncSession, username: str, password: str) -> bool:
    hash_password = DefaultConfig.PWD_CONTEXT.hash(password)
    is_inserted = await add_user(session, username, hash_password)
    return is_inserted


def check_token(token: str) -> tuple[bool, dict | None]:
    if token is None:
        return False, None

    try:
        decode_result = jwt.decode(token, DefaultConfig.SECRET, algorithms=[DefaultConfig.JWT_ALGORITHM])
    except jwt.exceptions.InvalidTokenError:
        return False, None

    return True, decode_result


async def get_current_user(session: AsyncSession, token: str) -> User:
    is_valid, decode_result = check_token(token)
    if not is_valid or decode_result is None:
        raise exceptions.Unauthorized(f"Could not validate credentials.")

    user_login = decode_result.get("username", None)

    if user_login is None:
        raise exceptions.Unauthorized("Could not validate credentials.")

    user = await get_user(session, user_login)
    if user is None:
        raise exceptions.Unauthorized("Could not validate credentials.")

    return user


def protected(wrapped):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):
            is_correct, _ = check_token(request.token)
            if is_correct:
                return await func(request, *args, **kwargs)

            raise exceptions.Unauthorized("Auth required.")

        return decorated_function

    return decorator(wrapped)
