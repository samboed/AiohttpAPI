from aiohttp import web
from aiohttp_jwt import login_required

from src.app.decorators import owner_required
from src.app.serializer.validate import generate_validator
from src.app.token import get_user_id_from_token
from src.db.repository import get_item, add_item, delete_item, get_group
from src.db.service import replace_item, update_item


class BaseItemView(web.View):
    model = None
    validator = None
    owner_attr_name = None

    async def get(self):
        item_id = self.request.match_info.get('id')
        item = get_item(self.request.session, self.model, item_id)
        return web.json_response(item.dict)

    async def post(self):
        json_data = await self.request.json()
        self.validator.create(json_data)
        item = self.model(**json_data)
        await add_item(self.request.session, item)
        return web.json_response(item.dict)

    @login_required
    @owner_required()
    async def put(self, item):
        json_data = await self.request.json()
        self.validator.replace(json_data)
        replace_item(item, json_data)
        await add_item(self.request.session, item)
        return web.json_response(item.dict)

    @login_required
    @owner_required()
    async def patch(self, item):
        json_data = await self.request.json()
        self.validator.update(json_data)
        update_item(item, json_data)
        await add_item(self.request.session, item)
        return web.json_response(item.dict)

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
        return web.json_response([item.dict for item in item_group])

    @login_required
    async def post(self):
        user_id = get_user_id_from_token(self.request)
        json_data = await self.request.json()
        self.validator.create(json_data)
        item = self.model(**json_data)
        if self.owner_attr_name:
            setattr(item, self.owner_attr_name, user_id)
        await add_item(self.request.session, item)
        return web.json_response(item.dict)


class BaseTokenItemView(web.View):
    model = None
    validator = None
    owner_attr = None

    async def _get_item_by_token(self):
        user_id = get_user_id_from_token(self.request)
        item = await get_item(self.request.session, self.model, user_id)
        return item

    @login_required
    async def get(self):
        item = await self._get_item_by_token()
        return web.json_response(item.dict)

    @login_required
    async def post(self):
        json_data = await self.request.json()
        self.validator.create(json_data)
        item = self.model(**json_data)
        await add_item(self.request.session, item)
        return web.json_response(item.dict)

    @login_required
    async def put(self):
        item = await self._get_item_by_token()
        json_data = await self.request.json()
        self.validator.replace(json_data)
        replace_item(item, json_data)
        await add_item(self.request.session, item)
        return web.json_response(item.dict)

    @login_required
    async def patch(self):
        item = await self._get_item_by_token()
        json_data = await self.request.json()
        self.validator.update(json_data)
        update_item(item, json_data)
        await add_item(self.request.session, item)
        return web.json_response(item.dict)

    @login_required
    async def delete(self):
        user = await self._get_item_by_token()
        await delete_item(self.request.session, user)
        return web.json_response()


def generate_custom_api_class(name, model, inherited_cls):
    return type(
        f"{name.capitalize()}API",
        (inherited_cls, ),
        {
            "model": model,
            "validator": generate_validator(model)
        }
    )
