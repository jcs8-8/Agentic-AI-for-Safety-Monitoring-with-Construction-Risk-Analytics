import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ComplianceCheckBase(BaseModel):
    regulation_name: str
    regulation_category: str
    compliance_status: str = "pending"
    inspector_notes: Optional[str] = None
    severity: int = 1
    next_inspection_date: Optional[datetime] = None
    documentation_url: Optional[str] = None

class ComplianceCheckCreate(ComplianceCheckBase):
    project_id: uuid.UUID

class ComplianceCheckResponse(ComplianceCheckBase):
    model_config = ConfigDict(from_attributes=True)
    compliance_id: uuid.UUID
    project_id: uuid.UUID
    checked_at: datetime

class ComplianceDashboardData(BaseModel):
    project_id: uuid.UUID
    project_name: str
    compliance_score: float
    open_violations: int
    audit_readiness: float
    compliance_by_category: List[dict]
    insurance_risk_score: str
    features: List[str]
