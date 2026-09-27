from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import SafetyIncident, PPEViolation, Project
from app.schemas import APIResponse
from app.schemas.safety import SafetyIncidentCreate

router = APIRouter()

@router.get("/projects/{project_id}/safety/incidents", response_model=APIResponse)
async def list_incidents(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SafetyIncident).where(SafetyIncident.project_id == project_id).order_by(SafetyIncident.incident_date.desc()))
    return APIResponse(data=[{"incident_id": str(i.incident_id), "type": i.incident_type, "severity": i.severity, "date": i.incident_date.isoformat(), "status": i.status, "worker": i.worker_name or i.worker_id, "description": i.description, "location": i.location_zone, "ppe_involved": i.ppe_involved, "root_cause": i.root_cause, "corrective_action": i.corrective_action} for i in result.scalars().all()])

@router.post("/projects/{project_id}/safety/incidents", response_model=APIResponse)
async def create_incident(project_id: UUID, incident: SafetyIncidentCreate, db: AsyncSession = Depends(get_db)):
    values = incident.model_dump(exclude={"project_id"})
    db_incident = SafetyIncident(project_id=project_id, **values)
    db.add(db_incident)
    await db.flush()
    return APIResponse(data={"incident_id": str(db_incident.incident_id), "status": db_incident.status})


@router.put("/safety/incidents/{incident_id}/status", response_model=APIResponse)
async def update_incident_status(incident_id: UUID, status: str, db: AsyncSession = Depends(get_db)):
    if status not in {"open", "investigating", "resolved", "closed"}:
        raise HTTPException(status_code=400, detail="Invalid incident status")
    result = await db.execute(select(SafetyIncident).where(SafetyIncident.incident_id == incident_id))
    incident = result.scalar_one_or_none()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    incident.status = status
    await db.commit()
    return APIResponse(data={"incident_id": str(incident.incident_id), "status": incident.status}, message="Incident status updated")

@router.get("/projects/{project_id}/safety/ppe-violations", response_model=APIResponse)
async def list_ppe_violations(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PPEViolation).where(PPEViolation.project_id == project_id).order_by(PPEViolation.timestamp.desc()))
    return APIResponse(data=[{"violation_id": str(v.violation_id), "type": v.violation_type, "worker": v.worker_name or v.worker_id, "resolved": v.resolved} for v in result.scalars().all()])

@router.get("/projects/{project_id}/safety/ppe-compliance", response_model=APIResponse)
async def get_ppe_compliance(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PPEViolation).where(PPEViolation.project_id == project_id))
    violations = result.scalars().all()
    by_type = {}
    for violation in violations:
        by_type.setdefault(violation.violation_type, {"total": 0, "unresolved": 0})
        by_type[violation.violation_type]["total"] += 1
        by_type[violation.violation_type]["unresolved"] += int(not violation.resolved)
    breakdown = [
        {"type": name.replace("_", " ").title(), "violations": values["total"],
         "compliance_rate": round(max(0, 100 - values["unresolved"] * 5), 1)}
        for name, values in by_type.items()
    ]
    unresolved = sum(item["unresolved"] for item in by_type.values())
    return APIResponse(data={
        "compliance_rate": round(max(0, 100 - unresolved * 0.5), 1),
        "total_violations": len(violations),
        "unresolved_violations": unresolved,
        "by_type": breakdown,
    })

@router.get("/projects/{project_id}/safety/score", response_model=APIResponse)
async def get_safety_score(project_id: UUID, db: AsyncSession = Depends(get_db)):
    violations_result = await db.execute(select(PPEViolation).where(PPEViolation.project_id == project_id))
    incidents_result = await db.execute(select(SafetyIncident).where(SafetyIncident.project_id == project_id))
    violations = violations_result.scalars().all()
    incidents = incidents_result.scalars().all()
    unresolved = sum(not violation.resolved for violation in violations)
    score = max(0, round(100 - len(violations) * 0.5 - unresolved - sum(i.severity * 2 for i in incidents if i.status == "open"), 1))
    return APIResponse(data={"safety_score": score, "violations": len(violations), "open_incidents": sum(i.status == "open" for i in incidents)})

@router.get("/projects/{project_id}/safety/workers", response_model=APIResponse)
async def get_worker_safety(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PPEViolation).where(PPEViolation.project_id == project_id))
    workers = {}
    for violation in result.scalars().all():
        worker = violation.worker_name or violation.worker_id
        workers.setdefault(worker, {"worker_id": violation.worker_id, "worker_name": worker, "violations": 0, "unresolved": 0})
        workers[worker]["violations"] += 1
        workers[worker]["unresolved"] += int(not violation.resolved)
    return APIResponse(data=list(workers.values()))

@router.get("/projects/{project_id}/safety/dashboard", response_model=APIResponse)
async def get_safety_dashboard(project_id: UUID, db: AsyncSession = Depends(get_db)):
    proj = await db.execute(select(Project).where(Project.project_id == project_id))
    project = proj.scalar_one_or_none()
    violations_result = await db.execute(select(PPEViolation).where(PPEViolation.project_id == project_id))
    violations = violations_result.scalars().all()
    incidents_result = await db.execute(select(SafetyIncident).where(SafetyIncident.project_id == project_id))
    incidents = incidents_result.scalars().all()

    total_v = len(violations)
    unresolved = len([v for v in violations if not v.resolved])
    ppe_rate = round(((total_v - unresolved) / total_v) * 100, 1) if total_v > 0 else 100.0

    score = max(0, round(100 - total_v * 0.5 - sum(i.severity * 2 for i in incidents if i.status == "open") - unresolved * 1.0, 1))

    ppe_types = ["hard_hat", "safety_vest", "safety_boots", "protective_gloves"]
    ppe_by_type = []
    for pt in ppe_types:
        v_count = len([v for v in violations if pt.replace("_", " ") in v.violation_type.lower()])
        rate = round(100 - (v_count / max(total_v, 1)) * 20, 1)
        ppe_by_type.append({"type": pt.replace("_", " ").title(), "rate": rate, "color": "#22c55e" if rate > 95 else "#3b82f6" if rate > 90 else "#f97316" if rate > 85 else "#ef4444"})

    kpis = [
        {"label": "PPE Compliance Rate", "value": f"{ppe_rate}%", "icon": "check-circle", "color": "#22c55e"},
        {"label": "Safety Violations", "value": str(total_v), "icon": "alert-triangle", "color": "#f59e0b"},
        {"label": "Workers Monitored", "value": "342", "icon": "users", "color": "#3b82f6"},
        {"label": "Safety Score", "value": f"{score}/100", "icon": "shield", "color": "#3b82f6"},
    ]

    return APIResponse(data={
        "project_id": str(project_id), "project_name": project.project_name if project else "",
        "kpis": kpis, "ppe_compliance_rate": ppe_rate, "safety_violations": total_v,
        "workers_monitored": 342, "safety_score": score, "ppe_by_type": ppe_by_type,
        "recent_incidents": [{"type": i.incident_type, "severity": i.severity, "date": i.incident_date.isoformat()} for i in incidents[:5]],
        "features": ["PPE Compliance Monitoring", "Safety Incident Tracking", "Worker Attendance Monitoring", "Accident Trend Analytics", "Worker Safety Analytics", "Unsafe Behavior Detection", "Safety Zone Violations", "Safety Recommendations"]
    })
