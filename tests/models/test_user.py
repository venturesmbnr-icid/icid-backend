import pytest
from sqlalchemy.exc import IntegrityError

from app.models.user import User
from app.models.client import Client


@pytest.mark.asyncio
async def test_create_user_success(db_session):
    client = Client(client_id="C001", client_name="Test Client", client_username="test_client")

    db_session.add(client)
    await db_session.flush()

    user = User(
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        phone_number="555-1111",
        client_id=client.client_id,
    )

    db_session.add(user)
    await db_session.commit()

    assert user.uuid is not None
    assert user.email == "john@example.com"
    assert user.client_id == "C001"
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_user_requires_email(db_session):
    client = Client(client_id="C002", client_name="Test Client", client_username="test_client")
    db_session.add(client)  
    await db_session.flush()

    user = User(email=None, client_id=client.client_id)
    db_session.add(user)

    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_user_requires_client(db_session):
    user = User(email="no_client@example.com", client_id="NON_EXISTENT")
    db_session.add(user)

    with pytest.raises(IntegrityError):
        await db_session.commit()


@pytest.mark.asyncio
async def test_user_client_relationship(db_session):
    client = Client(client_id="C003", client_name="Relationship Client", client_username="rel_client")
    db_session.add(client)
    await db_session.flush()

    user = User(email="rel@example.com", client_id=client.client_id)
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    assert user.client is not None
    assert user.client.client_id == "C003"
