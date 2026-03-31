import pytest
from uuid import uuid4

from app.crud.user import (
    create_user,
    get_user,
    list_users,
    update_user,
    delete_user,
)
from app.schemas.user import UserCreate, UserUpdate


# ----------------------------
# Helpers
# ----------------------------

def sample_user_payload(**overrides):
    data = {
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "555-1111",
        "client_id": "C001",
    }
    data.update(overrides)
    return UserCreate(**data)


# ----------------------------
# Create
# ----------------------------

@pytest.mark.asyncio
async def test_create_user(db_session, test_client):
    payload = sample_user_payload()

    user = await create_user(db_session, payload)

    assert user.uuid is not None
    assert user.email == payload.email
    assert user.first_name == payload.first_name
    assert user.client_id == test_client.client_id


# ----------------------------
# Read
# ----------------------------

@pytest.mark.asyncio
async def test_get_user_found(db_session, test_client):
    user = await create_user(db_session, sample_user_payload())

    fetched = await get_user(db_session, user.uuid)

    assert fetched is not None
    assert fetched.uuid == user.uuid


@pytest.mark.asyncio
async def test_get_user_not_found(db_session):
    fetched = await get_user(db_session, uuid4())
    assert fetched is None


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_users(db_session, test_client):
    await create_user(db_session, sample_user_payload(email="a@a.com"))
    await create_user(db_session, sample_user_payload(email="b@b.com"))

    users = await list_users(db_session)

    assert len(users) == 2
    emails = {u.email for u in users}
    assert emails == {"a@a.com", "b@b.com"}


# ----------------------------
# Update
# ----------------------------

@pytest.mark.asyncio
async def test_update_user_partial(db_session, test_client):
    user = await create_user(db_session, sample_user_payload())

    payload = UserUpdate(first_name="Updated")
    updated = await update_user(db_session, user.uuid, payload)

    assert updated is not None
    assert updated.first_name == "Updated"
    assert updated.last_name == user.last_name


@pytest.mark.asyncio
async def test_update_user_not_found(db_session):
    payload = UserUpdate(first_name="Updated")

    updated = await update_user(db_session, uuid4(), payload)

    assert updated is None


# ----------------------------
# Delete
# ----------------------------

@pytest.mark.asyncio
async def test_delete_user(db_session, test_client):
    user = await create_user(db_session, sample_user_payload())

    ok = await delete_user(db_session, user.uuid)

    assert ok is True
    assert await get_user(db_session, user.uuid) is None


@pytest.mark.asyncio
async def test_delete_user_not_found(db_session):
    ok = await delete_user(db_session, uuid4())
    assert ok is False
