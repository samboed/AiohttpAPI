from aiohttp import web
from sqlalchemy.exc import IntegrityError

from src.app.error import generate_error
from src.db import AsyncSession


async def add_item(session: AsyncSession, item):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError:
        raise generate_error(web.HTTPUnprocessableEntity,
                             f'{item.__tablename__} already exist')


async def get_item(session: AsyncSession, model, item_id):
    item = await session.get(model, item_id)
    if not item:
        raise generate_error(web.HTTPNotFound,
                             f'{model.__tablename__} not found')
    return item


async def get_group(session: AsyncSession, model):
    return await session.query(model).all()


async def delete_item(session: AsyncSession, item):
    await session.delete(item)
    await session.commit()
