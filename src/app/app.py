from aiohttp import web
from aiohttp_jwt import JWTMiddleware

from src.app.middleware import (session_middleware,
                                error_handler_middleware)
from src.app.token import JWA
from src.app.routes import setup_routes
from src.db import init_orm, close_orm
from src.config import JWT_SECRET_KEY


async def orm_context(app: web.Application):
    await init_orm()
    yield
    await close_orm()


def create_app() -> web.Application:
    app = web.Application(
        middlewares=[
            error_handler_middleware,
            JWTMiddleware(JWT_SECRET_KEY, algorithms=JWA,
                          credentials_required=False),
            session_middleware
        ]
    )

    app.cleanup_ctx.append(orm_context)

    setup_routes(app)

    return app
