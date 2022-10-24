from sanic import Sanic

from bank.endpoints import user_blueprint


def create_app() -> Sanic:
    application = Sanic("MyApp")
    application.config.update({
        "DB_HOST": "localhost",
        "DB_NAME": "postgres",
        "DB_USER": "user",
        "DB_PASSWORD": "hackme",
    })
    application.blueprint(user_blueprint)
    return application


app = create_app()
