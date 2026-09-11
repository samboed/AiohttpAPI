from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import DB_DRIVER, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from src.db.models import Base


DSN = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DSN)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)


async def init_orm():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_orm():
    await engine.dispose()
