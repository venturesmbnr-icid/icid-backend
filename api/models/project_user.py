# app/models/project_user.py

from sqlalchemy import Column, Text, TIMESTAMP, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime, timezone


class ProjectUser(Base):
    __tablename__ = "project_users"

    project_id = Column(
        Text,
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        primary_key=True,
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        primary_key=True,
    )

    user_role = Column(Text)

    assigned_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    project = relationship(
        "Project",
        back_populates="project_assignments",
    )

    user = relationship(
        "User",
        back_populates="project_assignments",
    )

