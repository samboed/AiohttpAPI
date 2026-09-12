from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType

from src.db.models import Base
from src.utils.permission import hash_password, check_password

class User(Base):
    __tablename__ = 'user'

    login: Mapped[str] = mapped_column(String(30),
                                       unique=True)
    _password: Mapped[str] = mapped_column('password',
                                           String(128))
    email: Mapped[str] = mapped_column(EmailType,
                                       unique=True)
    name: Mapped[str] = mapped_column(String(60))
    last_name: Mapped[str] = mapped_column(String(60),
                                           nullable=True)

    advertisements: Mapped[list['Advertisement']] = (
        relationship(back_populates='owner'))

    def __init__(self, **kwargs):
        password = kwargs.pop('password', None)
        super().__init__(**kwargs)
        self.password = password

    @property
    async def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'last_name': self.last_name,
            'email': self.email
        }

    @hybrid_property
    def password(self) -> str:
        raise AttributeError("The password is not readable")

    @password.setter
    def password(self, raw_password: str):
        self._password = hash_password(raw_password)

    def check_password(self, password: str):
        return check_password(password, self._password)
