import pytest
from uuid import uuid4

from app.crud.project_user import (
    assign_user_to_project,
    list_project_users,
)
from app.schemas.project_user import ProjectUserCreate
from app.models.user import User


# ----------------------------
# Helpers
# ----------------------------

def sample_project_user_payload(*, project_id: str, user_uuid, **overrides):
    data = {
        "project_id": project_id,
        "user_uuid": user_uuid,
        "user_role": "member",
    }
    data.update(overrides)
    return ProjectUserCreate(**data)


# ----------------------------
# Create / Assign
# ----------------------------

@pytest.mark.asyncio
async def test_assign_user_to_project(db_session, test_project, test_user):
    payload = sample_project_user_payload(
    project_id=test_project.project_id,
    user_uuid=test_user.uuid,
)

    obj = await assign_user_to_project(db_session, payload)

    assert obj.project_id == test_project.project_id
    assert obj.user_id == test_user.uuid
    assert obj.user_role == "member"


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_project_users(db_session, test_project, test_user):
    # create second user explicitly
    user2 = User(
        uuid=uuid4(),
        email="alt@example.com",
        first_name="Alt",
        last_name="User",
        client_id=test_user.client_id,
    )
    db_session.add(user2)
    await db_session.commit()
    await db_session.refresh(user2)

    await assign_user_to_project(
        db_session,
        sample_project_user_payload(
            project_id=test_project.project_id,
            user_uuid=test_user.uuid,
        ),
    )

    await assign_user_to_project(
        db_session,
        sample_project_user_payload(
            project_id=test_project.project_id,
            user_uuid=user2.uuid,   # ✅ second user
            user_role="admin",
        ),
    )

    users = await list_project_users(db_session, project_id=test_project.project_id)

    assert len(users) == 2

    roles = {u.user_id: u.user_role for u in users}
    assert roles[test_user.uuid] == "member"
    assert roles[user2.uuid] == "admin"


@pytest.mark.asyncio
async def test_list_project_users_empty(db_session, test_project):
    users = await list_project_users(db_session, project_id=test_project.project_id)
    assert users == []
