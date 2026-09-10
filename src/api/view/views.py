from aiohttp import web

from src.api.error import generate_error
from src.api.serializer.validation import generate_validator
from src.api.token import create_access_token
from src.api.view.patterns import BaseTokenItemView, BaseItemView, BaseGroupView
from src.db.models import User, Advertisement


class UserTokenItemView(BaseTokenItemView):
    model = User
    validator = generate_validator(User)

    post = None


class UserGroupView(BaseGroupView):
    model = User
    validator = generate_validator(User)

    get = None


class AdvertisementItemView(BaseItemView):
    model = Advertisement
    validator = generate_validator(Advertisement)
    owner_attr_name = 'owner_id'


class AdvertisementGroupView(BaseGroupView):
    model = Advertisement
    validator = generate_validator(Advertisement)
    owner_attr_name = 'owner_id'


async def login(request):
    data = await request.json()
    validator = generate_validator(User)
    validator.login(data)
    user = request.session.query(User).filter_by(login=data['login']).first()
    if user is None or not user.check_password(data['password']):
        raise generate_error(web.HTTPUnauthorized,
                             'login or password are incorrect')

    token = create_access_token(identity=str(user.id))

    return web.json_response({"access_token": token})
