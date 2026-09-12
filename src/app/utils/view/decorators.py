from functools import wraps
from aiohttp import web

from src.app.utils.token import get_user_id_by_token
from src.app.utils.view.request import get_request_info
from src.utils.error import generate_error
from src.db.repository import get_item_by_id


def owner_required(msg='You can only edit your own'):
    def decorator(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            user_id = get_user_id_by_token(self.request)
            item_id = int(get_request_info(self.request, 'id'))

            item = await get_item_by_id(self.request.session, self.model, item_id)

            if self.owner_attr_name:
                item_owner_id = getattr(item, self.owner_attr_name)
                if item_owner_id != user_id:
                    raise generate_error(web.HTTPForbidden,
                                         f'{msg}, {self.model.__tablename__}')

            return await func(self, item, *args, **kwargs)

        return wrapper

    return decorator
