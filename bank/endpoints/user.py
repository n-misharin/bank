import datetime

import jwt
from sanic import text, Request, HTTPResponse, Blueprint, json
from sanic_ext import validate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import User
from bank.middleware.auth import protected
from bank.schemas.auth.registration import RegistrationUserForm

bp = Blueprint("user")


@bp.get("/")
async def index(request: Request) -> HTTPResponse:
    session: AsyncSession = request.ctx.session
    async with session.begin():
        stmt = select(User)
        result = await session.execute(stmt)
    return json(result.scalar().to_dict())


@bp.post("/auth")
@protected
async def auth(request: Request) -> HTTPResponse:
    return json({
        "token": request.token,
    })


@bp.post("/registration")
@validate(json=RegistrationUserForm)
async def registration(request: Request, body: RegistrationUserForm) -> HTTPResponse:
    return json({
        "token": jwt.encode({
            "user": "nd-misharin1",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=2),
        }, request.app.config.SECRET)
    })
