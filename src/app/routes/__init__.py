from aiohttp import web

from .general import routes as general_routes
from .users import routes as user_routes
from .ads import routes as ad_routes


def setup_routes(app: web.Application):
    api = web.Application()
    api.add_routes(user_routes)
    api.add_routes(ad_routes)

    app.add_subapp('/api/v1', api)

    app.add_routes(general_routes)
