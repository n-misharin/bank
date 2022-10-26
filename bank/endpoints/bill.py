from uuid import UUID

from Crypto.Hash import SHA1
from sanic import Request, HTTPResponse, Blueprint, json, exceptions
from sanic_ext import validate

from bank.config.config import DefaultConfig
from bank.schemas.bill.bill import AddAmountRequest
from bank.utils.biil.bill import credit_to
from bank.utils.biil.database import get_bills_by_user_id, BaseInvalidDataError, get_bill_history
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


@bp.get("/history/<bill_id:uuid>")
@protected
async def get_history(request: Request, bill_id: UUID) -> HTTPResponse:
    bills = await get_bills_by_user_id(request.ctx.session, request.ctx.cur_user.id)
    if bill_id not in [bill.id for bill in bills]:
        raise exceptions.Forbidden("Processing denied.")

    result = await get_bill_history(request.ctx.session, bill_id)

    return json({
        "items": [transaction.to_dict() for transaction in result]
    })


@bp.post("/payment/webhook")
@validate(json=AddAmountRequest)
async def add_amount(request: Request, body: AddAmountRequest) -> HTTPResponse:
    signature = SHA1.new(
        f'{DefaultConfig.SECRET}:{body.transaction_id}:{body.user_id}:{body.bill_id}:{body.amount}'.encode()
    )
    if signature.hexdigest() != body.signature:
        raise exceptions.BadRequest("Invalid data.")
    try:
        await credit_to(request.ctx.session, body.bill_id, body.user_id, body.amount)
    except BaseInvalidDataError as exc:
        raise exceptions.BadRequest(str(exc))

    return json({
        "message": "Accepted."
    })
