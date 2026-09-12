from aiohttp import web
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from typing import Any

from src.utils.error import generate_error
from src.db import AsyncSession, Base


async def add_item(session: type[AsyncSession], item: Base):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError:
        raise generate_error(web.HTTPUnprocessableEntity,
                             f'{item.__tablename__} already exist')


async def delete_item(session: type[AsyncSession], item: Base):
    await session.delete(item)
    await session.commit()


async def get_item_by_id(session: type[AsyncSession], model: type[Base],
                         item_id: int) -> Base:
    item = await session.get(model, item_id)
    if not item:
        raise generate_error(web.HTTPNotFound,
                             f'{model.__tablename__} not found')
    return item


async def get_item_by_filter(session: type[AsyncSession], model: type[Base],
                             filter_by: dict[str, Any]) -> Base:
    query = select(model).filter_by(**filter_by)

    coro = await session.execute(query)

    return coro.scalars().first()


async def get_group(session: type[AsyncSession], model: type[Base]) -> list[Base]:
    query = select(model)

    coro = await session.scalars(query)

    return coro.all()
