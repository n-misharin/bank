import datetime

from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from sanic import Request, HTTPResponse, Blueprint, json, exceptions
from sanic_ext import validate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bank.config.config import DefaultConfig
from bank.db.models import User
from bank.schemas.auth.authentication import UserAuthenticationRequest, UserAuthenticationResponse
from bank.schemas.auth.registration import UserRegistrationRequest, UserRegistrationResponse
from bank.utils.user.user import authenticate_user, create_token, register_user


bp = Blueprint("user")


@bp.get("/")
async def index(request: Request) -> HTTPResponse:
    session: AsyncSession = request.ctx.session
    async with session.begin():
        stmt = select(User)
        result = await session.execute(stmt)
    return json(result.scalar().to_dict())


@bp.post("/authentication")
@validate(json=UserAuthenticationRequest)
async def auth(request: Request, body: UserAuthenticationRequest) -> HTTPResponse:
    user = await authenticate_user(request.ctx.session, body.username, body.password)
    if not user:
        raise exceptions.Unauthorized("Invalid username or password.")

    access_token_delta = datetime.timedelta(minutes=DefaultConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token({"username": user.username}, access_token_delta)

    response = UserAuthenticationResponse(
        access_token=access_token,
        token_type="bearer"
    )
    return json(response.dict())


@bp.post("/registration")
@validate(json=UserRegistrationRequest)
async def registration(request: Request, body: UserRegistrationRequest) -> HTTPResponse:
    is_registered = await register_user(request.ctx.session, body.username, body.password)
    if not is_registered:
        raise exceptions.BadRequest("Username already exists.")

    serializer = URLSafeTimedSerializer(DefaultConfig.SECRET)
    confirmed_token = serializer.dumps(body.username, DefaultConfig.SECURITY_PASSWORD_SALT)

    # TODO: beautiful url
    response = UserRegistrationResponse(
        confirmed_url=f"http://{request.host}/confirm/{confirmed_token}"
    )
    return json(response.dict())


@bp.get("/confirm/<token:str>", name="confirm")
async def confirm(request: Request, token: str) -> HTTPResponse:
    serializer = URLSafeTimedSerializer(DefaultConfig.SECRET)
    try:
        # TODO: username == user.username?
        username = serializer.loads(
            token,
            salt=DefaultConfig.SECURITY_PASSWORD_SALT,
            max_age=DefaultConfig.CONFIRM_TOKEN_EXPIRE_MINUTES * 60,
        )
    except SignatureExpired:
        raise exceptions.NotFound("Page not found.")

    return json({
        "message": "Accept."
    })
