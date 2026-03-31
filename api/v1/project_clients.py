from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.project_client import ProjectClientCreate, ProjectClientRead
from app.crud.project_client import add_client_to_project, list_project_clients

router = APIRouter(prefix="/v1/project-clients", tags=["Project Clients"])


@router.post("/", response_model=ProjectClientRead)
async def add(db: AsyncSession = Depends(get_session), payload: ProjectClientCreate = None):
    return await add_client_to_project(db, payload)


@router.get("/{project_id}", response_model=list[ProjectClientRead])
async def list_all(project_id: str, db: AsyncSession = Depends(get_session)):
    return await list_project_clients(db, project_id)
