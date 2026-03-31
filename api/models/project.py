# app/models/project.py

import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    project_id = Column(
        String,
        primary_key=True,
        default=lambda: f"P{uuid.uuid4().hex[:8]}",
        nullable=False,
    )

    project_name = Column(Text, nullable=False)
    project_description = Column(Text)
    registration_code = Column(String, unique=True, nullable=False)
    borough = Column(Text)
    status = Column(Text, nullable=False)

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

    # relationships
    project_assignments = relationship(
        "ProjectUser",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    client_links = relationship(
        "ProjectClient",
        back_populates="project",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    reports = relationship(
        "Report",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="selectin",
)