from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


from config import settings
from database.base import Base


class PostgresCore:
    def __init__(self):
        self.__engine = create_async_engine(
            url=settings.DATABASE_URL_asyncpg
        )

        self.session_factory = async_sessionmaker(self.__engine)

    async def create_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_tables(self):
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
