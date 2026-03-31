# app/models/user.py

import uuid
from sqlalchemy import Column, Text, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(Text, nullable=False)
    first_name = Column(Text)
    last_name = Column(Text)
    phone_number = Column(Text)

    client_id = Column(
        Text,
        ForeignKey("clients.client_id", ondelete="CASCADE"),
        nullable=False,
    )


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
    client = relationship("Client", back_populates="users")

    project_assignments = relationship(
        "ProjectUser",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    reports = relationship("Report", back_populates="reporter")


