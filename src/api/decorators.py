from functools import wraps
from aiohttp import web

from src.db.repository import get_item
from src.api.token import get_user_id_from_token
from src.api.error import generate_error


def owner_required(msg='You can only edit your own'):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            item_id = self.request.match_info.get('id')
            user_id = int(get_user_id_from_token(self.request))

            item = get_item(self.request.session, self.model, item_id)

            item_owner_id = getattr(item, self.owner_attr_name)
            if item_owner_id != user_id:
                raise generate_error(web.HTTPForbidden,
                                     f'{msg}, {self.model.__tablename__}')
            return func(self, item, *args, **kwargs)

        return wrapper

    return decorator
