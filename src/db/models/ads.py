import datetime

from sqlalchemy import String, Text, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models import Base
from src.db.models.users import User


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
    async def dict(self):
        self.owner = await self.awaitable_attrs.owner

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
