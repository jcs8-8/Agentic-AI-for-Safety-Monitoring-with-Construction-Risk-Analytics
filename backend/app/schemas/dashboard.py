import uuid
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class KPIData(BaseModel):
    label: str
    value: str
    icon: str
    color: str
    trend: Optional[str] = None
    trend_direction: Optional[str] = None

class SiteRiskDashboardData(BaseModel):
    project_id: uuid.UUID
    project_name: str
    kpis: List[KPIData]
    risk_distribution: List[Dict[str, Any]]
    heatmap: Dict[str, Any]
    recent_risks: List[Dict[str, Any]]
    features: List[str]

class SafetyDashboardData(BaseModel):
    project_id: uuid.UUID
    project_name: str
    kpis: List[KPIData]
    ppe_compliance_rate: float
    safety_violations: int
    workers_monitored: int
    safety_score: float
    ppe_by_type: List[Dict[str, Any]]
    recent_incidents: List[Dict[str, Any]]
    features: List[str]

class ComplianceInsuranceDashboardData(BaseModel):
    project_id: uuid.UUID
    project_name: str
    compliance_kpis: List[KPIData]
    insurance_kpis: List[KPIData]
    compliance_by_category: List[Dict[str, Any]]
    features: List[str]

class ExecutiveDashboardData(BaseModel):
    project_id: uuid.UUID
    project_name: str
    kpis: List[KPIData]
    agent_performance: List[Dict[str, Any]]
    risk_forecast: List[Dict[str, Any]]
    recommendations: List[str]
    features: List[str]

class DashboardOverview(BaseModel):
    total_projects: int
    active_projects: int
    total_risks: int
    high_risk_projects: int
