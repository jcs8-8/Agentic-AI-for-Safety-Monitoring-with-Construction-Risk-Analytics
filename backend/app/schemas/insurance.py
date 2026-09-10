import uuid
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class InsuranceCaseBase(BaseModel):
    claim_type: str
    risk_score: float
    risk_level: str
    status: str = "open"
    estimated_liability: Optional[Decimal] = None
    incident_date: datetime
    description: Optional[str] = None
    ai_recommendation: Optional[str] = None

class InsuranceCaseCreate(InsuranceCaseBase):
    project_id: uuid.UUID

class InsuranceCaseResponse(InsuranceCaseBase):
    model_config = ConfigDict(from_attributes=True)
    case_id: uuid.UUID
    project_id: uuid.UUID

class InsuranceDashboardData(BaseModel):
    project_id: uuid.UUID
    project_name: str
    insurance_risk_score: str
    total_exposure: float
    open_cases: int
    claim_analysis: List[dict]
    features: List[str]
