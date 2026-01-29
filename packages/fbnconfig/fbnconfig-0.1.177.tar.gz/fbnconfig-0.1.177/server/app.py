import json
import logging
import os
import pathlib
import time
import uuid
from datetime import datetime, timezone

from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Mount, Route

import fbnconfig
from fbnconfig import log as deployment_log
from fbnconfig import schemagen
from fbnconfig.load_module import load_module

logger = logging.getLogger("fbnconfig.server")


def _get_request_ids(request: Request) -> tuple[str, str | None]:
    """Return (request_id, correlation_id).

    Since upstream services don't establish a single canonical correlation header,
    we accept both and ensure there's always a request_id.
    """

    request_id = request.headers.get("X-Request-Id")
    correlation_id = request.headers.get("X-Correlation-Id")
    if not request_id:
        request_id = correlation_id or str(uuid.uuid4())
    return request_id, correlation_id


def _configure_logging() -> None:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper().strip()
    level = logging.getLevelNamesMapping().get(level_name, logging.INFO)

    root_logger = logging.getLogger()
    if not root_logger.handlers:
        logging.basicConfig(level=level)
    else:
        root_logger.setLevel(level)


_configure_logging()

# Startup tracking for readiness probe
_app_started_at = None


def _json_log(level: int, event: str, **fields):
    log_data = {"timestamp": datetime.now(timezone.utc).isoformat(), "event": event, **fields}
    logger.log(level, json.dumps(log_data))


def get_examples_path():
    return pathlib.Path(__file__).parent.parent / "public_examples" / "examples"


async def homepage(_: Request):
    return JSONResponse({"message": "Hello, Banana!", "status": "success"})


async def health_check(_: Request):
    return JSONResponse({"status": "healthy", "service": "fbnconfig-api"})


async def ready_check(_: Request):
    """Readiness probe endpoint for Kubernetes.

    Returns 200 if the server has finished startup initialization.
    Used by K8s to route traffic only to ready replicas.
    """
    if _app_started_at is None:
        return JSONResponse({"status": "not_ready", "service": "fbnconfig-api"}, status_code=503)
    return JSONResponse({
        "status": "ready",
        "service": "fbnconfig-api",
        "started_at": _app_started_at.isoformat()
    })


async def get_schema(_):
    return JSONResponse(SCHEMA)


async def invoke(request: Request) -> JSONResponse:
    # Minimal callable endpoint for platform health checks and integration tests
    try:
        payload = await request.json()
    except Exception as exc:
        payload = None
        _json_log(
            logging.WARNING,
            "json_parse_failed",
            request_id=getattr(request.state, "request_id", None),
            correlation_id=getattr(request.state, "correlation_id", None),
            error=str(exc),
        )
    return JSONResponse({"status": "ok", "received": payload})


async def list_examples(request: Request) -> JSONResponse:
    example_folder = get_examples_path()
    if not example_folder.exists():
        return JSONResponse([])

    files = example_folder.glob("*.py")
    res = [
        {"name": str(f.stem), "path": request.url_for("get_example", example_name=str(f.stem)).path}
        for f in files
    ]
    return JSONResponse(res)


async def get_example(request: Request):
    example_folder = get_examples_path()
    example_name = request.path_params["example_name"] + ".py"
    script_path = example_folder / example_name

    if not script_path.exists():
        raise HTTPException(status_code=404, detail=f"Example {example_name} not found")

    module = load_module(script_path, str(example_folder))
    if getattr(module, "configure", None) is None:
        raise HTTPException(status_code=400, detail="No configure found in " + example_name)
    deployment = module.configure({})
    dump = fbnconfig.dump_deployment(deployment)
    return JSONResponse(dump)


def create_client(lusid_env, token):
    if lusid_env is None or token is None:
        raise HTTPException(status_code=401, detail="No auth header or no X-LUSID-Host")
    client = fbnconfig.create_client(lusid_env, token)
    return client


async def get_log(request: Request):
    client = create_client(request.state.lusid_env, request.state.token)
    deployment_name = request.path_params["deployment_name"]
    log = []
    for line in deployment_log.list_resources_for_deployment(client, deployment_id=deployment_name):
        d = line._asdict()
        d["state"] = vars(d["state"])
        log.append(d)
    return JSONResponse(log)


SCHEMA = schemagen.cmd_deployment_schema()


class RequestLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id, correlation_id = _get_request_ids(request)
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception as exc:  # Log and re-raise to preserve default handlers
            duration_ms = round((time.perf_counter() - start) * 1000, 3)
            _json_log(
                logging.ERROR,
                "request_error",
                request_id=request_id,
                correlation_id=correlation_id,
                method=request.method,
                path=request.url.path,
                duration_ms=duration_ms,
                error=str(exc),
            )
            raise

        duration_ms = round((time.perf_counter() - start) * 1000, 3)
        response.headers["X-Request-Id"] = request_id
        if correlation_id:
            response.headers["X-Correlation-Id"] = correlation_id
        _json_log(
            logging.INFO,
            "request_complete",
            request_id=request_id,
            correlation_id=correlation_id,
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=duration_ms,
        )
        return response


class PassThruAuth(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")
        if auth and auth.startswith("Bearer "):
            request.state.token = auth.split(" ")[1]
        else:
            request.state.token = None
        host = request.headers.get("X-LUSID-Host")
        request.state.lusid_env = host if host else None
        return await call_next(request)


middleware = [Middleware(RequestLogger), Middleware(PassThruAuth)]
routes = [
    Route("/", homepage),
    Route("/health", health_check),
    Route("/ready", ready_check),
    Route("/invoke", invoke, methods=["POST"]),
    Route("/examples/", list_examples),
    Route("/examples/{example_name}", get_example),
    Route("/log/{deployment_name}", get_log),
    Route("/schema", get_schema, methods=["GET"]),
]

# the fbnconfig application
cfg_app = Starlette(routes=routes, middleware=middleware)

# the app that will be run to mount the cfg app
app = Starlette(routes=[
    Mount("/api/fbnconfig", cfg_app)
])


# Lifespan events for startup/shutdown logging
@app.router.on_event("startup")
async def startup():
    global _app_started_at
    _app_started_at = datetime.now(timezone.utc)
    _json_log(
        logging.INFO,
        "app_startup",
        timestamp=_app_started_at.isoformat(),
        version=getattr(fbnconfig, "__version__", "unknown")
    )


@app.router.on_event("shutdown")
async def shutdown():
    _json_log(
        logging.INFO,
        "app_shutdown",
        timestamp=datetime.now(timezone.utc).isoformat()
    )
