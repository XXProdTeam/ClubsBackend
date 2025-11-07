from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import Settings

settings = Settings()  # type: ignore

DATABASE_URL = str(settings.DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)

async_session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Зависимость для получения асинхронной сессии базы данных.
    """
    async with async_session_maker() as session:
        yield session
