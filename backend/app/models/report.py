import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Report(Base):
    __tablename__ = "reports"
    
    report_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.project_id"), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(100), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    file_format: Mapped[str] = mapped_column(String(20), default="pdf")
    content_summary: Mapped[str] = mapped_column(Text, nullable=True)
    generated_by: Mapped[str] = mapped_column(String(100), default="Reporting Agent")
    
    project: Mapped["Project"] = relationship(back_populates="reports")
