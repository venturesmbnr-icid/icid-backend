import pytest
from app.models.client import Client


from app.crud.project_client import (
    add_client_to_project,
    list_project_clients,
)
from app.schemas.project_client import ProjectClientCreate


# ----------------------------
# Helpers
# ----------------------------

def sample_project_client_payload(*, project_id: str, client_id: str):
    return ProjectClientCreate(
        project_id=project_id,
        client_id=client_id,
    )


# ----------------------------
# Add
# ----------------------------

@pytest.mark.asyncio
async def test_add_client_to_project(db_session, test_project, test_client):
    payload = sample_project_client_payload(
        project_id=test_project.project_id,
        client_id=test_client.client_id,
    )

    obj = await add_client_to_project(db_session, payload)

    assert obj.project_id == test_project.project_id
    assert obj.client_id == test_client.client_id


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_project_clients(db_session, test_project, test_client):
    # create second client explicitly
    client2 = Client(
        client_id="C999",
        client_username="alt_client",
        client_name="Alt Client",
    )
    db_session.add(client2)
    await db_session.commit()
    await db_session.refresh(client2)

    await add_client_to_project(
        db_session,
        sample_project_client_payload(
            project_id=test_project.project_id,
            client_id=test_client.client_id,
        ),
    )

    await add_client_to_project(
        db_session,
        sample_project_client_payload(
            project_id=test_project.project_id,
            client_id=client2.client_id,
        ),
    )

    clients = await list_project_clients(db_session, project_id=test_project.project_id)

    assert len(clients) == 2
    ids = {c.client_id for c in clients}
    assert ids == {test_client.client_id, client2.client_id}
