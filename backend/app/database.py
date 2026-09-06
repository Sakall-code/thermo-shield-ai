"""
Async SQLAlchemy engine & session factory (prototype — SQLite).

The engine points at a local SQLite file so the prototype runs with zero
external infrastructure.  Import ``Base`` from here when defining ORM models
and ``get_db`` as a FastAPI dependency for request-scoped sessions.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./thermoshield_prototype.db"

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=settings.DEBUG)

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    """Shared declarative base for all ORM models."""


async def get_db() -> AsyncSession:  # type: ignore[misc]
    """FastAPI dependency — yields an async DB session."""
    async with async_session() as session:
        yield session
