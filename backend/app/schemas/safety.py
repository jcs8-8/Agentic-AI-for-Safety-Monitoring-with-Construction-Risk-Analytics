import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class SafetyIncidentBase(BaseModel):
    incident_type: str
    severity: int
    incident_date: datetime
    worker_id: Optional[str] = None
    worker_name: Optional[str] = None
    description: str
    location_zone: Optional[str] = None
    ppe_involved: bool = False
    root_cause: Optional[str] = None
    corrective_action: Optional[str] = None
    status: str = "open"

class SafetyIncidentCreate(SafetyIncidentBase):
    project_id: uuid.UUID

class SafetyIncidentResponse(SafetyIncidentBase):
    model_config = ConfigDict(from_attributes=True)
    incident_id: uuid.UUID
    project_id: uuid.UUID

class PPEViolationBase(BaseModel):
    worker_id: str
    worker_name: Optional[str] = None
    violation_type: str
    image_evidence: Optional[str] = None
    ai_confidence: float = 0.90
    location_zone: Optional[str] = None
    resolved: bool = False

class PPEViolationCreate(PPEViolationBase):
    project_id: uuid.UUID

class PPEViolationResponse(PPEViolationBase):
    model_config = ConfigDict(from_attributes=True)
    violation_id: uuid.UUID
    project_id: uuid.UUID
    timestamp: datetime
    resolved_at: Optional[datetime] = None

class SafetyDashboardData(BaseModel):
    project_id: uuid.UUID
    project_name: str
    ppe_compliance_rate: float
    safety_violations: int
    workers_monitored: int
    safety_score: float
    ppe_by_type: List[dict]
    recent_incidents: List[dict]
    features: List[str]
