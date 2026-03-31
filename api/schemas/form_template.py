# app/schemas/form_template.py

from pydantic import BaseModel
from typing import Optional, Any
from uuid import UUID
from datetime import datetime


class FormTemplateBase(BaseModel):
    form_template_id: str
    form_name: str
    form_description: Optional[str] = None
    form_status: Optional[str] = None
    mandatory_forms: Optional[str] = None
    optional_forms: Optional[str] = None


class FormTemplateCreate(BaseModel):
    form_template_id: str
    form_name: str
    form_description: Optional[str] = None


class FormTemplateUpdate(BaseModel):
    form_name: Optional[str] = None
    form_description: Optional[str] = None


class FormTemplateRead(FormTemplateCreate):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
