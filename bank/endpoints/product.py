from sanic import Request, HTTPResponse, Blueprint, json, exceptions
from sanic_ext import validate

from bank.db.models import User
from bank.schemas.product.buy_product import BuyProductRequest
from bank.utils.products.database import get_all_products
from bank.utils.products.products import buy_product
from bank.utils.user.user import protected

bp = Blueprint("product")


@bp.get("/products/list")
@protected
async def get_products(request: Request) -> HTTPResponse:
    products = await get_all_products(request.ctx.session)
    return json({
        "items": [
            product.to_dict()
            for product in products
        ]
    })


@bp.post("products/buy")
@validate(json=BuyProductRequest)
@protected
async def buy(request: Request, body: BuyProductRequest) -> HTTPResponse:
    cur_user: User = request.ctx.cur_user
    try:
        await buy_product(request.ctx.session, body.product_id, body.bill_id, cur_user.id)
    except Exception:
        raise exceptions.BadRequest("Invalid data.")
    return json({
        "details": "Accepted."
    })
