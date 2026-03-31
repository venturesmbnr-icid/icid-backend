# app/models/client.py
import uuid
from sqlalchemy import Column, Text, TIMESTAMP, String
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.base import Base

class Client(Base):
    """Client model"""
    __tablename__ = "clients"

    client_id = Column(
        String, 
        primary_key=True,    
        default=lambda: f"C{uuid.uuid4().hex[:8]}",
        nullable=False
    )
    client_username = Column(Text, nullable=False)
    client_name = Column(Text, nullable=False)
    client_email = Column(Text)
    client_phone = Column(Text)
    client_role = Column(Text)

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


    users = relationship(
        "User",
        back_populates="client",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    project_links = relationship(
        "ProjectClient",
        back_populates="client",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
