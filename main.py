from aiohttp import web

from src.app.app import create_app


if __name__ == '__main__':
    app = create_app()
    web.run_app(app, host='127.0.0.1', port=5000)
