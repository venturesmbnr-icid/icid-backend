from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.form_template import FormTemplateCreate, FormTemplateRead, FormTemplateUpdate
from app.crud.form_template import (
    create_form_template, get_form_template, list_form_templates,
    update_form_template, delete_form_template
)

router = APIRouter(prefix="/v1/form-templates", tags=["Form Templates"])


@router.post("/", response_model=FormTemplateRead)
async def create(db: AsyncSession = Depends(get_session), payload: FormTemplateCreate = None):
    return await create_form_template(db, payload)


@router.get("/", response_model=list[FormTemplateRead])
async def list_all(db: AsyncSession = Depends(get_session)):
    return await list_form_templates(db)


@router.get("/{form_template_id}", response_model=FormTemplateRead)
async def read(form_template_id: str, db: AsyncSession = Depends(get_session)):
    obj = await get_form_template(db, form_template_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Form template not found")
    return obj


@router.put("/{form_template_id}", response_model=FormTemplateRead)
async def update(form_template_id: str, payload: FormTemplateUpdate, db: AsyncSession = Depends(get_session)):
    obj = await update_form_template(db, form_template_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Form template not found")
    return obj


@router.delete("/{form_template_id}")
async def delete(form_template_id: str, db: AsyncSession = Depends(get_session)):
    ok = await delete_form_template(db, form_template_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Form template not found")
    return {"status": "deleted"}
