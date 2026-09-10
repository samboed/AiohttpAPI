from aiohttp import web

from src.api.app import app
from src.db.models import create_tables


if __name__ == '__main__':
    create_tables()
    web.run_app(app, host='127.0.0.1', port='5000')
