from __future__ import annotations

import contextlib
from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from ..config import ZENAUTH_SERVER_CONFIG
from .base import ZENAUTH_SCHEMA_TOKEN


def _schema_for_dsn(dsn: str) -> str | None:
    # SQLite does not support PostgreSQL-style schemas.
    if dsn.startswith("sqlite"):
        return None
    raw = ZENAUTH_SERVER_CONFIG().db_schema.strip()
    return raw or None


def create_engine_from_dsn(dsn: str) -> Engine:
    if dsn.startswith("sqlite"):
        engine = create_engine(
            dsn,
            poolclass=StaticPool,
            connect_args={"check_same_thread": False},
        )
    else:
        engine = create_engine(dsn, pool_pre_ping=True)

    # Use schema_translate_map so ORM models can be defined once using a schema
    # token and then mapped per-database at runtime.
    schema = _schema_for_dsn(dsn)
    return engine.execution_options(schema_translate_map={ZENAUTH_SCHEMA_TOKEN: schema})


def get_engine() -> Engine:
    return create_engine_from_dsn(ZENAUTH_SERVER_CONFIG().dsn)


def create_sessionmaker(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


@contextlib.contextmanager
def session_scope(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_session() -> Iterator[Session]:
    """FastAPI dependency: yields a DB session bound to configured engine."""

    engine = get_engine()
    session_factory = create_sessionmaker(engine)
    with session_scope(session_factory) as session:
        yield session
