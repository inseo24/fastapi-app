import logging
from typing import Optional

from sqlalchemy.orm import Session

from src.bono.project.models import ProjectExample

log = logging.getLogger(__name__)


def get(*, project_id: int, db_session: Session) -> Optional[ProjectExample]:
    log.info(f"Getting project by id: {project_id}")
    return (
        db_session.query(ProjectExample)
        .filter(ProjectExample.id == project_id)
        .one_or_none()
    )


def create(*, project_in: dict, db_session: Session) -> ProjectExample:
    log.info(f"Creating new project: {project_in}")
    form = ProjectExample(**project_in)

    db_session.add(form)
    db_session.commit()
    return form
