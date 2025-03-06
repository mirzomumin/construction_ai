import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ASGITransport
from app.database import Base, get_session
from app.main import app
from app.repositories import ProjectRepository, TaskRepository


TEST_DB_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    TEST_DB_URL,
    echo=False,
    # connect_args={"check_same_thread": False},
)
TestSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

####################### Set Up Test Database ########################


@pytest.fixture(autouse=True)
async def setup_test_db():
    # engine = create_async_engine(
    #     TEST_DB_URL,
    #     echo=False,
    #     connect_args={"check_same_thread": False},
    # )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

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


@pytest.fixture
async def project_obj():
    async for session in get_test_session():
        project_data = {
            "name": "Restaurant",
            "location": "San Francisco"
        }
        project = await ProjectRepository.create(
            values=project_data, session=session)
        
        tasks_data = [
            {"name": "Find land", "project_id": project.id},
            {"name": "Get permits", "project_id": project.id},
        ]
        await TaskRepository.bulk_create(values=tasks_data, session=session)
        await session.commit()
        await session.refresh(project)

        return project
