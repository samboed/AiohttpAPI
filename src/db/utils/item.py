from sqlalchemy import Column, inspect

from src.db import Base


def check_modification_column_right(column: Column):
    no_update = column.info.get('no_update', False)

    if (column.primary_key or
        column.default or
        column.server_default or
        no_update):
        return False

    return True


def replace_item(item: Base, data: dict):
    mapper = inspect(item).mapper

    for column in mapper.columns:
        if not check_modification_column_right(column):
            continue

        if column.name in data:
            setattr(item, column.name, data[column.name])
        else:
            setattr(item, column.name, None)


def modify_item(item: Base, data: dict):
    mapper = inspect(item).mapper

    for column in mapper.columns:
        if not check_modification_column_right(column):
            continue

        if column.name in data:
            setattr(item, column.name, data[column.name])
