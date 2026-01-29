"""Database configuration and session management."""

from collections.abc import AsyncIterator, Iterator
from contextlib import asynccontextmanager, contextmanager

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import get_settings
from app.core.logger import log

settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_pre_ping=True,  # Verify connections before using
)


def init_db() -> None:
    """
    Initialize database.
    
    Creates all tables defined in SQLModel models.
    Call this during application startup.
    """
    log.info("Initializing database...")
    SQLModel.metadata.create_all(engine)
    log.success("Database initialized")


def get_session() -> Iterator[Session]:
    """
    Get database session (sync).
    
    Use as FastAPI dependency:
        @app.get("/users")
        def get_users(session: Session = Depends(get_session)):
            users = session.exec(select(User)).all()
            return users
    
    Yields:
        Database session
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            log.error(f"Database session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


@contextmanager
def get_session_context() -> Iterator[Session]:
    """
    Get database session context manager.
    
    Use in services or utility functions:
        with get_session_context() as session:
            user = session.get(User, user_id)
    
    Yields:
        Database session
    """
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            log.error(f"Database session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


# If you need async support, uncomment and install sqlalchemy[asyncio]:
#
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
#
# async_engine = create_async_engine(
#     settings.database_url.replace("sqlite://", "sqlite+aiosqlite://"),
#     echo=settings.db_echo,
# )
#
# async def get_async_session() -> AsyncIterator[AsyncSession]:
#     """Get async database session."""
#     async with AsyncSession(async_engine) as session:
#         try:
#             yield session
#         except Exception as e:
#             log.error(f"Database session error: {e}")
#             await session.rollback()
#             raise
#         finally:
#             await session.close()
