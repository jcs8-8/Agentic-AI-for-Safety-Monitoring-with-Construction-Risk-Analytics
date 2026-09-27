import time
import random
from datetime import datetime
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base_agent import BaseAgent, AgentResult
from app.models import Alert, ComplianceCheck, Project

class ComplianceAgent(BaseAgent):
    def __init__(self):
        super().__init__("ComplianceAgent")

    async def execute(self, project_id: str, db: AsyncSession = None) -> AgentResult:
        start = time.time()
        self.status = "running"

        if db:
            project_uuid = UUID(str(project_id))
            c_result = await db.execute(select(ComplianceCheck).where(ComplianceCheck.project_id == project_uuid))
            checks = c_result.scalars().all()

            total = len(checks) or 1
            compliant = len([c for c in checks if c.compliance_status == "compliant"])
            violations = len([c for c in checks if c.compliance_status == "violation"])
            score = round((compliant / total) * 100, 1)

            new_c = []
            for _ in range(random.randint(0, 1)):
                cat = random.choice(["OSHA_Standards", "Building_Codes", "Environmental_Regulations", "Insurance_Requirements"])
                reg = {"OSHA_Standards": "OSHA-1926.501", "Building_Codes": "IBC-2021-Section-1705", "Environmental_Regulations": "EPA-Clean-Air-Act", "Insurance_Requirements": "GL-Policy-2026"}[cat]
                nc = ComplianceCheck(project_id=project_uuid, regulation_name=reg, regulation_category=cat, compliance_status=random.choice(["compliant", "pending"]), severity=random.randint(1,3))
                db.add(nc)
                new_c.append({"regulation": reg, "category": cat, "status": nc.compliance_status})

            if violations or score < 95:
                db.add(Alert(project_id=project_uuid, alert_type="compliance_violation", severity=3 if violations else 2, severity_label="High" if violations else "Medium", message=f"Compliance review found {violations} violation(s).", source_agent="ComplianceAgent"))

            metrics = {"compliance_score": score, "open_violations": violations, "audit_readiness": max(0, score - 4), "regulatory_readiness_score": score}
            recs = []
            if violations > 0: recs.append(f"{violations} compliance violations require immediate attention.")
            if score < 95: recs.append("Compliance score below target. Schedule audit.")
            if not recs: recs.append("All compliance checks passing.")
        else:
            metrics = {"compliance_score": 96.4, "open_violations": 5, "audit_readiness": 92.0}
            new_c = []
            recs = ["Demo mode"]

        self.status = "completed"
        self.last_run = datetime.utcnow()
        self.findings_count = len(new_c)
        return AgentResult(agent_name=self.name, project_id=project_id, status="success", findings=new_c, metrics=metrics, recommendations=recs, execution_time_ms=int((time.time()-start)*1000))
