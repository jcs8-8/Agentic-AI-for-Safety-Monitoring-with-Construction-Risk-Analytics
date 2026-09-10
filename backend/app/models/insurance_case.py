import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Float, DateTime, ForeignKey, Text, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class InsuranceCase(Base):
    __tablename__ = "insurance_cases"
    
    case_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.project_id"), nullable=False, index=True)
    claim_type: Mapped[str] = mapped_column(String(100), nullable=False)
    risk_score: Mapped[float] = mapped_column(Float, nullable=False)
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="open")
    estimated_liability: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=True)
    incident_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    ai_recommendation: Mapped[str] = mapped_column(Text, nullable=True)
    
    project: Mapped["Project"] = relationship(back_populates="insurance_cases")
