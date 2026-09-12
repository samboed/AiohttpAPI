import datetime

import jwt
from aiohttp import web

from src.config import JWT_SECRET_KEY
from src.db import Base
from src.db.repository import get_item_by_id

JWA = 'HS256'


def get_user_id_by_token(request: web.Request) -> int:
    return int(request['payload'].get('sub'))


async def get_item_by_token(request: web.Request, model: Base):
    user_id = get_user_id_by_token(request)

    return await get_item_by_id(request.session, model, user_id)


def create_access_token(identity: str):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "sub": identity,
        "exp": current_datetime + datetime.timedelta(hours=1),
        "iat": current_datetime
    }

    return jwt.encode(payload, key=JWT_SECRET_KEY, algorithm=JWA)
