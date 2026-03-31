import pytest
from sqlalchemy.exc import IntegrityError

from app.models.client import Client
from app.models.project import Project
from app.models.project_client import ProjectClient


@pytest.mark.asyncio
async def test_create_project_client_success(db_session):
    client = Client(
        client_id="C300",
        client_username="pc_client",
        client_name="Project Client",
    )

    project = Project(
        project_id="P300",
        project_name="Client Link Project",
        registration_code="PC-001",
        status="ACTIVE",
    )

    link = ProjectClient(
        project=project,
        client=client,
        client_role="OWNER",
    )

    db_session.add_all([client, project, link])
    await db_session.flush()

    assert link.project_id == "P300"
    assert link.client_id == "C300"
    assert link.client_role == "OWNER"


@pytest.mark.asyncio
async def test_project_client_requires_project(db_session):
    client = Client(
        client_id="C301",
        client_username="no_project_client",
        client_name="No Project Client",
    )

    link = ProjectClient(
        client=client,
    )

    db_session.add_all([client, link])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_client_requires_client(db_session):
    project = Project(
        project_id="P301",
        project_name="No Client Project",
        registration_code="PC-002",
        status="ACTIVE",
    )

    link = ProjectClient(
        project=project,
    )

    db_session.add_all([project, link])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_project_delete_cascades_project_clients(db_session):
    client = Client(
        client_id="C302",
        client_username="cascade_client",
        client_name="Cascade Client",
    )

    project = Project(
        project_id="P302",
        project_name="Cascade Project",
        registration_code="PC-003",
        status="ACTIVE",
    )

    link = ProjectClient(
        project=project,
        client=client,
    )

    db_session.add_all([client, project, link])
    await db_session.flush()

    await db_session.delete(project)
    await db_session.flush()

    result = await db_session.get(ProjectClient, ("P302", "C302"))
    assert result is None


@pytest.mark.asyncio
async def test_client_delete_cascades_project_clients(db_session):
    client = Client(
        client_id="C303",
        client_username="cascade_client2",
        client_name="Cascade Client 2",
    )

    project = Project(
        project_id="P303",
        project_name="Cascade Project 2",
        registration_code="PC-004",
        status="ACTIVE",
    )

    link = ProjectClient(
        project=project,
        client=client,
    )

    db_session.add_all([client, project, link])
    await db_session.flush()

    await db_session.delete(client)
    await db_session.flush()

    result = await db_session.get(ProjectClient, ("P303", "C303"))
    assert result is None
