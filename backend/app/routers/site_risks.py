from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import SiteRisk, Project
from app.schemas import SiteRiskCreate, SiteRiskResponse, SiteRiskListResponse, APIResponse

router = APIRouter()

@router.get("/projects/{project_id}/site-risks", response_model=APIResponse)
async def list_site_risks(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SiteRisk).where(SiteRisk.project_id == project_id).order_by(SiteRisk.detected_at.desc())
    )
    risks = result.scalars().all()
    return APIResponse(data=SiteRiskListResponse(
        risks=[SiteRiskResponse.model_validate(r) for r in risks], total=len(risks)
    ))

@router.post("/projects/{project_id}/site-risks", response_model=APIResponse)
async def create_site_risk(project_id: UUID, risk: SiteRiskCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Project).where(Project.project_id == project_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Project not found")
    db_risk = SiteRisk(**risk.model_dump(), project_id=project_id)
    db.add(db_risk)
    await db.commit()
    await db.refresh(db_risk)
    return APIResponse(data=SiteRiskResponse.model_validate(db_risk))

@router.get("/projects/{project_id}/site-risks/distribution", response_model=APIResponse)
async def get_risk_distribution(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SiteRisk.risk_type, func.count(SiteRisk.risk_id))
        .where(SiteRisk.project_id == project_id)
        .group_by(SiteRisk.risk_type)
    )
    rows = result.all()
    total = sum(count for _, count in rows) or 1
    colors = {"fall_hazard": "#ef4444", "equipment_risk": "#f97316", "electrical_hazard": "#3b82f6", "environmental_risk": "#6b7280", "structural_risk": "#8b5cf6"}
    distribution = [{"risk_type": rt.replace("_", " ").title(), "count": c, "percentage": round((c/total)*100, 1), "color": colors.get(rt, "#6b7280")} for rt, c in rows]
    return APIResponse(data=distribution)

@router.get("/projects/{project_id}/site-risks/heatmap", response_model=APIResponse)
async def get_risk_heatmap(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(SiteRisk.probability, SiteRisk.impact, func.count(SiteRisk.risk_id))
        .where(SiteRisk.project_id == project_id)
        .group_by(SiteRisk.probability, SiteRisk.impact)
    )
    rows = result.all()
    def rl(s):
        if s <= 4: return "Low"
        elif s <= 6: return "Low-Medium"
        elif s <= 9: return "Medium"
        elif s <= 12: return "Medium-High"
        elif s <= 16: return "High"
        elif s <= 20: return "Critical"
        else: return "Extreme"
    inherent = [{"probability": p, "impact": i, "count": c, "risk_level": rl(p*i)} for p, i, c in rows]
    residual = [{"probability": max(1,p-1), "impact": max(1,i-1), "count": max(0,c-1), "risk_level": rl(max(1,p-1)*max(1,i-1))} for p, i, c in rows]
    return APIResponse(data={"inherent": inherent, "residual": residual})

@router.get("/projects/{project_id}/site-risks/score", response_model=APIResponse)
async def get_site_risk_score(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SiteRisk).where(SiteRisk.project_id == project_id))
    risks = result.scalars().all()
    if not risks:
        return APIResponse(data={"score": 100.0, "active_risks": 0, "high_risk_zones": 0, "hazards_detected": 0})
    total_weighted = sum(r.probability * r.impact * 4 * r.ai_confidence for r in risks)
    score = max(0, round(100 - total_weighted / len(risks), 1))
    high_risk = len([r for r in risks if r.probability >= 4 and r.impact >= 4])
    hazards = len([r for r in risks if r.mitigation_status == "open"])
    return APIResponse(data={"score": score, "active_risks": len(risks), "high_risk_zones": high_risk, "hazards_detected": hazards})
