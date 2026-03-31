# app/crud/report.py

from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportUpdate
from typing import List, Optional


async def create_report(db: AsyncSession, payload: ReportCreate) -> Report:
    obj = Report(**payload.dict())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


async def get_report(db: AsyncSession, report_id: str) -> Optional[Report]:
    result = await db.execute(select(Report).where(Report.report_id == report_id))
    return result.scalar_one_or_none()


async def list_reports(db: AsyncSession, project_id: Optional[str] = None) -> List[Report]:
    query = select(Report)
    if project_id:
        query = query.where(Report.project_id == project_id)

    result = await db.execute(query)
    return result.scalars().all()


async def update_report(db: AsyncSession, report_id: str, payload: ReportUpdate) -> Optional[Report]:
    obj = await get_report(db, report_id)
    if not obj:
        return None

    update_data = payload.dict(exclude_unset=True)

    if "report_date" in update_data and isinstance(update_data["report_date"], str):
        update_data["report_date"] = date.fromisoformat(update_data["report_date"])

    for field, value in update_data.items():
        setattr(obj, field, value)


    await db.commit()
    await db.refresh(obj)
    return obj


async def delete_report(db: AsyncSession, report_id: str) -> bool:
    obj = await get_report(db, report_id)
    if not obj:
        return False

    await db.delete(obj)
    await db.commit()
    return True
