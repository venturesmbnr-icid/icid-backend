import pytest
from sqlalchemy.exc import IntegrityError

from app.models.client import Client
from app.models.user import User
from app.models.project import Project
from app.models.report import Report


@pytest.mark.asyncio
async def test_create_report_success(db_session):
    client = Client(
        client_id="C200",
        client_username="report_client",
        client_name="Report Client",
    )

    user = User(
        email="reporter@example.com",
        client=client,
    )

    project = Project(
        project_id="P200",
        project_name="Report Project",
        registration_code="REP-001",
        status="ACTIVE",
    )

    report = Report(
        report_id="R200",
        reporter=user,
        project=project,
    )

    db_session.add_all([client, user, project, report])
    await db_session.flush()

    assert report.report_id == "R200"
    assert report.reporter is user
    assert report.project is project


@pytest.mark.asyncio
async def test_report_requires_reporter(db_session):
    project = Project(
        project_id="P201",
        project_name="No Reporter Project",
        registration_code="REP-002",
        status="ACTIVE",
    )

    report = Report(
        report_id="R201",
        project=project,
    )

    db_session.add_all([project, report])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_report_requires_project(db_session):
    client = Client(
        client_id="C202",
        client_username="no_project_client",
        client_name="No Project Client",
    )

    user = User(
        email="no_project@example.com",
        client=client,
    )

    report = Report(
        report_id="R202",
        reporter=user,
    )

    db_session.add_all([client, user, report])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_delete_cascades_reports(db_session):
    client = Client(
        client_id="C203",
        client_username="cascade_project_client",
        client_name="Cascade Project Client",
    )

    user = User(
        email="cascade_reporter@example.com",
        client=client,
    )

    project = Project(
        project_id="P203",
        project_name="Cascade Project",
        registration_code="REP-003",
        status="ACTIVE",
    )

    report = Report(
        report_id="R203",
        reporter=user,
        project=project,
    )

    db_session.add_all([client, user, project, report])
    await db_session.flush()

    await db_session.delete(project)
    await db_session.flush()

    remaining = (
        await db_session.execute(Report.__table__.select())
    ).fetchall()

    assert len(remaining) == 0


@pytest.mark.asyncio
async def test_report_timestamps_are_set(db_session):
    client = Client(
        client_id="C204",
        client_username="timestamp_client",
        client_name="Timestamp Client",
    )

    user = User(
        email="timestamp@example.com",
        client=client,
    )

    project = Project(
        project_id="P204",
        project_name="Timestamp Project",
        registration_code="REP-004",
        status="ACTIVE",
    )

    report = Report(
        report_id="R204",
        reporter=user,
        project=project,
    )

    db_session.add_all([client, user, project, report])
    await db_session.flush()

    assert report.created_at is not None
    assert report.updated_at is not None
