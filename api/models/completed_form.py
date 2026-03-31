# app/models/completed_form.py

import uuid
from sqlalchemy import Column, Text, TIMESTAMP, UUID, ForeignKey, text
from sqlalchemy.orm import relationship

from app.db.base import Base


class CompletedForm(Base):
    __tablename__ = "completed_forms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    completed_form_id = Column(Text, unique=True, nullable=False)

    report_id = Column(
        Text,
        ForeignKey("reports.report_id", ondelete="CASCADE"),
        nullable=False,
    )

    template_id = Column(
        Text,
        ForeignKey("form_templates.form_template_id", ondelete="CASCADE"),
        nullable=False,
    )

    form_data = Column(Text)

    # ✅ FIX
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    report = relationship(
        "Report",
        back_populates="completed_forms",
    )

    form_template = relationship(
        "FormTemplate",
        primaryjoin="CompletedForm.template_id == FormTemplate.form_template_id",
    )
