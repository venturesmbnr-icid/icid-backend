# app/schemas/client.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class ClientBase(BaseModel):
    client_id: str
    client_username: str
    client_name: str
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = None
    client_role: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientUpdate(BaseModel):
    client_username: Optional[str] = None
    client_name: Optional[str] = None
    client_email: Optional[EmailStr] = None
    client_phone: Optional[str] = None
    client_role: Optional[str] = None

class ClientRead(ClientBase):
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ClientResponse(ClientBase):
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}
