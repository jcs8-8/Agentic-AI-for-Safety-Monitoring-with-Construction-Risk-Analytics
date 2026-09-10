import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class SiteRiskBase(BaseModel):
    risk_type: str
    severity: int
    probability: int
    impact: int
    location_zone: Optional[str] = None
    description: Optional[str] = None
    mitigation_status: str = "open"
    ai_confidence: float = 0.85

class SiteRiskCreate(SiteRiskBase):
    project_id: uuid.UUID

class SiteRiskResponse(SiteRiskBase):
    model_config = ConfigDict(from_attributes=True)
    risk_id: uuid.UUID
    project_id: uuid.UUID
    detected_at: datetime
    image_evidence: Optional[str] = None

class SiteRiskListResponse(BaseModel):
    risks: List[SiteRiskResponse]
    total: int

class RiskDistributionItem(BaseModel):
    risk_type: str
    count: int
    percentage: float
    color: str

class RiskHeatmapCell(BaseModel):
    probability: int
    impact: int
    count: int
    risk_level: str

class RiskHeatmapData(BaseModel):
    inherent: List[RiskHeatmapCell]
    residual: List[RiskHeatmapCell]
