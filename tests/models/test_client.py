import pytest
from sqlalchemy.exc import IntegrityError

from api.models.client import Client
from api.models.user import User


@pytest.mark.asyncio
async def test_create_client_success(db_session):
    client = Client(
        client_id="C100",
        client_username="client_100",
        client_name="Test Client"
    )
    db_session.add(client)
    await db_session.flush()

    assert client.client_id == "C100"
    assert client.client_username == "client_100"
    assert client.client_name == "Test Client"


@pytest.mark.asyncio
async def test_client_requires_client_username(db_session):
    client = Client(
        client_id="C101",
        client_name="Missing Username"
    )
    db_session.add(client)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_client_requires_client_name(db_session):
    client = Client(
        client_id="C101",
        client_username="no_id_client",
    )
    db_session.add(client)

    with pytest.raises(IntegrityError):
        await db_session.flush()

@pytest.mark.asyncio
async def test_client_user_relationship(db_session):
    client = Client(
        client_id="C102",
        client_username="rel_client",
        client_name="Relationship Client"
    )
    db_session.add(client)
    await db_session.flush()

    user = User(
        email="user1@test.com",
        first_name="Test",
        last_name="User",
        client_id=client.client_id
    )
    db_session.add(user)
    await db_session.flush()

    assert user.client is client

    await db_session.flush()
    await db_session.refresh(client)
    
    assert len(client.users) == 1
    assert client.users[0].email == "user1@test.com"


@pytest.mark.asyncio
async def test_client_delete_cascades_users(db_session):
    client = Client(
        client_id="C103",
        client_username="cascade_client",
        client_name="Cascade Client"
    )
    db_session.add(client)
    await db_session.flush()

    user = User(
        email="cascade@test.com",
        first_name="Cascade",
        last_name="User",
        client_id=client.client_id
    )
    db_session.add(user)
    await db_session.flush()

    await db_session.delete(client)
    await db_session.flush()

    remaining_users = (
        await db_session.execute(
            User.__table__.select()
        )
    ).fetchall()

    assert len(remaining_users) == 0
