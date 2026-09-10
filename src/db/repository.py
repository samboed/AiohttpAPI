from aiohttp import web
from sqlalchemy.exc import IntegrityError

from src.api.error import generate_error
from src.db.models import Session


def add_item(session: Session, item):
    session.add(item)
    try:
        session.commit()
    except IntegrityError:
        raise generate_error(web.HTTPUnprocessableEntity,
                             f'{item.__tablename__} already exist')


def get_item(session: Session, model, item_id):
    item = session.get(model, item_id)
    if not item:
        raise generate_error(web.HTTPNotFound,
                             f'{model.__tablename__} not found')
    return item


def get_group(session: Session, model):
    return session.query(model).all()


def delete_item(session: Session, item):
    session.delete(item)
    session.commit()
