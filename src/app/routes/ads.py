from aiohttp import web

from src.app.views.ads import AdvertisementGroupView, AdvertisementItemView

routes = [
    web.get(r'/ads', AdvertisementGroupView),
    web.get(r'/ads/{id:\d+}', AdvertisementItemView),
    web.post(r'/ads', AdvertisementGroupView),
    web.put(r'/ads/{id:\d+}', AdvertisementItemView),
    web.patch(r'/ads/{id:\d+}', AdvertisementItemView),
    web.delete(r'/ads/{id:\d+}', AdvertisementItemView)
]
