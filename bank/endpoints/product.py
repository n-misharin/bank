from uuid import UUID

from sanic import Request, HTTPResponse, Blueprint, json, exceptions
from sanic_ext import validate

from bank.db.models import User, UserRoleEnum
from bank.schemas.product.products import BuyProductRequest, BuyProductResponse, AddProductRequest, UpdateProductRequest
from bank.utils.biil.database import BaseInvalidDataError, InsufficientFundsError
from bank.utils.products.database import get_all_products, remove_product, get_product, insert_product, update_product
from bank.utils.products.products import buy_product
from bank.utils.user.user import protected

bp = Blueprint("product")


@bp.get("/products/list")
@protected()
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
@protected()
async def buy(request: Request, body: BuyProductRequest) -> HTTPResponse:
    cur_user: User = request.ctx.cur_user
    try:
        await buy_product(request.ctx.session, body.product_id, body.bill_id, cur_user.id)
    except InsufficientFundsError as exc:
        raise exceptions.BadRequest(str(exc))
    except BaseInvalidDataError as exc:
        raise exceptions.BadRequest(str(exc))
    response = BuyProductResponse(message="Accepted.")

    return json(response.dict())


@bp.post("/product")
@protected(only=[UserRoleEnum.USER])
@validate(json=AddProductRequest)
async def add_product(request: Request, body: AddProductRequest) -> HTTPResponse:
    try:
        product = await insert_product(request.ctx.session, body)
    except Exception:
        raise exceptions.BadRequest("Invalid data.")

    return json({
        "message": "Accepted.",
        "product": product.to_dict(),
    })


@bp.put("/product/<product_id:uuid>")
@validate(json=UpdateProductRequest)
@protected(only=[UserRoleEnum.USER])
async def put_product(request: Request, product_id: UUID, body: UpdateProductRequest) -> HTTPResponse:
    try:
        await update_product(request.ctx.session, body, product_id)
    except Exception:
        raise exceptions.BadRequest("Invalid data.")

    return json({
        "message": "Accepted.",
    })


@bp.delete("/product/<product_id:uuid>")
@protected(only=[UserRoleEnum.ADMIN])
async def delete_product(request: Request, product_id: UUID) -> HTTPResponse:
    product = await get_product(request.ctx.session, product_id)
    if product is None:
        raise exceptions.NotFound("Product not found.")
    await remove_product(request.ctx.session, product_id)

    return json({
        "message": "Accepted."
    })
