# app/crud/completed_form.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.completed_form import CompletedForm
from app.schemas.completed_form import CompletedFormCreate, CompletedFormUpdate
from typing import List, Optional
from uuid import UUID


async def create_completed_form(db: AsyncSession, payload: CompletedFormCreate) -> CompletedForm:
    data = payload.dict(
        exclude={
            "created_at",
            "updated_at",
        }
    )

    obj = CompletedForm(
        completed_form_id=data["completed_form_id"],
        report_id=data["report_id"],
        template_id=data["form_template_id"],
        form_data=data.get("form_data"),
    )

    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_completed_form(db: AsyncSession, form_id: UUID) -> Optional[CompletedForm]:
    result = await db.execute(select(CompletedForm).where(CompletedForm.id == form_id))
    return result.scalar_one_or_none()


async def list_completed_forms(db: AsyncSession, report_id: Optional[str] = None) -> List[CompletedForm]:
    query = select(CompletedForm)
    if report_id:
        query = query.where(CompletedForm.report_id == report_id)

    result = await db.execute(query)
    return result.scalars().all()


async def update_completed_form(db: AsyncSession, form_id: UUID, payload: CompletedFormUpdate) -> Optional[CompletedForm]:
    obj = await get_completed_form(db, form_id)
    if not obj:
        return None

    if payload.form_data is not None:
        obj.form_data = payload.form_data

    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_completed_form(db: AsyncSession, form_id: UUID) -> bool:
    obj = await get_completed_form(db, form_id)
    if not obj:
        return False

    await db.delete(obj)
    await db.commit()
    return True
