import bcrypt

from sqlalchemy import String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import EmailType

from src.db.models import Base
from src.permission import hash_password


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
    def dict(self):
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
        raw_password_bytes = raw_password.encode('utf-8')
        hashed_password = hash_password(raw_password_bytes)
        self._password = hashed_password.decode('utf-8')

    def check_password(self, check_password: str):
        check_password_bytes = check_password.encode('utf-8')
        hash_password = self._password.encode('utf-8')
        return bcrypt.checkpw(check_password_bytes, hash_password)
