"""
Database base configuration with dynamic path support.
"""

import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from aidiscuss.app.core.config import settings

logger = logging.getLogger("aidiscuss.db")

# Create base class for models
Base = declarative_base()

# Async engine for SQLite
engine = create_async_engine(
    settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///"),
    echo=False,
    future=True,
)

# Async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """
    Initialize database tables and seed default data.
    Uses Alembic for migrations. If database doesn't exist, creates all tables
    and marks as current with Alembic.
    """
    logger.info("Initializing database schema...")

    # Import all models to ensure they're registered with SQLAlchemy
    from aidiscuss.app.models import (
        Provider,
        Agent,
        Conversation,
        Message,
        Settings,
        ConversationMemory,
        ProviderKey,
    )

    # Import Document models if they exist
    try:
        from aidiscuss.app.models.document import Document, DocumentChunk
    except ImportError:
        pass

    # Create all tables (SQLAlchemy will handle idempotency)
    # For fresh databases, this creates the schema
    # For existing databases, this is a no-op
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created successfully")

    # Seed default providers
    from aidiscuss.app.db.seed_providers import seed_default_providers
    async with AsyncSessionLocal() as session:
        await seed_default_providers(session)

    logger.info("Default data seeded successfully")
