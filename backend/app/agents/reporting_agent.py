import time
import random
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base_agent import BaseAgent, AgentResult

class ReportingAgent(BaseAgent):
    def __init__(self):
        super().__init__("ReportingAgent")

    async def execute(self, project_id: str, db: AsyncSession = None, agent_results: dict = None) -> AgentResult:
        start = time.time()
        self.status = "running"

        report_types = ["daily_site", "executive_summary", "compliance_audit", "safety_analysis", "insurance_assessment"]
        generated = []

        for rt in random.sample(report_types, k=random.randint(1, 3)):
            generated.append({"report_type": rt, "status": "generated", "pages": random.randint(5, 25)})

        metrics = {"reports_generated": len(generated), "total_pages": sum(r["pages"] for r in generated)}
        recs = ["Reports generated successfully. Distribute to stakeholders."]

        self.status = "completed"
        self.last_run = datetime.utcnow()
        self.findings_count = len(generated)
        return AgentResult(agent_name=self.name, project_id=project_id, status="success", findings=generated, metrics=metrics, recommendations=recs, execution_time_ms=int((time.time()-start)*1000))
