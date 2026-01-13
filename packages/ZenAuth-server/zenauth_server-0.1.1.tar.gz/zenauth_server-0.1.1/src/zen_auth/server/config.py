"""Server-side configuration loaded from environment variables.

This module contains settings that are only meaningful for the ZenAuth server
runtime (e.g., DB connectivity).
"""

from functools import lru_cache
from typing import Annotated, ClassVar

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode
from sqlalchemy.engine import make_url
from zen_auth.errors import ConfigError


class ZenAuthServerConfig(BaseSettings):
    """ZenAuth server settings.

    Values are loaded from env vars prefixed with `ZENAUTH_SERVER_` and an optional `.env` file.

    Note: In container environments, configuration is typically provided via
    environment variables / injected secrets, so `.env` is usually unnecessary.

    Note: Unlike core settings, these are only required when running the server.
    """

    _ENV_PREFIX: ClassVar[str] = "ZENAUTH_SERVER_"

    model_config = dict(env_prefix=_ENV_PREFIX, env_file=".env", extra="allow")

    dsn: str = ""
    refresh_window_sec: int = 300

    # --- Optional: DB schema ---
    # For databases that support schemas (e.g., PostgreSQL), ZenAuth tables can be
    # created under this schema. Use an empty string to disable schema usage.
    # Note: SQLite does not support schemas and will ignore this setting.
    db_schema: str = "zen_auth"

    # --- Optional: UI asset URLs ---
    # Lists of asset URLs to include in the server-rendered HTML.
    # Can be set via env vars as either:
    # - CSV: "https://a.css,https://b.css"
    # - Semicolon: "https://a.css;https://b.css"
    css_list: Annotated[list[str], NoDecode] = [
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css",
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.min.css",
    ]
    script_list: Annotated[list[str], NoDecode] = [
        "https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js",
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js",
    ]

    # --- Optional: static files mount ---
    # When set, the server will attempt to mount /static from this directory.
    # If relative, it is resolved against the current working directory.
    # If empty, the server will auto-detect ./static (current working directory).
    static_path: str = ""

    # --- CORS (disabled/locked-down recommended in production) ---
    # Comma-separated list of allowed origins. Use "*" for any origin.
    # Use an empty string to disable CORS middleware entirely.
    cors_allow_origins: str = ""
    cors_allow_credentials: bool = False
    cors_allow_methods: str = "*"
    cors_allow_headers: str = "*"

    # --- CSRF protection (recommended when using cookie-based auth from browsers) ---
    # When enabled, requests with the auth cookie must include a same-origin
    # (or trusted-origin) Origin/Referer header for unsafe methods.
    csrf_protect: bool = True
    # Comma-separated list of trusted origins (e.g. https://app.example).
    # If empty, falls back to CORS allow-origins (if set and not "*") or same-origin.
    csrf_trusted_origins: str = ""
    # If true, allows requests without Origin/Referer (not recommended).
    csrf_allow_no_origin: bool = False

    # --- Optional: bootstrap an initial admin account (recommended: disabled in production) ---
    # When enabled, creates the user only if it does not already exist.
    bootstrap_admin: bool = False
    bootstrap_admin_user: str = "admin"
    bootstrap_admin_password: str | None = None

    @field_validator("css_list", "script_list", mode="before")
    @classmethod
    def _parse_asset_list(cls, value: object) -> object:
        if value is None:
            return []
        if isinstance(value, str):
            raw = value.strip()
            if not raw:
                return []
            # Accept comma or semicolon separated values for convenience.
            sep = ";" if ";" in raw and "," not in raw else ","
            return [v.strip() for v in raw.split(sep) if v.strip()]
        return value

    def model_post_init(self, context: object) -> None:
        if not self.dsn or not self.dsn.strip():
            raise ConfigError(f"{self._ENV_PREFIX}DSN must be set")

        if self.bootstrap_admin:
            if not self.bootstrap_admin_user or not self.bootstrap_admin_user.strip():
                raise ConfigError(f"{self._ENV_PREFIX}BOOTSTRAP_ADMIN_USER must be set")
            if not self.bootstrap_admin_password or not self.bootstrap_admin_password.strip():
                raise ConfigError(f"{self._ENV_PREFIX}BOOTSTRAP_ADMIN_PASSWORD must be set")

    def safe_dict(self) -> dict[str, object]:
        """Return a redacted representation safe for logs/diagnostics."""

        data: dict[str, object] = self.model_dump()
        if self.dsn:
            try:
                url = make_url(self.dsn)
                data["dsn"] = url.render_as_string(hide_password=True)
            except Exception:
                # If parsing fails, fall back to full redaction.
                data["dsn"] = "***REDACTED***"

        for key in ("secret_key", "bootstrap_admin_password", "bootstrap_admin_user"):
            if data.get(key) is not None:
                data[key] = "***REDACTED***"
        return data


@lru_cache
def ZENAUTH_SERVER_CONFIG() -> ZenAuthServerConfig:
    return ZenAuthServerConfig()
