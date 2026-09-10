import uuid
from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class ComplianceCheck(Base):
    __tablename__ = "compliance_checks"
    
    compliance_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.project_id"), nullable=False, index=True)
    regulation_name: Mapped[str] = mapped_column(String(255), nullable=False)
    regulation_category: Mapped[str] = mapped_column(String(100), nullable=False)
    compliance_status: Mapped[str] = mapped_column(String(50), default="pending")
    checked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    inspector_notes: Mapped[str] = mapped_column(Text, nullable=True)
    severity: Mapped[int] = mapped_column(Integer, default=1)
    next_inspection_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    documentation_url: Mapped[str] = mapped_column(String(500), nullable=True)
    
    project: Mapped["Project"] = relationship(back_populates="compliance_checks")
