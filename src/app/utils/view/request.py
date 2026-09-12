from aiohttp import web


def get_request_info(request: web.Request, key: str):
    return request.match_info.get(key)
