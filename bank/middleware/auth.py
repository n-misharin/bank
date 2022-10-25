from functools import wraps

from sanic import Request, text

import jwt


def check_token(request: Request) -> bool:
    if not request.token:
        return False

    try:
        result = jwt.decode(request.token, request.app.config.SECRET, algorithms=["HS256"])
        # result["user"]
    except jwt.exceptions.InvalidTokenError:
        return False

    return True


def protected(wrapped):
    def decorator(func):
        @wraps(func)
        async def decorated_function(request: Request, *args, **kwargs):
            if check_token(request):
                response = await func(request, *args, **kwargs)
                return response

            return text("You are unauthorized.", 401)

        return decorated_function

    return decorator(wrapped)
