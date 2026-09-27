from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import InsuranceCase, Project
from app.schemas import APIResponse
from app.schemas.insurance import InsuranceCaseBase

router = APIRouter()

class InsuranceStatusUpdate(BaseModel):
    status: str

def risk_level_for_score(score: float) -> str:
    if score < 30:
        return "Low"
    if score < 60:
        return "Medium"
    if score < 80:
        return "High"
    return "Critical"

@router.post("/projects/{project_id}/insurance", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_insurance_case(project_id: UUID, payload: InsuranceCaseBase, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    case = InsuranceCase(project_id=project_id, **payload.model_dump(exclude={"project_id"}))
    db.add(case)
    await db.flush()
    return APIResponse(data={"id": str(case.case_id), "project_id": str(project_id), "status": case.status})

@router.get("/projects/{project_id}/insurance", response_model=APIResponse)
async def list_insurance(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InsuranceCase).where(InsuranceCase.project_id == project_id))
    return APIResponse(data=[{"id": str(c.case_id), "type": c.claim_type, "risk_level": c.risk_level, "status": c.status} for c in result.scalars().all()])

@router.get("/projects/{project_id}/insurance/score", response_model=APIResponse)
async def get_insurance_score(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InsuranceCase).where(InsuranceCase.project_id == project_id))
    cases = result.scalars().all()
    score = sum(case.risk_score for case in cases) / len(cases) if cases else 0
    level = risk_level_for_score(score)
    return APIResponse(data={"insurance_risk_score": round(score, 1), "risk_level": level, "open_cases": sum(case.status == "open" for case in cases)})

@router.get("/projects/{project_id}/insurance/exposure", response_model=APIResponse)
async def get_insurance_exposure(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InsuranceCase).where(InsuranceCase.project_id == project_id))
    cases = result.scalars().all()
    total = sum(float(case.estimated_liability or 0) for case in cases)
    by_type = {}
    for case in cases:
        by_type[case.claim_type] = by_type.get(case.claim_type, 0) + float(case.estimated_liability or 0)
    return APIResponse(data={"total_exposure": total, "open_exposure": sum(float(case.estimated_liability or 0) for case in cases if case.status == "open"), "by_claim_type": by_type, "cost_savings_estimate": round(total * 0.15, 2)})

@router.put("/insurance/{case_id}/status", response_model=APIResponse)
async def update_insurance_status(case_id: UUID, update: InsuranceStatusUpdate, db: AsyncSession = Depends(get_db)):
    if update.status not in {"open", "closed", "under_review", "disputed"}:
        raise HTTPException(status_code=422, detail="Invalid insurance case status")
    result = await db.execute(select(InsuranceCase).where(InsuranceCase.case_id == case_id))
    case = result.scalar_one_or_none()
    if case is None:
        return APIResponse(data=None, message="Insurance case not found")
    case.status = update.status
    return APIResponse(data={"id": str(case.case_id), "status": case.status})

@router.get("/projects/{project_id}/insurance/dashboard", response_model=APIResponse)
async def get_insurance_dashboard(project_id: UUID, db: AsyncSession = Depends(get_db)):
    proj = await db.execute(select(Project).where(Project.project_id == project_id))
    project = proj.scalar_one_or_none()
    cases_result = await db.execute(select(InsuranceCase).where(InsuranceCase.project_id == project_id))
    cases = cases_result.scalars().all()

    total_exposure = sum(float(c.estimated_liability or 0) for c in cases)
    open_cases = len([c for c in cases if c.status == "open"])
    avg_risk = sum(c.risk_score for c in cases) / len(cases) if cases else 50
    risk_level = risk_level_for_score(avg_risk)

    claim_types = {}
    for c in cases:
        ct = c.claim_type
        if ct not in claim_types:
            claim_types[ct] = {"count": 0, "total_risk": 0}
        claim_types[ct]["count"] += 1
        claim_types[ct]["total_risk"] += c.risk_score

    analysis = [{"type": k.replace("_", " ").title(), "count": v["count"], "avg_risk": round(v["total_risk"]/v["count"], 1)} for k, v in claim_types.items()]

    return APIResponse(data={
        "project_id": str(project_id), "project_name": project.project_name if project else "",
        "insurance_risk_score": risk_level, "average_risk_score": round(avg_risk, 1),
        "total_exposure": total_exposure,
        "open_exposure": sum(float(c.estimated_liability or 0) for c in cases if c.status == "open"),
        "cost_savings_estimate": round(total_exposure * 0.15, 2),
        "open_cases": open_cases, "claim_analysis": analysis,
        "features": ["Claim Risk Analysis", "Insurance Exposure Assessment", "Risk Forecasting", "Policy Validation"]
    })
