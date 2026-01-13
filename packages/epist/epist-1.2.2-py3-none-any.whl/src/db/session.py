from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from src.core.config import settings

# Create Async Engine
# echo=True enables SQL logging (useful for dev, disable in prod)
engine_args: dict[str, Any] = {
    "echo": False,
    "future": True,
    "pool_pre_ping": True,
    "pool_recycle": 1800,
}

if str(settings.DATABASE_URL).startswith("postgresql"):
    engine_args["pool_size"] = settings.DB_POOL_SIZE
    engine_args["max_overflow"] = settings.DB_MAX_OVERFLOW

engine = create_async_engine(
    str(settings.DATABASE_URL),
    **engine_args,
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore
    async with async_session() as session:
        yield session
