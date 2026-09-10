from aiohttp import web
from src.api.error import generate_error
from src.db.models import User, Advertisement
from src.api.serializer.schema.advertisement import (AdvertisementCreate,
                                                     AdvertisementReplace,
                                                     AdvertisementUpdate)
from src.api.serializer.schema.user import (UserLogin, UserCreate,
                                            UserReplace, UserUpdate)
from pydantic import ValidationError


def validate_model(data: dict, model):
    try:
        model.model_validate(data)
    except ValidationError as ex:
        raise generate_error(web.HTTPBadRequest, ex.json())


class UserValidation:
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
    def update(data: dict):
        validate_model(data, UserUpdate)


class AdvertisementValidation:
    @staticmethod
    def create(data: dict):
        validate_model(data, AdvertisementCreate)

    @staticmethod
    def replace(data: dict):
        validate_model(data, AdvertisementReplace)

    @staticmethod
    def update(data: dict):
        validate_model(data, AdvertisementUpdate)


def generate_validator(model):
    if model is User:
        return UserValidation
    elif model is Advertisement:
        return AdvertisementValidation
    return None
