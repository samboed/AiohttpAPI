import datetime
import bcrypt

from sqlalchemy import (String, Text, ForeignKey,
                        DateTime, func, create_engine)
from sqlalchemy_utils import EmailType
from sqlalchemy.orm import (DeclarativeBase, Mapped,
                            mapped_column, relationship,
                            sessionmaker)
from sqlalchemy.ext.hybrid import hybrid_property

from src.config import (DB_DRIVER, DB_USER, DB_PASSWORD,
                        DB_HOST, DB_PORT, DB_NAME)
from src.db.service import hash_password


DSN = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DSN)
Session = sessionmaker(engine)


def create_tables():
    Base.metadata.create_all(engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


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


class Advertisement(Base):
    __tablename__ = 'advertisement'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime.datetime] = (
        mapped_column(DateTime, server_default=func.now()))
    owner_id = mapped_column(ForeignKey("user.id"), info={'no_update': True})

    owner: Mapped[User] = relationship(back_populates='advertisements')

    @property
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.timestamp(),
            'owner': {
                'id': self.owner.id,
                'name': self.owner.name,
                'last_name': self.owner.last_name,
                'email': self.owner.email
            }
        }
