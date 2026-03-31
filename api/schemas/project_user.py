# app/schemas/project_user.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class ProjectUserBase(BaseModel):
    project_id: str
    user_uuid: UUID
    user_role: Optional[str] = None


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUserRead(ProjectUserBase):
    assigned_at: datetime

    model_config = {"from_attributes": True}

class ProjectUserResponse(ProjectUserBase):
    assigned_at: str

    model_config = {"from_attributes": True}
