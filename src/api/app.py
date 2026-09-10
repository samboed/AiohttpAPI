from aiohttp import web
from aiohttp_jwt import JWTMiddleware

from src.api.middleware import session_middleware, error_handler_middleware
from src.api.token import JWA
from src.api.view.views import (login, UserTokenItemView, UserGroupView,
                                AdvertisementGroupView, AdvertisementItemView)

from src.config import JWT_SECRET_KEY

routes = web.RouteTableDef()


app = web.Application(
    middlewares=[
        error_handler_middleware,
        JWTMiddleware(JWT_SECRET_KEY, algorithms=JWA, credentials_required=False),
        session_middleware
    ])


app.router.add_route('POST', '/login', login)
app.router.add_view(r'/user', UserTokenItemView)
app.router.add_view(r'/user/create', UserGroupView)
app.router.add_view(r'/ads', AdvertisementGroupView)
app.router.add_view(r'/ads/{id:\d+}', AdvertisementItemView)
