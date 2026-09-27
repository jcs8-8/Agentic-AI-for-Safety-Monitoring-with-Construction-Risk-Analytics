import time
from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base_agent import BaseAgent, AgentResult
from app.models import Alert, ComplianceCheck, InsuranceCase, Report, SafetyIncident, SiteRisk

class ReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportingAgent")

    async def execute(self, project_id: str, db: AsyncSession = None, agent_results: dict = None) -> AgentResult:
        start = time.time()
        self.status = "running"

        if db is None:
            self.status = "failed"
            return AgentResult(agent_name=self.name, project_id=project_id, status="failed", recommendations=["Database session is required for reporting intelligence."])

        project_uuid = UUID(str(project_id))
        totals = {name: len((await db.execute(query)).scalars().all()) for name, query in {
            "alerts": select(Alert.alert_id).where(Alert.project_id == project_uuid),
            "incidents": select(SafetyIncident.incident_id).where(SafetyIncident.project_id == project_uuid),
            "risks": select(SiteRisk.risk_id).where(SiteRisk.project_id == project_uuid),
            "compliance_checks": select(ComplianceCheck.compliance_id).where(ComplianceCheck.project_id == project_uuid),
            "insurance_cases": select(InsuranceCase.case_id).where(InsuranceCase.project_id == project_uuid),
        }.items()}
        summary = "Site intelligence summary: " + ", ".join(f"{key.replace('_', ' ')}={value}" for key, value in totals.items()) + "."
        report = Report(project_id=project_uuid, report_type="executive_summary", file_format="txt", content_summary=summary, generated_by=self.name)
        db.add(report)
        await db.flush()
        generated = [{"report_type": report.report_type, "report_id": str(report.report_id), "status": "generated", "summary": summary}]

        metrics = {"reports_generated": 1, "source_metrics": totals}
        recs = ["Reports generated successfully. Distribute to stakeholders."]

        self.status = "completed"
        self.last_run = datetime.utcnow()
        self.findings_count = len(generated)
        return AgentResult(agent_name=self.name, project_id=project_id, status="success", findings=generated, metrics=metrics, recommendations=recs, execution_time_ms=int((time.time()-start)*1000))
