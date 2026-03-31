from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.project_user import ProjectUserCreate, ProjectUserRead
from app.crud.project_user import assign_user_to_project, list_project_users

router = APIRouter(prefix="/v1/project-users", tags=["Project Users"])


@router.post("/", response_model=ProjectUserRead)
async def assign(db: AsyncSession = Depends(get_session), payload: ProjectUserCreate = None):
    return await assign_user_to_project(db, payload)


@router.get("/{project_id}", response_model=list[ProjectUserRead])
async def list_all(project_id: str, db: AsyncSession = Depends(get_session)):
    return await list_project_users(db, project_id)
