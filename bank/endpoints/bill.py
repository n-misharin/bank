from sanic import Request, HTTPResponse, Blueprint, json

from bank.utils.biil.database import get_bills_by_user_id
from bank.utils.user.user import protected

bp = Blueprint("bill")


@bp.get("/bills")
@protected
async def get_bills(request: Request) -> HTTPResponse:
    cur_user = request.ctx.cur_user
    session = request.ctx.session
    bills = await get_bills_by_user_id(session, cur_user.id)
    return json({
        "items": [bill.to_dict() for bill in bills],
    })



