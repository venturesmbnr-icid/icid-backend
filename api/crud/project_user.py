# app/crud/project_user.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.project_user import ProjectUser
from app.schemas.project_user import ProjectUserCreate
from typing import List


from sqlalchemy import select

async def assign_user_to_project(
    db: AsyncSession,
    payload: ProjectUserCreate,
) -> ProjectUser:

    result = await db.execute(
        select(ProjectUser).where(
            ProjectUser.project_id == payload.project_id,
            ProjectUser.user_id == payload.user_uuid,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        return existing

    obj = ProjectUser(
        project_id=payload.project_id,
        user_id=payload.user_uuid,
        user_role=payload.user_role or "member",
    )

    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj



async def list_project_users(db: AsyncSession, project_id: str) -> List[ProjectUser]:
    result = await db.execute(select(ProjectUser).where(ProjectUser.project_id == project_id))
    return result.scalars().all()
