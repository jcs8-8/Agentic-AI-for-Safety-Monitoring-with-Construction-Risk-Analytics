import uuid
from datetime import datetime
from typing import List
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class Project(Base):
    __tablename__ = "projects"
    
    project_id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    project_name: Mapped[str] = mapped_column(String(255), nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="active")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    
    site_risks: Mapped[List["SiteRisk"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="selectin")
    safety_incidents: Mapped[List["SafetyIncident"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="selectin")
    ppe_violations: Mapped[List["PPEViolation"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="selectin")
    compliance_checks: Mapped[List["ComplianceCheck"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="selectin")
    insurance_cases: Mapped[List["InsuranceCase"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="selectin")
    reports: Mapped[List["Report"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="selectin")
    alerts: Mapped[List["Alert"]] = relationship(back_populates="project", cascade="all, delete-orphan", lazy="selectin")
