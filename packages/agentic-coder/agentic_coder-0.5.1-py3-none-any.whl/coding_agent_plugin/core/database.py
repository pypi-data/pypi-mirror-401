"""Database connection and session management."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    AsyncEngine,
    create_async_engine,
    async_sessionmaker,
)

from . import config
from ..schemas.project import Base


class DatabaseManager:
    """Manages database connections and sessions."""

    def __init__(self) -> None:
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None
        self._initialized: bool = False

    def _check_database_url(self) -> None:
        """Check if DATABASE_URL is configured."""
        if not config.DATABASE_URL:
            raise ValueError("DATABASE_URL is not configured.")
            
        # Ensure directory exists for SQLite
        if "sqlite" in config.DATABASE_URL and "///" in config.DATABASE_URL:
            try:
                # Extract path from sqlite+aiosqlite:///path/to/db
                db_path = config.DATABASE_URL.split("///")[1]
                Path(db_path).parent.mkdir(parents=True, exist_ok=True)
            except Exception:
                pass # Best effort

    @property
    def engine(self) -> AsyncEngine:
        """Get or create the database engine."""
        if self._engine is None:
            self._check_database_url()

            if not config.DATABASE_URL:
                raise ValueError("DATABASE_URL is not configured.")

            engine_args = {
                "url": config.DATABASE_URL,
                "echo": config.DATABASE_ECHO,
                "pool_pre_ping": True,
            }

            # SQLite (aiosqlite) usually doesn't support pool_size/max_overflow
            if "sqlite" not in config.DATABASE_URL:
                engine_args.update({
                    "pool_size": 5,
                    "max_overflow": 10,
                })

            self._engine = create_async_engine(**engine_args)
        return self._engine

    @property
    def session_factory(self) -> async_sessionmaker[AsyncSession]:
        """Get or create the session factory."""
        if self._session_factory is None:
            self._session_factory = async_sessionmaker(
                self.engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
                autocommit=False,
            )
        return self._session_factory

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Get a database session."""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def setup(self) -> None:
        """
        Initialize database - validate URL and create tables.

        Raises:
            ValueError: If DATABASE_URL not configured
        """
        if self._initialized:
            return

        self._check_database_url()

        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        self._initialized = True
        print("✅ Database initialized successfully")

    async def close(self) -> None:
        """Close database connections."""
        if self._engine:
            await self._engine.dispose()


# Global instance
db_manager: DatabaseManager = DatabaseManager()
