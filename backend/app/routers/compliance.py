from uuid import UUID
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import ComplianceCheck, InsuranceCase, Project
from app.schemas import APIResponse
from app.schemas.compliance import ComplianceCheckBase

router = APIRouter()

class ComplianceStatusUpdate(BaseModel):
    status: str

def score_for_check(check: ComplianceCheck) -> int:
    values = {"compliant": 100, "under_review": 70, "pending": 50}
    return values.get(check.compliance_status, max(0, 100 - check.severity * 20))

@router.post("/projects/{project_id}/compliance", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_compliance_check(project_id: UUID, payload: ComplianceCheckBase, db: AsyncSession = Depends(get_db)):
    project = await db.get(Project, project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    check = ComplianceCheck(project_id=project_id, **payload.model_dump(exclude={"project_id"}))
    db.add(check)
    await db.flush()
    return APIResponse(data={"id": str(check.compliance_id), "project_id": str(project_id), "status": check.compliance_status})

@router.get("/projects/{project_id}/compliance", response_model=APIResponse)
async def list_compliance(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ComplianceCheck).where(ComplianceCheck.project_id == project_id))
    return APIResponse(data=[{"id": str(c.compliance_id), "regulation": c.regulation_name, "status": c.compliance_status, "category": c.regulation_category} for c in result.scalars().all()])

@router.get("/projects/{project_id}/compliance/score", response_model=APIResponse)
async def get_compliance_score(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ComplianceCheck).where(ComplianceCheck.project_id == project_id))
    checks = result.scalars().all()
    score = sum(score_for_check(check) for check in checks) / len(checks) if checks else 0
    return APIResponse(data={"compliance_score": round(score, 1), "total_checks": len(checks), "open_violations": sum(check.compliance_status == "violation" for check in checks)})

@router.get("/projects/{project_id}/compliance/categories", response_model=APIResponse)
async def get_compliance_categories(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ComplianceCheck).where(ComplianceCheck.project_id == project_id))
    categories = {}
    for check in result.scalars().all():
        categories.setdefault(check.regulation_category, []).append(check)
    data = []
    for category, checks in categories.items():
        score = sum(score_for_check(check) for check in checks) / len(checks)
        data.append({"category": category, "score": round(score, 1), "total": len(checks), "violations": sum(check.compliance_status == "violation" for check in checks)})
    return APIResponse(data=data)

@router.put("/compliance/{check_id}/status", response_model=APIResponse)
async def update_compliance_status(check_id: UUID, update: ComplianceStatusUpdate, db: AsyncSession = Depends(get_db)):
    if update.status not in {"compliant", "violation", "pending", "under_review"}:
        raise HTTPException(status_code=422, detail="Invalid compliance status")
    result = await db.execute(select(ComplianceCheck).where(ComplianceCheck.compliance_id == check_id))
    check = result.scalar_one_or_none()
    if check is None:
        return APIResponse(data=None, message="Compliance check not found")
    check.compliance_status = update.status
    return APIResponse(data={"id": str(check.compliance_id), "status": check.compliance_status})

@router.get("/projects/{project_id}/compliance/dashboard", response_model=APIResponse)
async def get_compliance_dashboard(project_id: UUID, db: AsyncSession = Depends(get_db)):
    proj = await db.execute(select(Project).where(Project.project_id == project_id))
    project = proj.scalar_one_or_none()
    checks_result = await db.execute(select(ComplianceCheck).where(ComplianceCheck.project_id == project_id))
    checks = checks_result.scalars().all()

    total = len(checks) or 1
    compliant = len([c for c in checks if c.compliance_status == "compliant"])
    violations = len([c for c in checks if c.compliance_status == "violation"])
    score = round(sum(score_for_check(check) for check in checks) / total, 1)
    now = datetime.now(timezone.utc)
    overdue = []
    upcoming = []
    for check in checks:
        if not check.next_inspection_date:
            continue
        inspection_date = check.next_inspection_date
        if inspection_date.tzinfo is None:
            inspection_date = inspection_date.replace(tzinfo=timezone.utc)
        if inspection_date < now:
            overdue.append(check)
        else:
            upcoming.append((check, inspection_date))
    documented = sum(bool(check.documentation_url) for check in checks)

    categories = {}
    for c in checks:
        cat = c.regulation_category
        if cat not in categories:
            categories[cat] = {"total": 0, "compliant": 0}
        categories[cat]["total"] += 1
        if c.compliance_status == "compliant":
            categories[cat]["compliant"] += 1

    by_category = [{"category": k.replace("_", " ").title(), "score": round((v["compliant"]/v["total"])*100, 1), "color": "#22c55e" if (v["compliant"]/v["total"]) > 0.95 else "#3b82f6" if (v["compliant"]/v["total"]) > 0.90 else "#f97316"} for k, v in categories.items()]

    # Insurance risk from cases
    cases_result = await db.execute(select(InsuranceCase).where(InsuranceCase.project_id == project_id))
    cases = cases_result.scalars().all()
    avg_risk = sum(c.risk_score for c in cases) / len(cases) if cases else 50
    risk_level = "Low" if avg_risk < 30 else "Medium" if avg_risk < 60 else "High" if avg_risk < 80 else "Critical"

    compliance_kpis = [
        {"label": "Compliance Score", "value": f"{score}%", "icon": "check-circle", "color": "#22c55e"},
        {"label": "Open Violations", "value": str(violations), "icon": "alert-triangle", "color": "#f59e0b"},
    ]
    audit_readiness = max(0, round(score - len(overdue) * 2, 1))
    insurance_kpis = [
        {"label": "Insurance Risk Score", "value": risk_level, "icon": "shield", "color": "#f59e0b" if risk_level == "Medium" else "#ef4444" if risk_level in ["High", "Critical"] else "#22c55e"},
        {"label": "Audit Readiness", "value": f"{audit_readiness}%", "icon": "file-check", "color": "#3b82f6"},
    ]

    return APIResponse(data={
        "project_id": str(project_id), "project_name": project.project_name if project else "",
        "compliance_kpis": compliance_kpis, "insurance_kpis": insurance_kpis,
        "compliance_score": score, "open_violations": violations,
        "audit_readiness": audit_readiness,
        "overdue_inspections": len(overdue),
        "documentation_coverage": round((documented / total) * 100, 1),
        "upcoming_inspections": [{"regulation": check.regulation_name, "date": inspection_date.isoformat()} for check, inspection_date in upcoming[:5]],
        "applications": {"approval_rate": round((compliant / total) * 100, 1), "processing_time_days": None},
        "insurance_risk_score": risk_level, "compliance_by_category": by_category,
        "features": ["Regulatory Compliance Dashboard", "Compliance Audit Results", "Claim Risk Analysis", "Documentation Status", "Inspection Tracking", "Insurance Risk Assessment", "Compliance Violation Monitoring", "Regulatory Readiness Score"]
    })
