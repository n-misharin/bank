from sanic import Request, HTTPResponse, Blueprint, json, exceptions

from bank.db.models.user import UserRoleEnum
from bank.utils.user.database import get_all_users, confirm_user
from bank.utils.user.user import protected

bp = Blueprint("admin", url_prefix="/admin")


@bp.get("/users")
@protected(only=[UserRoleEnum.ADMIN])
async def get_users(request: Request) -> HTTPResponse:
    users = await get_all_users(request.ctx.session)
    return json({
        "items": [user.to_dict() for user in users]
    })


@bp.put("/user/<username:str>/confirm")
@protected(only=[UserRoleEnum.USER])
async def confirm(request: Request, username: str) -> HTTPResponse:
    # TODO: валидация лоинов пользователей при записи в базу (на допустимые символы)
    try:
        is_confirm = await confirm_user(request.ctx.session, username)
        if not is_confirm:
            raise Exception("Invalid username.")
    except Exception:
        raise exceptions.BadRequest("Invalid username")
    return json({
        "message": "Accepted."
    })
