from bank.endpoints.user import bp as user_blueprint
from bank.endpoints.product import bp as product_blueprint

routes_list = [
    user_blueprint,
    product_blueprint,
]

__all__ = [
    "routes_list",
]
