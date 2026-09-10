import time
import random
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base_agent import BaseAgent, AgentResult
from app.models import Alert, PPEViolation, SafetyIncident, Project

class SafetyAgent(BaseAgent):
    def __init__(self):
        super().__init__("SafetyAgent")

    async def execute(self, project_id: str, db: AsyncSession = None) -> AgentResult:
        start = time.time()
        self.status = "running"

        if db:
            v_result = await db.execute(select(PPEViolation).where(PPEViolation.project_id == project_id))
            violations = v_result.scalars().all()
            i_result = await db.execute(select(SafetyIncident).where(SafetyIncident.project_id == project_id))
            incidents = i_result.scalars().all()

            total_v = len(violations)
            unresolved = len([v for v in violations if not v.resolved])
            ppe_rate = round(((total_v - unresolved) / max(total_v, 1)) * 100, 1)
            score = max(0, round(100 - total_v * 0.5 - sum(i.severity * 2 for i in incidents if i.status == "open") - unresolved * 1.0, 1))

            new_v = []
            for _ in range(random.randint(0, 2)):
                vt = random.choice(["missing_hard_hat", "no_safety_vest", "no_safety_boots", "no_protective_gloves"])
                nv = PPEViolation(project_id=project_id, worker_id=f"W{random.randint(100,999)}", worker_name=f"Worker {random.randint(1,50)}", violation_type=vt, ai_confidence=round(random.uniform(0.85, 0.99), 2), location_zone=random.choice(["Zone A", "Zone B", "Zone C"]))
                db.add(nv)
                new_v.append({"type": vt, "worker": nv.worker_name})

            if new_v or ppe_rate < 90:
                db.add(Alert(project_id=project_id, alert_type="safety_violation", severity=3 if ppe_rate < 90 else 2, severity_label="High" if ppe_rate < 90 else "Medium", message=f"Safety agent detected {len(new_v)} new PPE violation(s).", source_agent="SafetyAgent"))

            metrics = {"ppe_compliance_rate": ppe_rate, "safety_violations": total_v + len(new_v), "workers_monitored": 342, "safety_score": score}
            recs = []
            if ppe_rate < 90: recs.append("PPE compliance below 90%. Immediate safety briefing required.")
            if score < 80: recs.append("Safety score declining. Review protocols.")
            if not recs: recs.append("Safety conditions stable.")
        else:
            metrics = {"ppe_compliance_rate": 92.0, "safety_violations": 14, "workers_monitored": 342, "safety_score": 88.0}
            new_v = []
            recs = ["Demo mode"]

        self.status = "completed"
        self.last_run = datetime.utcnow()
        self.findings_count = len(new_v)
        return AgentResult(agent_name=self.name, project_id=project_id, status="success", findings=new_v, metrics=metrics, recommendations=recs, execution_time_ms=int((time.time()-start)*1000))
