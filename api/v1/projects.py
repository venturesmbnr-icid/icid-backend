from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.crud.project import (
    create_project, get_project, list_projects, update_project, delete_project
)

router = APIRouter(prefix="/v1/projects", tags=["Projects"])


@router.post("/", response_model=ProjectRead)
async def create(db: AsyncSession = Depends(get_session), payload: ProjectCreate = None):
    return await create_project(db, payload)


@router.get("/", response_model=list[ProjectRead])
async def list_all(db: AsyncSession = Depends(get_session)):
    return await list_projects(db)


@router.get("/{project_id}", response_model=ProjectRead)
async def read(project_id: str, db: AsyncSession = Depends(get_session)):
    obj = await get_project(db, project_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj


@router.put("/{project_id}", response_model=ProjectRead)
async def update(project_id: str, payload: ProjectUpdate, db: AsyncSession = Depends(get_session)):
    obj = await update_project(db, project_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj


@router.delete("/{project_id}")
async def delete(project_id: str, db: AsyncSession = Depends(get_session)):
    ok = await delete_project(db, project_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"status": "deleted"}
