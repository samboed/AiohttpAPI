from aiohttp import web

from src.app.app import app
from src.app.views.users import (UserTokenItemView, UserItemView)
from src.app.views.general import login
from src.app.views.ads import AdvertisementItemView, AdvertisementGroupView

app.router.add_route('POST', '/login', login)

app.router.add_routes(
    [
        web.get(r'/user', UserTokenItemView),
        web.post(r'/user', UserItemView),
        web.patch(r'/user', UserTokenItemView),
        web.put(r'/user', UserTokenItemView),
        web.delete(r'/user', UserTokenItemView),
    ]
)
app.router.add_routes(
    [
        web.get(r'/ads', AdvertisementGroupView),
        web.post(r'/ads', AdvertisementGroupView),
        web.get(r'/ads/{id:\d+}', AdvertisementItemView),
        web.patch(r'/ads/{id:\d+}', AdvertisementItemView),
        web.put(r'/ads/{id:\d+}', AdvertisementItemView),
        web.delete(r'/ads/{id:\d+}', AdvertisementItemView),
    ]
)
