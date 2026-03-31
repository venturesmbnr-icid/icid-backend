import pytest

from app.crud.form_template import (
    create_form_template,
    get_form_template,
    list_form_templates,
    update_form_template,
    delete_form_template,
)
from app.schemas.form_template import FormTemplateCreate, FormTemplateUpdate


# ----------------------------
# Helpers
# ----------------------------

def sample_form_template_payload(**overrides):
    data = {
        "form_template_id": "FT001",
        "form_name": "Inspection Form",
        # "template_json": {
        #     "fields": [
        #         {"id": "f1", "type": "text", "label": "Inspector name"},
        #         {"id": "f2", "type": "checkbox", "label": "Passed"},
        #     ]
        # },
        "is_active": True,
    }

    data.update(overrides)
    return FormTemplateCreate(**data)


# ----------------------------
# Create
# ----------------------------

@pytest.mark.asyncio
async def test_create_form_template(db_session):
    payload = sample_form_template_payload()

    obj = await create_form_template(db_session, payload)

    assert obj.form_template_id == payload.form_template_id
    assert obj.form_name == payload.form_name
    # assert obj.template_json == payload.template_json


# ----------------------------
# Read
# ----------------------------

@pytest.mark.asyncio
async def test_get_form_template_found(db_session):
    obj = await create_form_template(
        db_session,
        sample_form_template_payload(),
    )

    fetched = await get_form_template(db_session, obj.form_template_id)

    assert fetched is not None
    assert fetched.form_template_id == obj.form_template_id


@pytest.mark.asyncio
async def test_get_form_template_not_found(db_session):
    fetched = await get_form_template(db_session, "NON_EXISTENT")
    assert fetched is None


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_form_templates(db_session):
    await create_form_template(
        db_session,
        sample_form_template_payload(form_template_id="FT001"),
    )
    await create_form_template(
        db_session,
        sample_form_template_payload(form_template_id="FT002"),
    )

    items = await list_form_templates(db_session)

    assert len(items) == 2
    ids = {f.form_template_id for f in items}
    assert ids == {"FT001", "FT002"}


# ----------------------------
# Update
# ----------------------------

@pytest.mark.asyncio
async def test_update_form_template_partial(db_session):
    obj = await create_form_template(
        db_session,
        sample_form_template_payload(),
    )

    payload = FormTemplateUpdate(
        form_name="Inspection Form - Updated",
    )

    updated = await update_form_template(db_session, obj.form_template_id, payload)

    assert updated is not None
    assert updated.form_name == "Inspection Form - Updated"
    # assert updated.template_json == obj.template_json  # unchanged


@pytest.mark.asyncio
async def test_update_form_template_not_found(db_session):
    payload = FormTemplateUpdate(name="Nope")

    updated = await update_form_template(db_session, "NON_EXISTENT", payload)

    assert updated is None


# ----------------------------
# Delete
# ----------------------------

@pytest.mark.asyncio
async def test_delete_form_template(db_session):
    obj = await create_form_template(
        db_session,
        sample_form_template_payload(),
    )

    ok = await delete_form_template(db_session, obj.form_template_id)

    assert ok is True
    assert await get_form_template(db_session, obj.form_template_id) is None

@pytest.mark.asyncio
async def test_delete_form_template_not_found(db_session):
    ok = await delete_form_template(db_session, "NON_EXISTENT")
    assert ok is False
