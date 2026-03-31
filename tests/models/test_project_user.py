import pytest
from sqlalchemy.exc import IntegrityError

from app.models.client import Client
from app.models.user import User
from app.models.project import Project
from app.models.project_user import ProjectUser


@pytest.mark.asyncio
async def test_create_project_user_success(db_session):
    client = Client(
        client_id="C300",
        client_username="proj_user_client",
        client_name="Project User Client",
    )

    user = User(
        email="user@project.com",
        client=client,
    )

    project = Project(
        project_id="P300",
        project_name="Project User Test",
        registration_code="PU-001",
        status="ACTIVE",
    )

    assignment = ProjectUser(
        project=project,
        user=user,
        user_role="EDITOR",
    )

    db_session.add_all([client, user, project, assignment])
    await db_session.flush()

    assert assignment.project_id == project.project_id
    assert assignment.user_id == user.uuid
    assert assignment.user_role == "EDITOR"


@pytest.mark.asyncio
async def test_project_user_requires_project(db_session):
    client = Client(
        client_id="C301",
        client_username="no_project_client",
        client_name="No Project Client",
    )

    user = User(
        email="no_project@user.com",
        client=client,
    )

    assignment = ProjectUser(
        user=user,
        user_role="VIEWER",
    )

    db_session.add_all([client, user, assignment])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_user_requires_user(db_session):
    project = Project(
        project_id="P301",
        project_name="No User Project",
        registration_code="PU-002",
        status="ACTIVE",
    )

    assignment = ProjectUser(
        project=project,
        user_role="VIEWER",
    )

    db_session.add_all([project, assignment])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_user_relationships(db_session):
    client = Client(
        client_id="C302",
        client_username="rel_client",
        client_name="Relationship Client",
    )

    user = User(
        email="rel@user.com",
        client=client,
    )

    project = Project(
        project_id="P302",
        project_name="Relationship Project",
        registration_code="PU-003",
        status="ACTIVE",
    )

    assignment = ProjectUser(
        project=project,
        user=user,
        user_role="OWNER",
    )

    db_session.add_all([client, user, project, assignment])
    await db_session.flush()

    assert assignment in user.project_assignments
    assert assignment in project.project_assignments
    assert assignment.user is user
    assert assignment.project is project


@pytest.mark.asyncio
async def test_project_delete_cascades_project_users(db_session):
    client = Client(
        client_id="C303",
        client_username="cascade_client",
        client_name="Cascade Client",
    )

    user = User(
        email="cascade@user.com",
        client=client,
    )

    project = Project(
        project_id="P303",
        project_name="Cascade Project",
        registration_code="PU-004",
        status="ACTIVE",
    )

    assignment = ProjectUser(
        project=project,
        user=user,
    )

    db_session.add_all([client, user, project, assignment])
    await db_session.flush()

    await db_session.delete(project)
    await db_session.flush()

    remaining = (
        await db_session.execute(ProjectUser.__table__.select())
    ).fetchall()

    assert len(remaining) == 0
