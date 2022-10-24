from sanic import text, Request, HTTPResponse, Blueprint, json

bp = Blueprint("user")


@bp.get("/")
async def index(request: Request) -> HTTPResponse:
    return text("Hello, world.")


@bp.post("/auth")
async def login(request: Request) -> HTTPResponse:
    return json({
        "token": None,
    })


@bp.post("/registration")
async def login(request: Request) -> HTTPResponse:
    return json({

    })
