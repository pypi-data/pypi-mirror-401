"""Integration test configuration - real PostgreSQL."""

import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from coding_agent_plugin.schemas.project import Base


# DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# if not DATABASE_URL:
#     # Fallback to in-memory SQLite for testing if no DB configured
#     DATABASE_URL = "sqlite+aiosqlite:///:memory:"





@pytest.fixture(scope="function")
async def engine() -> AsyncGenerator[AsyncEngine, None]:
    """Real async engine against PostgreSQL."""
    # Configure engine args based on DB type
    engine_args = {"echo": False, "pool_pre_ping": False}
    if "sqlite" not in DATABASE_URL:
        engine_args.update({"pool_size": 1, "max_overflow": 0})
        
    engine = create_async_engine(
        DATABASE_URL,
        **engine_args
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Real DB session, rolled back and closed per test."""
    factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    async with factory() as sess:
        try:
            yield sess
        finally:
            await sess.rollback()
            await sess.close()
