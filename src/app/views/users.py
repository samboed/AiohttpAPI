from src.app.serializer.validate import generate_validator
from src.app.views.patterns import BaseTokenItemView, BaseItemView
from src.db.models.users import User


class UserTokenItemView(BaseTokenItemView):
    model = User
    validator = generate_validator(User)


class UserItemView(BaseItemView):
    model = User
    validator = generate_validator(User)
