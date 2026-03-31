# app/crud/project.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate
from typing import List, Optional


async def create_project(db: AsyncSession, payload: ProjectCreate) -> Project:
    obj = Project(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_project(db: AsyncSession, project_id: str) -> Optional[Project]:
    result = await db.execute(select(Project).where(Project.project_id == project_id))
    return result.scalar_one_or_none()


async def list_projects(db: AsyncSession) -> List[Project]:
    result = await db.execute(select(Project))
    return result.scalars().all()


async def update_project(db: AsyncSession, project_id: str, payload: ProjectUpdate) -> Optional[Project]:
    obj = await get_project(db, project_id)
    if not obj:
        return None

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(obj, field, value)

    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_project(db: AsyncSession, project_id: str) -> bool:
    obj = await get_project(db, project_id)
    if not obj:
        return False

    await db.delete(obj)
    await db.commit()
    return True
