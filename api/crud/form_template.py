# app/crud/form_template.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.form_template import FormTemplate
from app.schemas.form_template import FormTemplateCreate, FormTemplateUpdate
from typing import List, Optional


async def create_form_template(
    db: AsyncSession,
    payload: FormTemplateCreate,
) -> FormTemplate:
    obj = FormTemplate(
        form_template_id=payload.form_template_id,
        form_name=payload.form_name,
        form_description=payload.form_description,
    )

    db.add(obj)
    await db.flush()
    return obj



async def get_form_template(
    db: AsyncSession,
    template_id: str,
) -> Optional[FormTemplate]:
    result = await db.execute(
        select(FormTemplate).where(
                FormTemplate.form_template_id == template_id
            )
    )
    return result.scalar_one_or_none()


async def list_form_templates(
    db: AsyncSession,
) -> List[FormTemplate]:
    result = await db.execute(select(FormTemplate))
    return result.scalars().all()


async def update_form_template(
    db: AsyncSession,
    template_id: str,
    payload: FormTemplateUpdate,
) -> Optional[FormTemplate]:

    obj = await get_form_template(db, template_id)
    if not obj:
        return None

    if payload.form_name is not None:
        obj.form_name = payload.form_name

    # if payload.template_json is not None:
    #     obj.template_json = payload.template_json

    if payload.form_description is not None:
        obj.form_description = payload.form_description

    await db.flush()
    return obj


async def delete_form_template(
    db: AsyncSession,
    template_id: str,
) -> bool:
    obj = await get_form_template(db, template_id)
    if not obj:
        return False

    await db.delete(obj)
    await db.commit()
    return True
