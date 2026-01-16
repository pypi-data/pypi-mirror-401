from __future__ import annotations

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import JSONResponse

from ....config import ZENAUTH_SERVER_CONFIG
from ..url_names import (
    AUTH_LOGIN_PAGE,
    META_ACCESS_TOKEN_API,
    META_ENDPOINTS_API,
    VERIFY_TOKEN_API,
    VERIFY_USER_API,
    VERIFY_USER_ROLE_API,
    VERIFY_USER_ROLE_OR_SCOPE_API,
    VERIFY_USER_SCOPE_API,
)

router = APIRouter(prefix="", tags=["meta"])


@router.get("/endpoints", name=META_ENDPOINTS_API)
def endpoints(req: Request) -> JSONResponse:
    """Return public API endpoints for clients.

    This is intended for service discovery so callers don't need to hardcode
    paths like `/verify/token`.
    """

    data = {
        "login_page": str(req.url_for(AUTH_LOGIN_PAGE)),
        "verify_token": str(req.url_for(VERIFY_TOKEN_API)),
        "verify_user": str(req.url_for(VERIFY_USER_API)),
        "verify_user_role": str(req.url_for(VERIFY_USER_ROLE_API)),
        "verify_user_scope": str(req.url_for(VERIFY_USER_SCOPE_API)),
        "verify_user_role_or_scope": str(req.url_for(VERIFY_USER_ROLE_OR_SCOPE_API)),
    }
    return JSONResponse(content={"data": data})


@router.get("/access_token", name=META_ACCESS_TOKEN_API)
def access_token() -> JSONResponse:
    """Return public access-token metadata for clients.

    This is intended for cross-origin clients that need to know:
    - the access token cookie name
    - the cookie max-age (derived from server token expiry)
    """

    cfg = ZENAUTH_SERVER_CONFIG()
    return JSONResponse(
        content={
            "data": {
                "access_token_cookie_name": cfg.access_token_cookie_name,
                "access_token_expire_min": cfg.expire_min,
            }
        }
    )
