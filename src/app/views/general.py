from aiohttp import web

from src.utils.error import generate_error
from src.app.serializer.validate import UserValidator
from src.app.utils.token import create_access_token
from src.db.models.users import User
from src.db.repository import get_item_by_filter


async def login(request):
    validator = UserValidator

    data = await request.json()

    validator.login(data)

    user = await get_item_by_filter(request.session, User,
                                    {'login': data['login']})
    if not user or not user.check_password(data['password']):
        raise generate_error(web.HTTPUnauthorized,
                             'login or password are incorrect')

    token = create_access_token(identity=str(user.id))

    return web.json_response({"access_token": token})
