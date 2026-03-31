import pytest

from app.crud.project import (
    create_project,
    get_project,
    list_projects,
    update_project,
    delete_project,
)
from app.schemas.project import ProjectCreate, ProjectUpdate


# ----------------------------
# Helpers
# ----------------------------

def sample_project_payload(**overrides):
    project_id = overrides.get("project_id", "P001")

    data = {
        "project_id": project_id,
        "project_name": "Test Project",
        "registration_code": f"REG-{project_id}",
        "borough": "Manhattan",
        "status": "active",
    }
    data.update(overrides)
    return ProjectCreate(**data)


# ----------------------------
# Create
# ----------------------------

@pytest.mark.asyncio
async def test_create_project(db_session, test_client):
    payload = sample_project_payload()

    project = await create_project(db_session, payload)

    assert project.project_id == payload.project_id
    assert project.project_name == payload.project_name


# ----------------------------
# Read
# ----------------------------

@pytest.mark.asyncio
async def test_get_project_found(db_session, test_client):
    project = await create_project(db_session, sample_project_payload())

    fetched = await get_project(db_session, project.project_id)

    assert fetched is not None
    assert fetched.project_id == project.project_id


@pytest.mark.asyncio
async def test_get_project_not_found(db_session):
    fetched = await get_project(db_session, "DOES_NOT_EXIST")
    assert fetched is None


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_projects(db_session, test_client):
    await create_project(db_session, sample_project_payload(project_id="P001"))
    await create_project(db_session, sample_project_payload(project_id="P002"))

    projects = await list_projects(db_session)

    assert len(projects) == 2
    ids = {p.project_id for p in projects}
    assert ids == {"P001", "P002"}


# ----------------------------
# Update
# ----------------------------

@pytest.mark.asyncio
async def test_update_project_partial(db_session, test_client):
    project = await create_project(db_session, sample_project_payload())

    payload = ProjectUpdate(project_name="Updated Project")
    updated = await update_project(db_session, project.project_id, payload)

    assert updated is not None
    assert updated.project_name == "Updated Project"
    assert updated.project_id == project.project_id


@pytest.mark.asyncio
async def test_update_project_not_found(db_session):
    payload = ProjectUpdate(project_name="Updated Project")

    updated = await update_project(db_session, "DOES_NOT_EXIST", payload)

    assert updated is None


# ----------------------------
# Delete
# ----------------------------

@pytest.mark.asyncio
async def test_delete_project(db_session, test_client):
    project = await create_project(db_session, sample_project_payload())

    ok = await delete_project(db_session, project.project_id)

    assert ok is True
    assert await get_project(db_session, project.project_id) is None


@pytest.mark.asyncio
async def test_delete_project_not_found(db_session):
    ok = await delete_project(db_session, "DOES_NOT_EXIST")
    assert ok is False
