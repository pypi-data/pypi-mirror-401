# Patch Google Cloud services before importing main app
from unittest.mock import MagicMock, patch

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from pgvector.sqlalchemy import Vector
from sqlalchemy import ARRAY
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from db.session import get_session

# Mock google.auth.default
patch("google.auth.default", return_value=(MagicMock(), "test-project")).start()

# Mock Cloud Tasks
mock_tasks = MagicMock()
patch("google.cloud.tasks_v2.CloudTasksClient", return_value=mock_tasks).start()

# Mock Storage Client (if used via google-cloud-storage)
patch("google.cloud.storage.Client", MagicMock()).start()


from main import app


# Compilation hooks for SQLite compatibility
@compiles(JSONB, "sqlite")
def compile_jsonb_sqlite(type_, compiler, **kw):
    return "JSON"


@compiles(Vector, "sqlite")
def compile_vector_sqlite(type_, compiler, **kw):
    return "JSON"


@compiles(TSVECTOR, "sqlite")
def compile_tsvector_sqlite(type_, compiler, **kw):
    return "TEXT"


@compiles(ARRAY, "sqlite")
def compile_array_sqlite(type_, compiler, **kw):
    return "TEXT"


@pytest_asyncio.fixture(name="session")
async def session_fixture():
    from sqlalchemy import text

    from core.config import settings

    database_url = str(settings.DATABASE_URL)
    is_postgres = database_url.startswith("postgresql")

    if is_postgres:
        engine = create_async_engine(
            database_url,
            echo=False,
            future=True,
        )
    else:
        engine = create_async_engine(
            "sqlite+aiosqlite:///file:testdb?mode=memory&cache=shared&uri=true",
            connect_args={"check_same_thread": False},
            poolclass=None,
        )

    # Register custom function for SQLite
    if not is_postgres:
        from sqlalchemy import event

        @event.listens_for(engine.sync_engine, "connect")
        def connect(dbapi_connection, connection_record):
            dbapi_connection.create_function("to_tsvector", 2, lambda config, text: text)

    # Create tables
    async with engine.begin() as conn:
        if is_postgres:
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))

        # Ensure fresh start
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Patch the engine in db.session so middleware uses the test engine
    from unittest.mock import patch

    with patch("db.session.engine", engine):
        async with async_session() as session:
            yield session

    # Ensure all background trace events are saved before cleanup
    from services.trace import trace_service

    await trace_service.wait_for_tasks()

    # Cleanup
    if is_postgres:
        async with engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(name="seed_db")
async def seed_db_fixture(session: AsyncSession):
    # Check if data already exists
    from sqlmodel import select

    from models.auth import Organization, User

    existing_user = (await session.exec(select(User))).first()
    if existing_user:
        return

    # Create Org
    org = Organization(name="Test Organization")
    session.add(org)
    await session.commit()
    await session.refresh(org)

    # Create User
    user = User(
        email="test@example.com",
        full_name="Test User",
        organization_id=org.id,
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Create API Key matching the test env var
    # settings.API_KEY is "test_api_key" in CI
    # We hash it because the DB stores the hash
    # Wait, the deps.py checks settings.API_KEY directly for Dev Key access.
    # But if we want to test the DB path, we should add a key.
    # However, the test uses settings.API_KEY which is treated as a Dev Key.
    # The Dev Key path requires *any* user to exist.
    # So just creating the user above is sufficient for Dev Key access!

    # But let's also add a real API key for completeness if needed.
    # key_content = "test_api_key"
    # key_hash = hashlib.sha256(key_content.encode()).hexdigest()
    # api_key = ApiKey(
    #     key_hash=key_hash,
    #     key_prefix=key_content[:8],
    #     user_id=user.id,
    #     organization_id=org.id,
    #     name="Test Key"
    # )
    # session.add(api_key)
    # await session.commit()

    return user


@pytest_asyncio.fixture(name="client")
async def client_fixture(session: AsyncSession, seed_db):
    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest_asyncio.fixture(name="user")
async def user_fixture(seed_db):
    return seed_db


@pytest_asyncio.fixture(name="normal_user_token_headers")
async def normal_user_token_headers_fixture(user):
    # Depending on how auth works in test, we might use a mock token or API key
    # For now, let's assume we can use the 'X-API-Key' header if we set up a key,
    # OR we mock the verify_token dependency.

    # Since we didn't create an API key in seed_db but assumed Dev Key access:
    # settings.API_KEY matches "test_api_key" (default in test env?).
    # Let's import settings and check.
    from core.config import settings

    # We can use the dev key
    return {"X-API-Key": settings.API_KEY}
