# tests/models/test_completed_form.py
import pytest
from sqlalchemy.exc import IntegrityError

from app.models.completed_form import CompletedForm
from app.models.report import Report
from app.models.form_template import FormTemplate
from app.models.user import User
from app.models.client import Client
from app.models.project import Project


def make_client_user(idx: int):
    client = Client(
        client_id=f"C{900 + idx}",
        client_username=f"client{idx}",
        client_name=f"Client {idx}",
    )

    user = User(
        email=f"user{idx}@example.com",
        first_name="User",
        last_name=str(idx),
        client=client,
    )
    return client, user


@pytest.mark.asyncio
async def test_create_completed_form_success(db_session):
    client, user = make_client_user(1)

    project = Project(
        project_id="P900",
        project_name="CompletedForm Project",
        registration_code="CF-001",
        status="ACTIVE",
    )

    report = Report(
        report_id="R900",
        reporter=user,
        project=project,
    )

    template = FormTemplate(
        form_template_id="TMP-900",
        form_name="Safety Checklist",
    )

    completed_form = CompletedForm(
        completed_form_id="CFORM-001",
        report=report,
        template_id=template.form_template_id,
        form_data='{"q1": "yes"}',
    )

    db_session.add_all([client, user, project, report, template, completed_form])
    await db_session.flush()

    assert completed_form.id is not None
    assert completed_form.created_at is not None
    assert completed_form.updated_at is not None


@pytest.mark.asyncio
async def test_completed_form_requires_completed_form_id(db_session):
    client, user = make_client_user(2)

    template = FormTemplate(
        form_template_id="TMP-901",
        form_name="Checklist",
    )

    project = Project(
        project_id="P901",
        project_name="Proj",
        registration_code="CF-002",
        status="ACTIVE",
    )

    report = Report(
        report_id="R901",
        reporter=user,
        project=project,
    )

    completed_form = CompletedForm(
        report=report,
        template_id=template.form_template_id,
        form_data="{}",
    )

    db_session.add_all([client, user, template, project, report, completed_form])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_completed_form_requires_report(db_session):
    template = FormTemplate(
        form_template_id="TMP-902",
        form_name="Checklist",
    )

    completed_form = CompletedForm(
        completed_form_id="CFORM-002",
        template_id=template.form_template_id,
        form_data="{}",
    )

    db_session.add_all([template, completed_form])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_completed_form_requires_template(db_session):
    client, user = make_client_user(3)

    project = Project(
        project_id="P903",
        project_name="Proj",
        registration_code="CF-003",
        status="ACTIVE",
    )

    report = Report(
        report_id="R903",
        reporter=user,
        project=project,
    )

    completed_form = CompletedForm(
        completed_form_id="CFORM-003",
        report=report,
        form_data="{}",
    )

    db_session.add_all([client, user, project, report, completed_form])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_completed_form_form_data_is_optional(db_session):
    client, user = make_client_user(4)

    template = FormTemplate(
        form_template_id="TMP-904",
        form_name="Checklist",
    )

    project = Project(
        project_id="P904",
        project_name="Proj",
        registration_code="CF-004",
        status="ACTIVE",
    )

    report = Report(
        report_id="R904",
        reporter=user,
        project=project,
    )

    completed_form = CompletedForm(
        completed_form_id="CFORM-004",
        report=report,
        template_id=template.form_template_id,
    )

    db_session.add_all([client, user, template, project, report, completed_form])
    await db_session.flush()

    assert completed_form.form_data is None



@pytest.mark.asyncio
async def test_completed_form_id_must_be_unique(db_session):
    client, user = make_client_user(5)

    template = FormTemplate(
        form_template_id="TMP-905",
        form_name="Checklist",
    )

    project = Project(
        project_id="P905",
        project_name="Proj",
        registration_code="CF-005",
        status="ACTIVE",
    )

    report = Report(
        report_id="R905",
        reporter=user,
        project=project,
    )

    cf1 = CompletedForm(
        completed_form_id="CFORM-DUP",
        report=report,
        template_id=template.form_template_id,
        form_data="{}",
    )

    cf2 = CompletedForm(
        completed_form_id="CFORM-DUP",
        report=report,
        template_id=template.form_template_id,
        form_data="{}",
    )

    db_session.add_all([client, user, template, project, report, cf1, cf2])

    with pytest.raises(IntegrityError):
        await db_session.flush()


@pytest.mark.asyncio
async def test_report_delete_cascades_completed_forms(db_session):
    client, user = make_client_user(6)

    template = FormTemplate(
        form_template_id="TMP-906",
        form_name="Checklist",
    )

    project = Project(
        project_id="P906",
        project_name="Proj",
        registration_code="CF-006",
        status="ACTIVE",
    )

    report = Report(
        report_id="R906",
        reporter=user,
        project=project,
    )

    completed_form = CompletedForm(
        completed_form_id="CFORM-906",
        report=report,
        template_id=template.form_template_id,
        form_data="{}",
    )

    db_session.add_all([client, user, template, project, report, completed_form])
    await db_session.flush()

    await db_session.delete(report)
    await db_session.flush()

    result = await db_session.get(CompletedForm, completed_form.id)
    assert result is None
