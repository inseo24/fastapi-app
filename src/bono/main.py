import logging

from fastapi import FastAPI
from contextvars import ContextVar
from typing import Optional, Final
from uuid import uuid1

from pydantic import ValidationError
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import compile_path

from src.bono.api import api_router
from src.bono.database.core import engine

log = logging.getLogger(__name__)

app = FastAPI(
    title="Bono API",
    description="Bono's API",
    root_path="/api",
    version="0.0.1",
    docs_url="/swagger",
    openapi_url="/docs/openapi.json",
    redoc_url="/docs"
)


class ExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        try:
            response = await call_next(request)
        except ValidationError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": e.errors()}
            )
        except ValueError as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content={"detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]},
            )
        except Exception as e:
            log.exception(e)
            response = JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]},
            )

        return response

REQUEST_ID_CTX_KEY: Final[str] = "request_id"
_request_id_ctx_var: ContextVar[Optional[str]] = ContextVar(REQUEST_ID_CTX_KEY, default=None)


def get_request_id() -> Optional[str]:
    return _request_id_ctx_var.get()

def get_path_params_from_request(request: Request) -> str:
    path_params = {}
    for r in api_router.routes:
        path_regex, path_format, param_converters = compile_path(r.path)
        path = request["path"].removeprefix("/api/v1")  # remove the /api/v1 for matching
        match = path_regex.match(path)
        if match:
            path_params = match.groupdict()
    return path_params


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request_id = str(uuid1())

    ctx_token = _request_id_ctx_var.set(request_id)
    path_params = get_path_params_from_request(request)
    log.info(
        f"Request {request_id} {request.method} {request.url.path} {path_params} {request.client.host}"
    )

    try:
        session = scoped_session(sessionmaker(bind=engine), scopefunc=get_request_id)
        request.state.db = session()
        response = await call_next(request)
    except Exception as e:
        raise e from None
    finally:
        request.state.db.close()

    _request_id_ctx_var.reset(ctx_token)
    return response



app.add_middleware(ExceptionMiddleware)

app.include_router(api_router)
