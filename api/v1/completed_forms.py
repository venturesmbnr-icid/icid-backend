from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

from app.db.session import get_session
from app.schemas.completed_form import CompletedFormCreate, CompletedFormRead, CompletedFormUpdate
from app.crud.completed_form import (
    create_completed_form, get_completed_form, list_completed_forms,
    update_completed_form, delete_completed_form
)

router = APIRouter(prefix="/v1/completed-forms", tags=["Completed Forms"])


@router.post("/", response_model=CompletedFormRead)
async def create(db: AsyncSession = Depends(get_session), payload: CompletedFormCreate = None):
    return await create_completed_form(db, payload)


@router.get("/", response_model=list[CompletedFormRead])
async def list_all(report_id: str | None = None, db: AsyncSession = Depends(get_session)):
    return await list_completed_forms(db, report_id)


@router.get("/{form_id}", response_model=CompletedFormRead)
async def read(form_id: UUID, db: AsyncSession = Depends(get_session)):
    obj = await get_completed_form(db, form_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Completed form not found")
    return obj


@router.put("/{form_id}", response_model=CompletedFormRead)
async def update(form_id: UUID, payload: CompletedFormUpdate, db: AsyncSession = Depends(get_session)):
    obj = await update_completed_form(db, form_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Completed form not found")
    return obj


@router.delete("/{form_id}")
async def delete(form_id: UUID, db: AsyncSession = Depends(get_session)):
    ok = await delete_completed_form(db, form_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Completed form not found")
    return {"status": "deleted"}
