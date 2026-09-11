from aiohttp import web

from src.app.views.users import UserTokenItemView, UserItemView

routes = [
        web.get(r'/user', UserTokenItemView),
        web.post(r'/user', UserItemView),
        web.patch(r'/user', UserTokenItemView),
        web.put(r'/user', UserTokenItemView),
        web.delete(r'/user', UserTokenItemView),
]
