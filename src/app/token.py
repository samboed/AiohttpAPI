import datetime

import jwt
from aiohttp import web

from src.config import JWT_SECRET_KEY


def get_user_id_from_token(request: web.Request) -> int:
    return int(request['payload'].get('sub'))


def create_access_token(identity: str):
    current_datetime = datetime.datetime.now(datetime.timezone.utc)

    payload = {
        "sub": identity,
        "exp": current_datetime + datetime.timedelta(hours=1),
        "iat": current_datetime
    }

    return jwt.encode(payload, key=JWT_SECRET_KEY, algorithm=JWA)


JWA = 'HS256'
