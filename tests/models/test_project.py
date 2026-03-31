import pytest
from sqlalchemy.exc import IntegrityError

from app.models.project import Project


@pytest.mark.asyncio
async def test_create_project_success(db_session):
    project = Project(
        project_id="P100",
        project_name="Test Project",
        project_description="Test description",
        registration_code="REG-001",
        borough="Manhattan",
        status="ACTIVE",
    )

    db_session.add(project)
    await db_session.flush()

    assert project.project_id == "P100"
    assert project.project_name == "Test Project"
    assert project.registration_code == "REG-001"
    assert project.status == "ACTIVE"


@pytest.mark.asyncio
async def test_project_requires_project_name(db_session):
    project = Project(
        project_id="P101",
        registration_code="REG-002",
        status="ACTIVE",
    )

    db_session.add(project)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_requires_registration_code(db_session):
    project = Project(
        project_id="P102",
        project_name="Missing Registration",
        status="ACTIVE",
    )

    db_session.add(project)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_requires_status(db_session):
    project = Project(
        project_id="P103",
        project_name="Missing Status",
        registration_code="REG-003",
    )

    db_session.add(project)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_registration_code_unique(db_session):
    project1 = Project(
        project_id="P104",
        project_name="Project One",
        registration_code="REG-004",
        status="ACTIVE",
    )

    project2 = Project(
        project_id="P105",
        project_name="Project Two",
        registration_code="REG-004",  # duplicate
        status="ACTIVE",
    )

    db_session.add_all([project1, project2])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_timestamps_are_set(db_session):
    project = Project(
        project_id="P106",
        project_name="Timestamp Test",
        registration_code="REG-005",
        status="ACTIVE",
    )

    db_session.add(project)
    await db_session.flush()

    assert project.created_at is not None
    assert project.updated_at is not None
