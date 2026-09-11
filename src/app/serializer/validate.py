from aiohttp import web
from src.app.error import generate_error
from src.db.models.users import User
from src.db.models.ads import Advertisement
from src.app.serializer.schema.ads import (AdvertisementCreate,
                                           AdvertisementReplace,
                                           AdvertisementUpdate)
from src.app.serializer.schema.users import (UserLogin, UserCreate,
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
