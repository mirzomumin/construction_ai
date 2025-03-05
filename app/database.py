from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncAttrs,
)
from sqlalchemy.orm import DeclarativeBase
from typing import AsyncGenerator


DATABASE_URL = "sqlite+aiosqlite:///./db.sqlite3"
engine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


class Base(DeclarativeBase, AsyncAttrs):
    pass
