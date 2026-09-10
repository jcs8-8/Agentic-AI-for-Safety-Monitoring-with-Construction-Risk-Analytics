import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Float, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class PPEViolation(Base):
    __tablename__ = "ppe_violations"
    
    violation_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.project_id"), nullable=False, index=True)
    worker_id: Mapped[str] = mapped_column(String(100), nullable=False)
    worker_name: Mapped[str] = mapped_column(String(255), nullable=True)
    violation_type: Mapped[str] = mapped_column(String(100), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    image_evidence: Mapped[str] = mapped_column(String(500), nullable=True)
    ai_confidence: Mapped[float] = mapped_column(Float, default=0.90)
    location_zone: Mapped[str] = mapped_column(String(100), nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    resolved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    project: Mapped["Project"] = relationship(back_populates="ppe_violations")
