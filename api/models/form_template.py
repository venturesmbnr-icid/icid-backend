# app/models/form_template.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, Text, TIMESTAMP, UUID
from app.db.base import Base


class FormTemplate(Base):
    __tablename__ = "form_templates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    form_template_id = Column(Text, unique=True, nullable=False)

    form_name = Column(Text, nullable=False)
    form_description = Column(Text)
    form_status = Column(Text)
    mandatory_forms = Column(Text)
    optional_forms = Column(Text)

    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
