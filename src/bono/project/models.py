from datetime import datetime

from sqlalchemy import Column, VARCHAR, Integer

from src.bono.database.core import Base
from src.bono.models import TimeStampMixin, PrimaryKey, AppBase
from src.bono.project.enums import ProjectType


class ProjectExample(TimeStampMixin, Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=True)
    image = Column(VARCHAR(255), nullable=True)
    type = Column(VARCHAR(255), nullable=True, default=ProjectType.OTHER)


class FormsBase(AppBase):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime


class ProjectRead(FormsBase):
    id: PrimaryKey


class ProjectCreate(FormsBase):
    pass