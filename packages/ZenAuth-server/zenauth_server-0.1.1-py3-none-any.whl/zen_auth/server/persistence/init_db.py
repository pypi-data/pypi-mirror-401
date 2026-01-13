from __future__ import annotations

import os

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from zen_auth.logger import LOGGER

from ..config import ZENAUTH_SERVER_CONFIG
from ..usecases.user_service import pwd_ctx
from .base import ZENAUTH_SCHEMA_TOKEN, Base
from .models import RoleOrm, UserOrm

# Dialects where we attempt to create a schema/database automatically.
# Other dialects may support schemas, but provisioning is expected to be handled
# externally (or added here when officially supported).
SUPPORTED_SCHEMA_DIALECTS = frozenset({"postgresql", "mysql", "mariadb"})


def _ensure_schema_exists(engine: Engine, schema: str | None) -> None:
    """Best-effort schema/database provisioning.

    Behavior:
    - If `schema` is None/empty, this is a no-op.
    - Only dialects in `SUPPORTED_SCHEMA_DIALECTS` are handled here. Other
      dialects must be provisioned externally.
    """

    dialect = engine.dialect.name

    if not schema:
        return
    if dialect not in SUPPORTED_SCHEMA_DIALECTS:
        return

    # Quote identifiers using the current dialect rules to avoid SQL injection
    # and to handle reserved words.
    quoted = engine.dialect.identifier_preparer.quote(schema)

    ddl = f"CREATE SCHEMA IF NOT EXISTS {quoted}"

    with engine.connect() as conn:
        conn.exec_driver_sql(ddl)
        conn.commit()


def _schema_for_engine(engine: Engine) -> str | None:
    # SQLite does not support schemas.
    # For SQLite, we map the schema token to None.
    dialect = engine.dialect.name

    if dialect == "sqlite":
        return None
    raw = ZENAUTH_SERVER_CONFIG().db_schema.strip()
    return raw or None


def init_db(engine: Engine) -> None:
    """Create DB tables.

    Optionally bootstraps an initial admin user when enabled via env:
    - `ZENAUTH_SERVER_BOOTSTRAP_ADMIN=true`
    - `ZENAUTH_SERVER_BOOTSTRAP_ADMIN_USER=<user>`
    - `ZENAUTH_SERVER_BOOTSTRAP_ADMIN_PASSWORD=<password>`

    This is intended for development/demo use.
    """

    schema = _schema_for_engine(engine)

    # Create schema if the dialect supports it and we have a safe way to do so.
    # Otherwise, expect the schema/database to be provisioned externally.
    _ensure_schema_exists(engine, schema)

    # Apply schema_translate_map so the same metadata can target either:
    # - a real schema name (e.g. "zen_auth") on schema-capable DBs
    # - no schema (None) on SQLite
    bind = engine.execution_options(schema_translate_map={ZENAUTH_SCHEMA_TOKEN: schema})
    Base.metadata.create_all(bind=bind)

    # Optional bootstrap admin: opt-in via env vars.
    # We intentionally avoid loading ZenAuthServerConfig here, because init_db(engine)
    # is used in tests/tools that construct an Engine directly and shouldn't require DSN env.
    bootstrap = os.getenv("ZENAUTH_SERVER_BOOTSTRAP_ADMIN", "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    if not bootstrap:
        return

    user_name = os.getenv("ZENAUTH_SERVER_BOOTSTRAP_ADMIN_USER", "").strip()
    password = os.getenv("ZENAUTH_SERVER_BOOTSTRAP_ADMIN_PASSWORD", "")
    if not user_name or not password.strip():
        LOGGER.warning(
            "Bootstrap admin enabled but missing env vars: ZENAUTH_SERVER_BOOTSTRAP_ADMIN_USER / ZENAUTH_SERVER_BOOTSTRAP_ADMIN_PASSWORD"
        )
        return

    with Session(bind) as session:
        with session.begin():
            admin = session.get(UserOrm, user_name)
            if admin is None:
                role = session.get(RoleOrm, "admin")
                if role is None:
                    role = RoleOrm(role_name="admin", display_name="Admin")
                    session.add(role)
                    session.flush()
                session.add(
                    UserOrm(
                        user_name=user_name,
                        password=pwd_ctx.hash(password),
                        roles=[role],
                        real_name="Administrator",
                        division="admin",
                        description="Bootstrapped admin account",
                    )
                )
                LOGGER.info("Bootstrapped admin account created")
