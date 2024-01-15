from fastapi import APIRouter
from pydantic import BaseModel
from starlette.responses import JSONResponse

from src.bono.project.views import router as project_router


class ErrorResponse(BaseModel):
    msg: str


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    }
)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"status": "ok"}


api_router.include_router(project_router, prefix="/project", tags=["project"])