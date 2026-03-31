# app/crud/project_client.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project_client import ProjectClient
from app.schemas.project_client import ProjectClientCreate
from typing import List


async def add_client_to_project(db: AsyncSession, payload: ProjectClientCreate) -> ProjectClient:
    obj = ProjectClient(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def list_project_clients(db: AsyncSession, project_id: str) -> List[ProjectClient]:
    result = await db.execute(select(ProjectClient).where(ProjectClient.project_id == project_id))
    return result.scalars().all()
