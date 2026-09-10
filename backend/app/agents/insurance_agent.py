import time
import random
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base_agent import BaseAgent, AgentResult
from app.models import Alert, InsuranceCase, Project

class InsuranceAgent(BaseAgent):
    def __init__(self):
        super().__init__("InsuranceAgent")

    async def execute(self, project_id: str, db: AsyncSession = None) -> AgentResult:
        start = time.time()
        self.status = "running"

        if db:
            c_result = await db.execute(select(InsuranceCase).where(InsuranceCase.project_id == project_id))
            cases = c_result.scalars().all()

            avg_risk = sum(c.risk_score for c in cases) / max(len(cases), 1) if cases else 50
            risk_level = "Low" if avg_risk < 30 else "Medium" if avg_risk < 60 else "High" if avg_risk < 80 else "Critical"
            total_exp = sum(float(c.estimated_liability or 0) for c in cases)
            open_cases = len([c for c in cases if c.status == "open"])

            new_cases = []
            for _ in range(random.randint(0, 1)):
                ct = random.choice(["workers_comp", "property_damage", "liability", "environmental"])
                rs = random.uniform(20, 85)
                rl = "Low" if rs < 30 else "Medium" if rs < 60 else "High"
                nc = InsuranceCase(project_id=project_id, claim_type=ct, risk_score=rs, risk_level=rl, status="open", estimated_liability=random.uniform(10000, 500000), incident_date=datetime.utcnow(), description=f"New {ct} risk identified", ai_recommendation="Review coverage limits")
                db.add(nc)
                new_cases.append({"type": ct, "risk_score": rs, "level": rl})

            if risk_level in ["High", "Critical"]:
                db.add(Alert(project_id=project_id, alert_type="insurance_alert", severity=4 if risk_level == "Critical" else 3, severity_label=risk_level, message=f"Insurance risk is {risk_level}; review coverage and open cases.", source_agent="InsuranceAgent"))

            metrics = {"insurance_risk_score": avg_risk, "risk_level": risk_level, "total_exposure": total_exp, "open_cases": open_cases + len(new_cases)}
            recs = []
            if risk_level in ["High", "Critical"]: recs.append("High insurance risk detected. Review coverage immediately.")
            if total_exp > 1000000: recs.append("Exposure exceeds $1M. Consider additional coverage.")
            if not recs: recs.append("Insurance risk within acceptable range.")
        else:
            metrics = {"insurance_risk_score": 55.0, "risk_level": "Medium", "total_exposure": 2500000, "open_cases": 12}
            new_cases = []
            recs = ["Demo mode"]

        self.status = "completed"
        self.last_run = datetime.utcnow()
        self.findings_count = len(new_cases)
        return AgentResult(agent_name=self.name, project_id=project_id, status="success", findings=new_cases, metrics=metrics, recommendations=recs, execution_time_ms=int((time.time()-start)*1000))
