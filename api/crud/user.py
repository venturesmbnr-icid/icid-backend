# app/crud/user.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from typing import List, Optional
from uuid import UUID


async def create_user(db: AsyncSession, payload: UserCreate) -> User:
    obj = User(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_user(db: AsyncSession, uuid: UUID) -> Optional[User]:
    result = await db.execute(select(User).where(User.uuid == uuid))
    return result.scalar_one_or_none()


async def list_users(db: AsyncSession) -> List[User]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def update_user(db: AsyncSession, uuid: UUID, payload: UserUpdate) -> Optional[User]:
    obj = await get_user(db, uuid)
    if not obj:
        return None

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_user(db: AsyncSession, uuid: UUID) -> bool:
    obj = await get_user(db, uuid)
    if not obj:
        return False

    await db.delete(obj)
    await db.commit()
    return True
