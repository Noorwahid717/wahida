"""Database configuration helpers."""

from __future__ import annotations

from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .config import settings


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""

    pass


def _create_engine() -> Engine:
    if settings.postgres_dsn:
        return create_engine(settings.postgres_dsn, future=True, pool_pre_ping=True)
    # Default to local sqlite for developer ergonomics when DSN is not provided
    return create_engine("sqlite+pysqlite:///./wahida.db", future=True, pool_pre_ping=True)


engine: Engine = _create_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency yielding a database session."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """Provide a transactional scope for scripts and background tasks."""

    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:  # pragma: no cover - helper for scripts
        session.rollback()
        raise
    finally:
        session.close()


__all__ = ["Base", "SessionLocal", "engine", "get_db", "session_scope"]
