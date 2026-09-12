from aiohttp import web


def generate_error(err_cls: type[web.HTTPException], msg: str):
    err_instance = err_cls()
    err_instance.text = msg
    return err_instance
