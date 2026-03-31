import pytest
from datetime import date

from app.crud.report import (
    create_report,
    get_report,
    list_reports,
    update_report,
    delete_report,
)
from app.schemas.report import ReportCreate, ReportUpdate


# ----------------------------
# Helpers
# ----------------------------

def sample_report_payload(*, reporter_uuid: str, **overrides):
    data = {
        "report_id": "R001",
        "report_name": "Test Report",
        "report_type": "inspection",
        "status": "draft",
        "project_id": "P001",
        "reporter_uuid": reporter_uuid,
    }
    data.update(overrides)
    return ReportCreate(**data)


# ----------------------------
# Create
# ----------------------------

@pytest.mark.asyncio
async def test_create_report(db_session, test_project, test_user):
    payload = sample_report_payload(
        project_id=test_project.project_id,
        reporter_uuid=test_user.uuid,
    )
    report = await create_report(db_session, payload)

    assert report.report_id == payload.report_id
    assert report.project_id == test_project.project_id
    assert report.report_id == payload.report_id
    assert report.project_id == test_project.project_id
    assert report.reporter_uuid == test_user.uuid
    assert report.report_date == payload.report_date



# ----------------------------
# Read
# ----------------------------

@pytest.mark.asyncio
async def test_get_report_found(db_session, test_project, test_user):
    report = await create_report(
        db_session,
        sample_report_payload(project_id=test_project.project_id, reporter_uuid=test_user.uuid),
    )

    fetched = await get_report(db_session, report.report_id)

    assert fetched is not None
    assert fetched.report_id == report.report_id


@pytest.mark.asyncio
async def test_get_report_not_found(db_session):
    fetched = await get_report(db_session, "NON_EXISTENT")
    assert fetched is None


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_reports_all(db_session, test_project, test_user):
    await create_report(
        db_session,
        sample_report_payload(report_id="R001", project_id=test_project.project_id, reporter_uuid=test_user.uuid),
    )
    await create_report(
        db_session,
        sample_report_payload(report_id="R002", project_id=test_project.project_id, reporter_uuid=test_user.uuid),
    )

    reports = await list_reports(db_session)

    assert len(reports) == 2
    ids = {r.report_id for r in reports}
    assert ids == {"R001", "R002"}


@pytest.mark.asyncio
async def test_list_reports_by_project(db_session, test_project, test_project_alt, test_user):
    await create_report(
        db_session,
        sample_report_payload(report_id="R001", project_id=test_project.project_id, reporter_uuid=test_user.uuid),
    )
    await create_report(
        db_session,
        sample_report_payload(report_id="R002", project_id=test_project_alt.project_id, reporter_uuid=test_user.uuid),
    )

    reports = await list_reports(db_session, project_id=test_project.project_id)

    assert len(reports) == 1
    assert reports[0].project_id == test_project.project_id


# ----------------------------
# Update
# ----------------------------

@pytest.mark.asyncio
async def test_update_report_partial(db_session, test_project, test_user):
    report = await create_report(
        db_session,
        sample_report_payload(project_id=test_project.project_id, reporter_uuid=test_user.uuid),
    )

    payload = ReportUpdate(report_date="2025-01-01")
    updated = await update_report(db_session, report.report_id, payload)

    assert updated is not None
    assert updated.report_date == date(2025, 1, 1)
    assert updated.reporter_uuid == report.reporter_uuid  # unchanged


@pytest.mark.asyncio
async def test_update_report_not_found(db_session):
    payload = ReportUpdate(status="submitted")

    updated = await update_report(db_session, "NON_EXISTENT", payload)

    assert updated is None


# ----------------------------
# Delete
# ----------------------------

@pytest.mark.asyncio
async def test_delete_report(db_session, test_project, test_user):
    report = await create_report(
        db_session,
        sample_report_payload(project_id=test_project.project_id, reporter_uuid=test_user.uuid),
    )

    ok = await delete_report(db_session, report.report_id)

    assert ok is True
    assert await get_report(db_session, report.report_id) is None


@pytest.mark.asyncio
async def test_delete_report_not_found(db_session):
    ok = await delete_report(db_session, "NON_EXISTENT")
    assert ok is False
