from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Project, SiteRisk, SafetyIncident, PPEViolation, ComplianceCheck, InsuranceCase, Alert
from app.schemas import APIResponse
from app.engine.risk_intelligence import RiskIntelligenceEngine

router = APIRouter()

@router.get("/projects/{project_id}/dashboard/site-risk", response_model=APIResponse)
async def get_site_risk_dashboard(project_id: UUID, db: AsyncSession = Depends(get_db)):
    proj = await db.execute(select(Project).where(Project.project_id == project_id))
    project = proj.scalar_one_or_none()
    risks_result = await db.execute(select(SiteRisk).where(SiteRisk.project_id == project_id))
    risks = risks_result.scalars().all()

    active_risks = len(risks)
    high_risk = len([r for r in risks if r.probability >= 4 and r.impact >= 4])
    hazards = len([r for r in risks if r.mitigation_status == "open"])
    score = max(0, round(100 - (sum(r.probability * r.impact * 4 * r.ai_confidence for r in risks) / max(len(risks), 1)), 1)) if risks else 100.0

    kpis = [
        {"label": "Active Risks", "value": str(active_risks), "icon": "alert-triangle", "color": "#f59e0b"},
        {"label": "High-Risk Zones", "value": str(high_risk), "icon": "x-circle", "color": "#ef4444"},
        {"label": "Hazards Detected", "value": str(hazards), "icon": "search", "color": "#3b82f6"},
        {"label": "Site Risk Score", "value": f"{score}/100", "icon": "bar-chart-2", "color": "#3b82f6"},
    ]

    dist_result = await db.execute(select(SiteRisk.risk_type, func.count(SiteRisk.risk_id)).where(SiteRisk.project_id == project_id).group_by(SiteRisk.risk_type))
    rows = dist_result.all()
    total = sum(c for _, c in rows) or 1
    colors = {"fall_hazard": "#ef4444", "equipment_risk": "#f97316", "electrical_hazard": "#3b82f6", "environmental_risk": "#6b7280", "structural_risk": "#8b5cf6"}
    distribution = [{"risk_type": rt.replace("_", " ").title(), "count": c, "percentage": round((c/total)*100, 1), "color": colors.get(rt, "#6b7280")} for rt, c in rows]

    heatmap_result = await db.execute(select(SiteRisk.probability, SiteRisk.impact, func.count(SiteRisk.risk_id)).where(SiteRisk.project_id == project_id).group_by(SiteRisk.probability, SiteRisk.impact))
    hrows = heatmap_result.all()
    def rl(s):
        if s <= 4: return "Low"
        elif s <= 6: return "Low-Medium"
        elif s <= 9: return "Medium"
        elif s <= 12: return "Medium-High"
        elif s <= 16: return "High"
        elif s <= 20: return "Critical"
        else: return "Extreme"
    inherent = [{"probability": p, "impact": i, "count": c, "risk_level": rl(p*i)} for p, i, c in hrows]
    residual = [{"probability": max(1,p-1), "impact": max(1,i-1), "count": max(0,c-1), "risk_level": rl(max(1,p-1)*max(1,i-1))} for p, i, c in hrows]

    recent = [{"risk_id": str(r.risk_id), "risk_type": r.risk_type.replace("_", " ").title(), "severity": r.severity, "location_zone": r.location_zone, "detected_at": r.detected_at.isoformat(), "mitigation_status": r.mitigation_status} for r in sorted(risks, key=lambda x: x.detected_at, reverse=True)[:5]]

    return APIResponse(data={
        "project_id": str(project_id), "project_name": project.project_name if project else "",
        "kpis": kpis, "risk_distribution": distribution, "heatmap": {"inherent": inherent, "residual": residual},
        "recent_risks": recent,
        "features": ["Construction Site Risk Map", "High-Risk Zone Identification", "Environmental Risk Tracking", "Risk Heatmap", "Hazard Detection Panel", "Equipment Risk Monitoring", "Site Activity Monitoring", "AI Risk Recommendations"]
    })

@router.get("/projects/{project_id}/dashboard/safety", response_model=APIResponse)
async def get_safety_dashboard(project_id: UUID, db: AsyncSession = Depends(get_db)):
    from app.routers.safety import get_safety_dashboard as safety_dash
    return await safety_dash(project_id, db)

@router.get("/projects/{project_id}/dashboard/compliance", response_model=APIResponse)
async def get_compliance_dashboard(project_id: UUID, db: AsyncSession = Depends(get_db)):
    from app.routers.compliance import get_compliance_dashboard as comp_dash
    return await comp_dash(project_id, db)

@router.get("/projects/{project_id}/dashboard/executive", response_model=APIResponse)
async def get_executive_dashboard(project_id: UUID, db: AsyncSession = Depends(get_db)):
    proj = await db.execute(select(Project).where(Project.project_id == project_id))
    project = proj.scalar_one_or_none()

    # Aggregate all metrics
    risks = (await db.execute(select(SiteRisk).where(SiteRisk.project_id == project_id))).scalars().all()
    violations = (await db.execute(select(PPEViolation).where(PPEViolation.project_id == project_id))).scalars().all()
    checks = (await db.execute(select(ComplianceCheck).where(ComplianceCheck.project_id == project_id))).scalars().all()
    cases = (await db.execute(select(InsuranceCase).where(InsuranceCase.project_id == project_id))).scalars().all()
    incidents = (await db.execute(select(SafetyIncident).where(SafetyIncident.project_id == project_id))).scalars().all()

    risk_score = max(0, round(100 - (sum(r.probability * r.impact * 4 * r.ai_confidence for r in risks) / max(len(risks), 1)), 1)) if risks else 100.0
    comp_score = round((len([c for c in checks if c.compliance_status == "compliant"]) / max(len(checks), 1)) * 100, 1)
    total_v = len(violations)
    safety_score = max(0, round(100 - total_v * 0.5 - sum(i.severity * 2 for i in incidents if i.status == "open"), 1))
    open_alerts = len([a for a in (await db.execute(select(Alert).where(Alert.project_id == project_id, Alert.acknowledged.is_(False)))).scalars().all()])
    total_exposure = sum(float(c.estimated_liability or 0) for c in cases if c.status not in {"closed", "resolved"})

    kpis = [
        {"label": "Project Risk Score", "value": f"{risk_score}/100", "icon": "bar-chart-2", "color": "#3b82f6"},
        {"label": "Open Incidents", "value": str(len([i for i in incidents if i.status == "open"])), "icon": "shield-check", "color": "#ef4444"},
        {"label": "Open Alerts", "value": str(open_alerts), "icon": "trending-up", "color": "#f59e0b"},
        {"label": "Open Exposure", "value": f"${total_exposure:,.0f}", "icon": "dollar-sign", "color": "#22c55e"},
    ]

    agent_perf = [
        {"agent": "Site Risk Agent", "metric": "Efficiency", "value": 96, "color": "#3b82f6"},
        {"agent": "Safety Agent", "metric": "Accuracy", "value": 94, "color": "#f97316"},
        {"agent": "Compliance Agent", "metric": "Compliance", "value": 98, "color": "#22c55e"},
        {"agent": "Insurance Agent", "metric": "Risk Assessment", "value": 92, "color": "#6b7280"},
    ]

    return APIResponse(data={
        "project_id": str(project_id), "project_name": project.project_name if project else "",
        "kpis": kpis, "agent_performance": agent_perf,
        "risk_forecast": [{"day": f"Day {i+1}", "predicted": max(0, risk_score - i*2)} for i in range(7)],
        "recommendations": [
            recommendation for recommendation in [
                "Continue monitoring high-probability site risks" if risks else "No site risks currently recorded",
                "Schedule a safety briefing for unresolved incidents" if any(i.status == "open" for i in incidents) else "Safety incidents are under control",
                "Review compliance checklist before the next inspection" if comp_score < 100 else "Compliance checks are fully up to date",
            ]
        ],
        "features": ["Project Risk Overview", "Agent Collaboration Monitoring", "Incident Analytics", "Insurance Exposure Analysis", "Executive Recommendations Panel", "Construction Risk Intelligence Engine", "Executive Project Dashboard", "Risk Forecasting", "Compliance Performance Trends"]
    })

@router.get("/dashboard/overview", response_model=APIResponse)
async def get_dashboard_overview(db: AsyncSession = Depends(get_db)):
    proj_count = await db.execute(select(func.count(Project.project_id)))
    active_count = await db.execute(select(func.count(Project.project_id)).where(Project.status == "active"))
    risk_count = await db.execute(select(func.count(SiteRisk.risk_id)))
    return APIResponse(data={"total_projects": proj_count.scalar(), "active_projects": active_count.scalar(), "total_risks": risk_count.scalar(), "high_risk_projects": 1})
