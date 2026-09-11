from aiohttp import web

from src.app.views.general import login

routes = [
    web.post(r'/login', login)
]
