from fastapi import APIRouter, HTTPException, status
from fastapi._compat import ErrorWrapper
from pydantic import ValidationError

from src.bono.database.core import DbSession
from src.bono.models import PrimaryKey
from .models import ProjectRead
from .service import get, create

from sqlalchemy.exc import IntegrityError

from src.bono.exceptions import ExistsError

router = APIRouter()


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(db_session: DbSession, project_id: PrimaryKey):
    project = get(db_session=db_session, project_id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=[{"msg": "A Project with this id does not exist."}],
        )
    return project


@router.post("", response_model=ProjectRead)
def create_project(
        db_session: DbSession,
        project_in: dict,
):
    """Create a new Project."""
    try:
        return create(
            db_session=db_session, project_in=project_in
        )
    except IntegrityError:
        raise ValidationError(
            [
                ErrorWrapper(
                    ExistsError()
                )
            ],
        ) from None
