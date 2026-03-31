# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    client_id: str


class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass


class UserUpdate(BaseModel):
    """Schema for partial updates."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

class UserRead(UserBase):
    uuid: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class UserResponse(UserBase):
    uuid: UUID
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class UserListItem(BaseModel):
    user_id: int
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    employer: str
    

class UserListResponse(BaseModel):
    status: str
    message: str
    data: list[UserListItem]