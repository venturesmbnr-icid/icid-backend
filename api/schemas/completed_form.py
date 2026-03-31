# app/schemas/completed_form.py

from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime



class CompletedFormBase(BaseModel):
    completed_form_id: str
    report_id: str
    form_template_id: str
    form_data: Optional[str] = None


class CompletedFormCreate(CompletedFormBase):
    pass


class CompletedFormUpdate(BaseModel):
    form_data: Optional[str] = None


class CompletedFormRead(CompletedFormBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True  # Pydantic v2 required for ORM mode
    }

class CompletedFormResponse(CompletedFormBase):
    id: UUID
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}
