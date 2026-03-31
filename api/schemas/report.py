# app/schemas/report.py

from pydantic import BaseModel
from uuid import UUID
from typing import Optional
from datetime import datetime


class ReportBase(BaseModel):
    report_id: str
    reporter_uuid: UUID
    project_id: str
    report_date: Optional[str] = None


class ReportCreate(ReportBase):
    pass


class ReportUpdate(BaseModel):
    report_date: Optional[str] = None

class ReportRead(ReportBase):
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ReportResponse(ReportBase):
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}
