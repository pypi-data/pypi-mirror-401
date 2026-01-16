import sys
from logging import Formatter, StreamHandler
from pathlib import Path

from fastapi import FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from zen_auth.errors import ClaimError
from zen_auth.logger import LOGGER

from . import ENV
from .api import router
from .api.util.error_redirect import error_redirect
from .api.util.req_id import RequestIDMiddleWare
from .api.v1.url_names import AUTH_LOGIN_PAGE, META_ENDPOINTS_API
from .config import ZENAUTH_SERVER_CONFIG, ZenAuthServerConfig
from .lifespan import lifespan
from .middleware import AccessLogWithTimeMiddleware, CSRFMiddleware

if LOGGER.handlers == []:
    handler = StreamHandler(sys.stdout)
    handler.setFormatter(
        Formatter(fmt="[%(asctime)s] %(levelname)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S"),
    )
    LOGGER.addHandler(handler)

LOGGER.setLevel(ENV.LOG_LEVEL)
LOGGER.info("Log level set to %s", ENV.LOG_LEVEL)


def _split_csv(value: str) -> list[str]:
    return [v.strip() for v in value.split(",") if v.strip()]


def _mount_static_if_present(app: FastAPI, config: ZenAuthServerConfig) -> None:
    static_dir: Path | None = None

    static_path = getattr(config, "static_path", "")
    if isinstance(static_path, str) and static_path.strip():
        candidate = Path(static_path.strip()).expanduser()
        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate
        if candidate.is_dir():
            static_dir = candidate
        else:
            LOGGER.warning("Static path configured but not found: %s", candidate)
            return
    else:
        candidate = Path.cwd() / "static"
        if candidate.is_dir():
            static_dir = candidate

    if not static_dir:
        return

    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    LOGGER.info("Mounted static files at /static from %s", static_dir)


def create_app() -> FastAPI:
    config = ZENAUTH_SERVER_CONFIG()
    app = FastAPI(
        title="ZenAuth Authentication", version=ENV.BUILD, docs_url=None, redoc_url=None, lifespan=lifespan
    )

    cors_origins_raw = config.cors_allow_origins.strip()
    if cors_origins_raw:
        allow_origins = ["*"] if cors_origins_raw == "*" else _split_csv(cors_origins_raw)
        allow_methods = (
            ["*"] if config.cors_allow_methods.strip() == "*" else _split_csv(config.cors_allow_methods)
        )
        allow_headers = (
            ["*"] if config.cors_allow_headers.strip() == "*" else _split_csv(config.cors_allow_headers)
        )

        app.add_middleware(
            CORSMiddleware,
            allow_origins=allow_origins,
            allow_credentials=config.cors_allow_credentials,
            allow_methods=allow_methods,
            allow_headers=allow_headers,
        )
    app.add_middleware(RequestIDMiddleWare)
    app.add_middleware(CSRFMiddleware)
    app.add_middleware(AccessLogWithTimeMiddleware)

    _mount_static_if_present(app, config)

    app.include_router(router)
    LOGGER.debug("ZenAuthServer config loaded (redacted): %s", config.safe_dict())

    return app


app = create_app()


@app.get("/")
def _top(req: Request) -> RedirectResponse:
    return RedirectResponse(req.url_for(AUTH_LOGIN_PAGE), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/endpoints")
def _endpoints(req: Request) -> RedirectResponse:
    return RedirectResponse(req.url_for(META_ENDPOINTS_API), status_code=status.HTTP_303_SEE_OTHER)


@app.exception_handler(ClaimError)
def rbac_exception_handler(request: Request, exc: ClaimError) -> Response:
    # NOTE: Avoid redirect targets derived from user-controlled cookies.
    # Redirect to the login page (fixed server route).
    to = request.url_for(AUTH_LOGIN_PAGE)

    # Log full details for operators
    LOGGER.warning("Claim error: %s", exc, exc_info=True)

    # Prepare a short, safe message for end users. Avoid leaking internals.
    msg = str(exc) or "An authentication error occurred"
    msg = msg.replace("\n", " ")[:200]

    return error_redirect(to, msg)
