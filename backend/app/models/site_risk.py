import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Float, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class SiteRisk(Base):
    __tablename__ = "site_risks"
    
    risk_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.project_id"), nullable=False, index=True)
    risk_type: Mapped[str] = mapped_column(String(100), nullable=False)
    severity: Mapped[int] = mapped_column(Integer, nullable=False)
    probability: Mapped[int] = mapped_column(Integer, nullable=False)
    impact: Mapped[int] = mapped_column(Integer, nullable=False)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    location_zone: Mapped[str] = mapped_column(String(100), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    mitigation_status: Mapped[str] = mapped_column(String(50), default="open")
    ai_confidence: Mapped[float] = mapped_column(Float, default=0.85)
    image_evidence: Mapped[str] = mapped_column(String(500), nullable=True)
    
    project: Mapped["Project"] = relationship(back_populates="site_risks")
