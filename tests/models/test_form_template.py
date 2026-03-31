# tests/models/test_form_template.py

import pytest
from sqlalchemy.exc import IntegrityError

from app.models.form_template import FormTemplate


@pytest.mark.asyncio
async def test_create_form_template_success(db_session):
    template = FormTemplate(
        form_template_id="TMP-001",
        form_name="Daily Inspection",
        form_description="Daily site inspection form",    )

    db_session.add(template)
    await db_session.flush()

    assert template.form_template_id == "TMP-001"
    assert template.form_name == "Daily Inspection"
    assert template.created_at is not None
    assert template.updated_at is not None


@pytest.mark.asyncio
async def test_form_template_requires_form_template_id(db_session):
    template = FormTemplate(
        form_name="Missing ID",
    )

    db_session.add(template)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_form_template_id_must_be_unique(db_session):
    t1 = FormTemplate(
        form_template_id="TMP-002",
        form_name="Template One",
    )

    t2 = FormTemplate(
        form_template_id="TMP-002",
        form_name="Template Two",
    )

    db_session.add_all([t1, t2])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_form_template_requires_form_name(db_session):
    template = FormTemplate(
        form_template_id="TMP-003",
    )

    db_session.add(template)

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_form_template_template_json_is_optional(db_session):
    template = FormTemplate(
        form_template_id="TMP-004",
        form_name="No JSON",
    )

    db_session.add(template)
    await db_session.flush()

    assert template.form_template_id == "TMP-004"


@pytest.mark.asyncio
async def test_form_template_timestamps_are_set(db_session):
    template = FormTemplate(
        form_template_id="TMP-005",
        form_name="Timestamp Test",
    )

    db_session.add(template)
    await db_session.flush()

    assert template.created_at is not None
    assert template.updated_at is not None
