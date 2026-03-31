# app/schemas/project.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    project_id: str
    project_name: str
    project_description: Optional[str] = None
    registration_code: Optional[str] = None
    borough: Optional[str] = None
    status: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    project_description: Optional[str] = None
    registration_code: Optional[str] = None
    borough: Optional[str] = None
    status: Optional[str] = None

class ProjectRead(ProjectBase):
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ProjectResponse(ProjectBase):
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}
