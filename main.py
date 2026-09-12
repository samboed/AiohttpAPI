from aiohttp import web

from src.app import create_app
from src.config import APP_HOST, APP_PORT


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host=APP_HOST, port=APP_PORT)
