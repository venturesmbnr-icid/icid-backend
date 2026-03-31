# app/models/project_client.py

from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ProjectClient(Base):
    __tablename__ = "project_clients"

    project_id = Column(
        Text,
        ForeignKey("projects.project_id", ondelete="CASCADE"),
        primary_key=True,
    )

    client_id = Column(
        Text,
        ForeignKey("clients.client_id", ondelete="CASCADE"),
        primary_key=True,
    )

    client_role = Column(Text)

    project = relationship(
        "Project",
        back_populates="client_links",
        passive_deletes=True,
    )

    client = relationship(
        "Client",
        back_populates="project_links",
        passive_deletes=True,
    )


