from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Alert, ComplianceCheck, InsuranceCase, Report, SafetyIncident, SiteRisk
from app.schemas import APIResponse
from app.schemas.report import ReportRequest

router = APIRouter()

@router.get("/projects/{project_id}/reports", response_model=APIResponse)
async def list_reports(project_id: UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Report).where(Report.project_id == project_id).order_by(Report.generated_at.desc()))
    return APIResponse(data=[{"id": str(r.report_id), "type": r.report_type, "format": r.file_format, "generated": r.generated_at.isoformat(), "summary": r.content_summary or "", "generated_by": r.generated_by} for r in result.scalars().all()])


@router.post("/projects/{project_id}/reports", response_model=APIResponse)
async def generate_report(project_id: UUID, request: ReportRequest, db: AsyncSession = Depends(get_db)):
    totals = {
        "alerts": await db.scalar(select(func.count(Alert.alert_id)).where(Alert.project_id == project_id)),
        "incidents": await db.scalar(select(func.count(SafetyIncident.incident_id)).where(SafetyIncident.project_id == project_id)),
        "site risks": await db.scalar(select(func.count(SiteRisk.risk_id)).where(SiteRisk.project_id == project_id)),
        "compliance checks": await db.scalar(select(func.count(ComplianceCheck.compliance_id)).where(ComplianceCheck.project_id == project_id)),
        "insurance cases": await db.scalar(select(func.count(InsuranceCase.case_id)).where(InsuranceCase.project_id == project_id)),
    }
    summary = ", ".join(f"{name}: {value or 0}" for name, value in totals.items())
    report = Report(project_id=project_id, report_type=request.report_type, file_format=request.file_format, content_summary=summary, generated_by="Reporting Agent")
    db.add(report)
    await db.flush()
    return APIResponse(data={"id": str(report.report_id), "type": report.report_type, "format": report.file_format, "generated": report.generated_at.isoformat(), "summary": summary, "generated_by": report.generated_by}, message="Report generated")
