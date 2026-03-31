# tests/crud/test_completed_form.py

import pytest
import json
from uuid import uuid4

from app.crud.completed_form import (
    create_completed_form,
    get_completed_form,
    list_completed_forms,
    update_completed_form,
    delete_completed_form,
)
from app.schemas.completed_form import CompletedFormCreate, CompletedFormUpdate

from app.crud.report import create_report
from app.schemas.report import ReportCreate

from app.crud.form_template import create_form_template
from app.schemas.form_template import FormTemplateCreate


# ----------------------------
# Helpers
# ----------------------------
def sample_completed_form_payload(*, report_id: str, form_template_id: str, **overrides):
    data = {
        "completed_form_id": str(uuid4()),  # ✅ STRING, not UUID
        "report_id": report_id,
        "form_template_id": form_template_id,
        "response_json": {"field1": "value1"},
        "submitted_by": None,
    }
    data.update(overrides)
    return CompletedFormCreate(**data)


async def create_test_report(db_session, *, project_id: str, reporter_uuid):
    payload = ReportCreate(
        report_id=uuid4().hex,
        project_id=project_id,
        reporter_uuid=reporter_uuid,
    )
    return await create_report(db_session, payload)


async def create_test_form_template(db_session):
    payload = FormTemplateCreate(
        form_template_id=uuid4().hex,
        form_name="Test Template",
        template_json={"fields": []},
    )
    return await create_form_template(db_session, payload)


# ----------------------------
# Create
# ----------------------------

@pytest.mark.asyncio
async def test_create_completed_form(db_session, test_project, test_user):
    report = await create_test_report(
        db_session,
        project_id=test_project.project_id,
        reporter_uuid=test_user.uuid,
    )
    form_template = await create_test_form_template(db_session)

    payload = sample_completed_form_payload(
        report_id=report.report_id,
        form_template_id=form_template.form_template_id,
    )

    obj = await create_completed_form(db_session, payload)

    assert obj.id is not None
    assert obj.completed_form_id == payload.completed_form_id
    assert obj.report_id == payload.report_id
    assert obj.template_id == payload.form_template_id
    assert obj.report_id == report.report_id


# ----------------------------
# Read
# ----------------------------

@pytest.mark.asyncio
async def test_get_completed_form_found(db_session, test_project, test_user):
    report = await create_test_report(
        db_session,
        project_id=test_project.project_id,
        reporter_uuid=test_user.uuid,
    )
    form_template = await create_test_form_template(db_session)

    obj = await create_completed_form(
        db_session,
        sample_completed_form_payload(
            report_id=report.report_id,
            form_template_id=form_template.form_template_id,
        ),
    )

    fetched = await get_completed_form(db_session, obj.id)

    assert fetched is not None
    assert fetched.id == obj.id


@pytest.mark.asyncio
async def test_get_completed_form_not_found(db_session):
    fetched = await get_completed_form(db_session, uuid4())
    assert fetched is None


# ----------------------------
# List
# ----------------------------

@pytest.mark.asyncio
async def test_list_completed_forms_all(db_session, test_project, test_user):
    report = await create_test_report(
        db_session,
        project_id=test_project.project_id,
        reporter_uuid=test_user.uuid,
    )
    form_template = await create_test_form_template(db_session)

    await create_completed_form(
        db_session,
        sample_completed_form_payload(
            report_id=report.report_id,
            form_template_id=form_template.form_template_id,
        ),
    )
    await create_completed_form(
        db_session,
        sample_completed_form_payload(
            report_id=report.report_id,
            form_template_id=form_template.form_template_id,
        ),
    )

    items = await list_completed_forms(db_session)

    assert len(items) == 2


@pytest.mark.asyncio
async def test_list_completed_forms_by_report(db_session, test_project, test_project_alt, test_user):
    report1 = await create_test_report(
        db_session,
        project_id=test_project.project_id,
        reporter_uuid=test_user.uuid,
    )
    report2 = await create_test_report(
        db_session,
        project_id=test_project_alt.project_id,
        reporter_uuid=test_user.uuid,
    )
    form_template = await create_test_form_template(db_session)

    await create_completed_form(
        db_session,
        sample_completed_form_payload(
            report_id=report1.report_id,
            form_template_id=form_template.form_template_id,
        ),
    )
    await create_completed_form(
        db_session,
        sample_completed_form_payload(
            report_id=report2.report_id,
            form_template_id=form_template.form_template_id,
        ),
    )

    items = await list_completed_forms(db_session, report_id=report1.report_id)

    assert len(items) == 1
    assert items[0].report_id == report1.report_id


# ----------------------------
# Update
# ----------------------------

@pytest.mark.asyncio
async def test_update_completed_form_partial(db_session, test_project, test_user):
    report = await create_test_report(
        db_session,
        project_id=test_project.project_id,
        reporter_uuid=test_user.uuid,
    )
    form_template = await create_test_form_template(db_session)

    obj = await create_completed_form(
        db_session,
        sample_completed_form_payload(
            report_id=report.report_id,
            form_template_id=form_template.form_template_id,
        ),
    )

    payload = CompletedFormUpdate(form_data=json.dumps({"field1": "updated"}))


    updated = await update_completed_form(db_session, obj.id, payload)

    assert updated is not None
    assert json.loads(updated.form_data) == {"field1": "updated"}
    assert updated.report_id == obj.report_id


@pytest.mark.asyncio
async def test_update_completed_form_not_found(db_session):
    payload = CompletedFormUpdate(response_json={"x": 1})

    updated = await update_completed_form(db_session, uuid4(), payload)

    assert updated is None


# ----------------------------
# Delete
# ----------------------------

@pytest.mark.asyncio
async def test_delete_completed_form(db_session, test_project, test_user):
    report = await create_test_report(
        db_session,
        project_id=test_project.project_id,
        reporter_uuid=test_user.uuid,
    )
    form_template = await create_test_form_template(db_session)

    obj = await create_completed_form(
        db_session,
        sample_completed_form_payload(
            report_id=report.report_id,
            form_template_id=form_template.form_template_id,
        ),
    )

    ok = await delete_completed_form(db_session, obj.id)

    assert ok is True
    assert await get_completed_form(db_session, obj.id) is None


@pytest.mark.asyncio
async def test_delete_completed_form_not_found(db_session):
    ok = await delete_completed_form(db_session, uuid4())
    assert ok is False
