from src.db.models.users import User
from src.app.serializer.validate import UserValidator
from src.app.utils.view.patterns import BaseTokenItemView, BaseItemView


class UserTokenItemView(BaseTokenItemView):
    model = User
    validator = UserValidator


class UserItemView(BaseItemView):
    model = User
    validator = UserValidator
