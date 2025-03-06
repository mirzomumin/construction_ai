import pytest
import os
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ASGITransport
from app.database import Base, get_session
from app.main import app



TEST_DB_PATH = "test_database.sqlite3"
TEST_DB_URL = f"sqlite+aiosqlite:///{TEST_DB_PATH}"


engine = create_async_engine(TEST_DB_URL, echo=False)
TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

####################### Set Up Test Database ########################


@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    engine = create_async_engine(TEST_DB_URL, echo=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

    await engine.dispose()

#####################################################################


############ Override app db sessions ############
async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide an async database session for tests.
    """
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_session] = get_test_session

##############################################


@pytest.fixture
async def client():
    """
    Provide an HTTP client for testing.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
