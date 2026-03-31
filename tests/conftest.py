import asyncio
import pytest
import pytest_asyncio
from sqlalchemy import event
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db import session as db_session_module
from app.db.session import create_session_factory

from app.models.client import Client
from app.crud.project import create_project
from app.schemas.project import ProjectCreate

from uuid import uuid4

from app.crud.user import create_user
from app.schemas.user import UserCreate

import app.models

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """
    Required for pytest-asyncio when using session-scoped async fixtures.
    """
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_sqlite_fk(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncSession:
    """
    One transaction per test.
    Automatically rolled back for isolation.
    """
    async_session_factory = create_session_factory(test_engine)

    async with test_engine.connect() as conn:
        trans = await conn.begin()
        session: AsyncSession = async_session_factory(bind=conn)

        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()


@pytest.fixture
async def client(db_session: AsyncSession):
    """
    FastAPI test client with DB session dependency override.
    """
    async def override_get_session():
        yield db_session

    app.dependency_overrides[db_session_module.get_session] = override_get_session

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture
async def test_client(db_session: AsyncSession) -> Client:
    """
    Creates a valid Client row for FK-dependent tests.
    """
    client = Client(
        client_id="C001",
        client_username="test_client",
        client_name="Test Client",
    )
    db_session.add(client)
    await db_session.commit()
    await db_session.refresh(client)
    return client

@pytest_asyncio.fixture
async def test_project(db_session, test_client):
    payload = ProjectCreate(
        project_id="P001",
        project_name="Test Project",
        registration_code="REG-P001",
        borough="Manhattan",
        status="active",
    )
    return await create_project(db_session, payload)


@pytest_asyncio.fixture
async def test_project_alt(db_session, test_client):
    payload = ProjectCreate(
        project_id="P002",
        project_name="Alt Project",
        registration_code="REG-P002",
        borough="Brooklyn",
        status="active",
    )
    return await create_project(db_session, payload)





@pytest_asyncio.fixture
async def test_user(db_session, test_client):
    payload = UserCreate(
        email="reporter@example.com",
        first_name="Report",
        last_name="User",
        phone_number="555-0000",
        client_id=test_client.client_id,
    )
    return await create_user(db_session, payload)