from aiohttp import web
from aiohttp_jwt import login_required

from src.app.utils.view.decorators import owner_required
from src.app.utils.view.request import get_request_info
from src.app.utils.token import get_user_id_by_token, get_item_by_token
from src.db.repository import get_item_by_id, add_item, delete_item, get_group
from src.db.utils.item import replace_item, modify_item


class BaseItemView(web.View):
    model = None
    validator = None
    owner_attr_name = None

    async def get(self):
        item_id = int(get_request_info(self.request, 'id'))

        item = await get_item_by_id(self.request.session, self.model, item_id)

        return web.json_response(await item.dict)

    async def post(self):
        json_data = await self.request.json()

        self.validator.create(json_data)

        item = self.model(**json_data)
        await add_item(self.request.session, item)

        return web.json_response(await item.dict)

    @login_required
    @owner_required()
    async def put(self, item):
        json_data = await self.request.json()

        self.validator.replace(json_data)

        replace_item(item, json_data)
        await add_item(self.request.session, item)

        return web.json_response(await item.dict)

    @login_required
    @owner_required()
    async def patch(self, item):
        json_data = await self.request.json()

        self.validator.modify(json_data)

        modify_item(item, json_data)
        await add_item(self.request.session, item)

        return web.json_response(await item.dict)

    @login_required
    @owner_required(msg='You can only delete your own')
    async def delete(self, item):
        await delete_item(self.request.session, item)

        return web.Response(status=204)


class BaseGroupView(web.View):
    model = None
    validator = None
    owner_attr_name = None

    async def get(self):
        item_group = await get_group(self.request.session, self.model)

        return web.json_response([await item.dict for item in item_group])

    @login_required
    async def post(self):
        user_id = get_user_id_by_token(self.request)
        json_data = await self.request.json()

        self.validator.create(json_data)

        item = self.model(**json_data)
        if self.owner_attr_name:
            setattr(item, self.owner_attr_name, user_id)
        await add_item(self.request.session, item)

        return web.json_response(await item.dict)


class BaseTokenItemView(web.View):
    model = None
    validator = None
    owner_attr_name = None

    @login_required
    async def get(self):
        item = await get_item_by_token(self.request, self.model)

        return web.json_response(await item.dict)

    @login_required
    async def post(self):
        json_data = await self.request.json()

        self.validator.create(json_data)

        item = self.model(**json_data)
        await add_item(self.request.session, item)

        return web.json_response(await item.dict)

    @login_required
    async def put(self):
        json_data = await self.request.json()
        item = await get_item_by_token(self.request, self.model)

        self.validator.replace(json_data)

        replace_item(item, json_data)
        await add_item(self.request.session, item)

        return web.json_response(await item.dict)

    @login_required
    async def patch(self):
        json_data = await self.request.json()
        item = await get_item_by_token(self.request, self.model)

        self.validator.modify(json_data)

        modify_item(item, json_data)
        await add_item(self.request.session, item)

        return web.json_response(await item.dict)

    @login_required
    async def delete(self):
        user = await get_item_by_token(self.request, self.model)

        await delete_item(self.request.session, user)

        return web.json_response()
