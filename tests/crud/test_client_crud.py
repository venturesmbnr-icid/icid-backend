import pytest

from app.crud.client import (
    create_client,
    get_client,
    list_clients,
    update_client,
    delete_client,
)
from app.schemas.client import ClientCreate, ClientUpdate


# ----------------------------
# Helpers
# ----------------------------

def sample_client_payload(**overrides):
    data = {
        "client_id": "C001",
        "client_username": "test_client",
        "client_name": "Test Client",
    }
    data.update(overrides)
    return ClientCreate(**data)


# ----------------------------
# Create
# ----------------------------

@pytest.mark.asyncio
async def test_create_client(db_session):
    payload = sample_client_payload()

    client = await create_client(db_session, payload)

    assert client.client_id == payload.client_id


# ----------------------------
# Read
# ----------------------------

@pytest.mark.asyncio
async def test_get_client_found(db_session):
    client = await create_client(db_session, sample_client_payload())

    fetched = await get_client(db_session, client.client_id)

    assert fetched is not None
    assert fetched.client_id == client.client_id


@pytest.mark.asyncio
async def test_get_client_not_found(db_session):
    fetched = await get_client(db_session, "DOES_NOT_EXIST")
    assert fetched is None


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_clients(db_session):
    await create_client(db_session, sample_client_payload(client_id="C001"))
    await create_client(db_session, sample_client_payload(client_id="C002"))

    clients = await list_clients(db_session)

    assert len(clients) == 2
    ids = {c.client_id for c in clients}
    assert ids == {"C001", "C002"}


# ----------------------------
# Update
# ----------------------------

@pytest.mark.asyncio
async def test_update_client_partial(db_session):
    client = await create_client(db_session, sample_client_payload())

    payload = ClientUpdate()
    updated = await update_client(db_session, client.client_id, payload)

    assert updated is not None
    assert updated.client_id == client.client_id


@pytest.mark.asyncio
async def test_update_client_not_found(db_session):
    payload = ClientUpdate()

    updated = await update_client(db_session, "DOES_NOT_EXIST", payload)

    assert updated is None


# ----------------------------
# Delete
# ----------------------------

@pytest.mark.asyncio
async def test_delete_client(db_session):
    client = await create_client(db_session, sample_client_payload())

    ok = await delete_client(db_session, client.client_id)

    assert ok is True
    assert await get_client(db_session, client.client_id) is None


@pytest.mark.asyncio
async def test_delete_client_not_found(db_session):
    ok = await delete_client(db_session, "DOES_NOT_EXIST")
    assert ok is False
