from contextvars import ContextVar

from sanic import Sanic, Request
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from bank.config.config import get_config
from bank.endpoints import routes_list
from bank.utils.user.user import get_current_user


def bind_routes(application: Sanic) -> None:
    for route in routes_list:
        application.blueprint(route)


def connect_database(application: Sanic, con_uri: str) -> None:
    bind = create_async_engine(con_uri)
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


app_config = get_config()
app = Sanic("App", config=app_config)
bind_routes(app)
connect_database(app, app_config.get_db_uri())


@app.middleware("request")
async def inject_current_user(request: Request):
    request.ctx.cur_user = None
    if request.path == "/authentication":
        return
    if request.headers.get("Authorization", None) is None:
        return
    scheme, token = request.headers.get("Authorization").split(" ")
    is_bearer_auth = scheme.lower() == "bearer" and token is not None
    if is_bearer_auth:
        request.ctx.cur_user = await get_current_user(request.ctx.session, request.token)


if __name__ == "__main__":
    app.run(
        host=app_config.APP_HOST,
        port=app_config.APP_PORT,
        dev=app_config.DEBUG,
        debug=app_config.DEBUG,
    )
