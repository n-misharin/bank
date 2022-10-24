from sanic import text, Request, HTTPResponse, Blueprint, json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bank.db.models import User

bp = Blueprint("user")


@bp.get("/")
async def index(request: Request) -> HTTPResponse:
    session: AsyncSession = request.ctx.session
    async with session.begin():
        stmt = select(User)
        result = await session.execute(stmt)
    return json(result.scalar().to_dict())


@bp.post("/auth")
async def auth(request: Request) -> HTTPResponse:
    return json({
        "token": None,
    })


@bp.post("/registration")
async def registration(request: Request) -> HTTPResponse:
    return json({

    })
