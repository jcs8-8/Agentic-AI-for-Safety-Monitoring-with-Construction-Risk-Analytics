import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class SafetyIncident(Base):
    __tablename__ = "safety_incidents"
    
    incident_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.project_id"), nullable=False, index=True)
    incident_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[int] = mapped_column(Integer, nullable=False)
    incident_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    worker_id: Mapped[str] = mapped_column(String(100), nullable=True)
    worker_name: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    location_zone: Mapped[str] = mapped_column(String(100), nullable=True)
    ppe_involved: Mapped[bool] = mapped_column(Boolean, default=False)
    root_cause: Mapped[str] = mapped_column(Text, nullable=True)
    corrective_action: Mapped[str] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="open")
    
    project: Mapped["Project"] = relationship(back_populates="safety_incidents")
