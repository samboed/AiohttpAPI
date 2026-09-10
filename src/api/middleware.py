from aiohttp import web
from jwt.exceptions import PyJWTError

from src.db.models import Session


@web.middleware
async def session_middleware(request: web.Request, handler):
    with Session() as session:
        request.session = session
        response = await handler(request)

    return response


@web.middleware
async def error_handler_middleware(request: web.Request, handler):
    try:
        response = await handler(request)
    except (web.HTTPException, PyJWTError) as ex:
        data = {
            'error': ex.__class__.__name__,
            'message': ex.text
        }
        return web.json_response(data=data, status=ex.status)

    return response
