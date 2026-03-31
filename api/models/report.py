# app/models/report.py

from sqlalchemy import Column, Text, TIMESTAMP, DATE, ForeignKey, UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Text, primary_key=True)

    reporter_uuid = Column(
        UUID(as_uuid=True),
        ForeignKey("users.uuid", ondelete="CASCADE"),
        nullable=False,
    )

    project_id = Column(
        Text,
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        nullable=False,
    )

    report_date = Column(DATE)

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
    reporter = relationship("User", back_populates="reports")
    project = relationship("Project", back_populates="reports")
    completed_forms = relationship(
        "CompletedForm",
        back_populates="report",
        cascade="all, delete-orphan",
    )
