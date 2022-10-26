from contextvars import ContextVar

from sanic import Sanic, Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bank.config.config import DefaultConfig
from bank.endpoints import routes_list
from bank.utils.user.user import get_current_user


def create_app() -> Sanic:
    application = Sanic("MyApp", config=DefaultConfig())

    #  TODO: вынести строку подключения
    bind = create_async_engine("postgresql+asyncpg://user:hackme@localhost:5432/postgres")
    _sessionmaker = sessionmaker(bind, AsyncSession, expire_on_commit=False)
    _base_model_session_ctx = ContextVar("session")

    @application.middleware("request")
    async def inject_session(request: Request):
        request.ctx.session = _sessionmaker()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

    @application.middleware("request")
    async def inject_current_user(request: Request):
        if request.path == "/authentication":
            request.ctx.cur_user = None
        else:
            if not request.headers.get("Authorization", None):
                request.ctx.cur_user = None
            else:
                scheme, token = request.headers.get("Authorization").split(" ")
                if scheme.lower() == "bearer" and token:
                    request.ctx.cur_user = await get_current_user(request.ctx.session, request.token)
                else:
                    request.ctx.cur_user = None

    @application.middleware("response")
    async def close_session(request: Request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()

    for route in routes_list:
        application.blueprint(route)

    return application


app = create_app()
