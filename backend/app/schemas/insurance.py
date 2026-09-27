import uuid
from datetime import datetime
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

class InsuranceCaseBase(BaseModel):
    claim_type: str = Field(min_length=1, max_length=100)
    risk_score: float = Field(ge=0, le=100)
    risk_level: str = Field(pattern="^(Low|Medium|High|Critical)$")
    status: str = Field(default="open", pattern="^(open|closed|under_review|disputed)$")
    estimated_liability: Optional[Decimal] = Field(default=None, ge=0)
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
