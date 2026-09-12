from aiohttp import web
from pydantic import ValidationError

from src.utils.error import generate_error
from src.app.serializer.schema.ads import (AdvertisementCreate,
                                           AdvertisementReplace,
                                           AdvertisementUpdate)
from src.app.serializer.schema.users import (UserLogin, UserCreate,
                                             UserReplace, UserUpdate)


def validate_model(data: dict, model):
    try:
        model.model_validate(data)
    except ValidationError as ex:
        raise generate_error(web.HTTPBadRequest, ex.json())


class UserValidator:
    @staticmethod
    def login(data: dict):
        validate_model(data, UserLogin)

    @staticmethod
    def create(data: dict):
        validate_model(data, UserCreate)

    @staticmethod
    def replace(data: dict):
        validate_model(data, UserReplace)

    @staticmethod
    def modify(data: dict):
        validate_model(data, UserUpdate)


class AdvertisementValidator:
    @staticmethod
    def create(data: dict):
        validate_model(data, AdvertisementCreate)

    @staticmethod
    def replace(data: dict):
        validate_model(data, AdvertisementReplace)

    @staticmethod
    def modify(data: dict):
        validate_model(data, AdvertisementUpdate)
