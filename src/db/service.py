import bcrypt
from sqlalchemy import inspect


def replace_item(instance, data: dict):
    mapper = inspect(instance).mapper

    for column in mapper.columns:
        no_update = column.info.get('no_update', False)
        if (column.primary_key or column.default or
                column.server_default or no_update):
            continue

        if column.name in data:
            setattr(instance, column.name, data[column.name])
        else:
            setattr(instance, column.name, None)


def update_item(instance, data: dict):
    mapper = inspect(instance).mapper

    for column in mapper.columns:
        no_update = column.info.get('no_update', False)
        if (column.primary_key or column.default or
                column.server_default or no_update):
            continue

        if column.name in data:
            setattr(instance, column.name, data[column.name])


def hash_password(raw_password: bytes) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(raw_password, salt)
