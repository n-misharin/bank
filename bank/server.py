from contextvars import ContextVar

from sanic import Sanic, Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bank.endpoints import user_blueprint


def create_app() -> Sanic:
    application = Sanic("MyApp")
    application.config.update({
        "DB_HOST": "localhost",
        "DB_NAME": "postgres",
        "DB_USER": "user",
        "DB_PASSWORD": "hackme",
    })
    bind = create_async_engine("postgresql+asyncpg://user:hackme@localhost:5432/postgres")
    _sessionmaker = sessionmaker(bind, AsyncSession, expire_on_commit=False)
    _base_model_session_ctx = ContextVar("session")

    @application.middleware("request")
    async def inject_session(request: Request):
        request.ctx.session = _sessionmaker()
        request.ctx.session_ctx_token = _base_model_session_ctx.set(request.ctx.session)

    @application.middleware("response")
    async def close_session(request: Request, response):
        if hasattr(request.ctx, "session_ctx_token"):
            _base_model_session_ctx.reset(request.ctx.session_ctx_token)
            await request.ctx.session.close()

    application.blueprint(user_blueprint)
    return application


app = create_app()
