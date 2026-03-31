# app/schemas/project_client.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectClientBase(BaseModel):
    project_id: str
    client_id: str
    client_role: Optional[str] = None


class ProjectClientCreate(ProjectClientBase):
    pass


class ProjectClientRead(ProjectClientBase):
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = {"from_attributes": True}

class ProjectClientResponse(ProjectClientBase):
    model_config = {"from_attributes": True}
