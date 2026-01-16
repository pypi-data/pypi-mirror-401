from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# All tables are defined under this schema token.
# Engines should set schema_translate_map to map this token to the desired
# database schema (e.g. "zen_auth") or to None (e.g. for SQLite).
ZENAUTH_SCHEMA_TOKEN = "__zen_auth_schema__"

metadata_obj = MetaData(schema=ZENAUTH_SCHEMA_TOKEN)


class Base(DeclarativeBase):
    metadata = metadata_obj
