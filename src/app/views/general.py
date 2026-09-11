from aiohttp import web

from src.app.error import generate_error
from src.app.serializer.validate import generate_validator
from src.app.token import create_access_token
from src.db.models.users import User


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
