from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.schemas.report import ReportCreate, ReportRead, ReportUpdate
from app.crud.report import (
    create_report, get_report, list_reports, update_report, delete_report
)

router = APIRouter(prefix="/v1/reports", tags=["Reports"])


@router.post("/", response_model=ReportRead)
async def create(db: AsyncSession = Depends(get_session), payload: ReportCreate = None):
    return await create_report(db, payload)


@router.get("/", response_model=list[ReportRead])
async def list_all(project_id: str | None = None, db: AsyncSession = Depends(get_session)):
    return await list_reports(db, project_id)


@router.get("/{report_id}", response_model=ReportRead)
async def read(report_id: str, db: AsyncSession = Depends(get_session)):
    obj = await get_report(db, report_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Report not found")
    return obj


@router.put("/{report_id}", response_model=ReportRead)
async def update(report_id: str, payload: ReportUpdate, db: AsyncSession = Depends(get_session)):
    obj = await update_report(db, report_id, payload)
    if not obj:
        raise HTTPException(status_code=404, detail="Report not found")
    return obj


@router.delete("/{report_id}")
async def delete(report_id: str, db: AsyncSession = Depends(get_session)):
    ok = await delete_report(db, report_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"status": "deleted"}
