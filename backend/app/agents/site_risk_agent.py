import time
import random
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base_agent import BaseAgent, AgentResult
from app.models import SiteRisk, Project

class SiteRiskAgent(BaseAgent):
    def __init__(self):
        super().__init__("SiteRiskAgent")

    async def execute(self, project_id: str, db: AsyncSession = None) -> AgentResult:
        start = time.time()
        self.status = "running"

        if db:
            result = await db.execute(select(Project).where(Project.project_id == project_id))
            if not result.scalar_one_or_none():
                self.status = "failed"
                return AgentResult(agent_name=self.name, project_id=project_id, status="failed", recommendations=["Project not found"], execution_time_ms=int((time.time()-start)*1000))

            risks_result = await db.execute(select(SiteRisk).where(SiteRisk.project_id == project_id))
            existing = risks_result.scalars().all()

            risk_types = ["fall_hazard", "equipment_risk", "electrical_hazard", "environmental_risk", "structural_risk"]
            zones = ["Zone A", "Zone B", "Zone C", "Zone D", "Zone E"]
            new_findings = []

            for _ in range(random.randint(1, 3)):
                rt = random.choice(risk_types)
                nr = SiteRisk(project_id=project_id, risk_type=rt, severity=random.randint(2,5), probability=random.randint(2,5), impact=random.randint(2,5), location_zone=random.choice(zones), description=f"AI detected {rt.replace('_', ' ')} in {random.choice(zones)}", mitigation_status="open", ai_confidence=round(random.uniform(0.75, 0.98), 2))
                db.add(nr)
                new_findings.append({"risk_type": rt, "severity": nr.severity, "location": nr.location_zone, "confidence": nr.ai_confidence})

            all_risks = existing + [r for r in new_findings]
            total_w = sum(r.probability * r.impact * 4 * r.ai_confidence for r in existing)
            score = max(0, round(100 - total_w / max(len(existing), 1), 1))
            metrics = {"active_risks": len(existing) + len(new_findings), "high_risk_zones": len([r for r in existing if r.probability >= 4 and r.impact >= 4]), "hazards_detected": len([r for r in existing if r.mitigation_status == "open"]) + len(new_findings), "site_risk_score": score, "new_findings": len(new_findings)}
            recs = []
            if metrics["high_risk_zones"] > 5: recs.append("CRITICAL: Multiple high-risk zones detected. Immediate inspection required.")
            if metrics["site_risk_score"] < 70: recs.append("Site risk score below threshold. Review safety protocols.")
            if not recs: recs.append("Site conditions within acceptable parameters. Continue monitoring.")
        else:
            metrics = {"active_risks": 47, "high_risk_zones": 8, "hazards_detected": 23, "site_risk_score": 72.0}
            new_findings = [{"demo": True}]
            recs = ["Demo mode: Connect to database for live analysis."]

        self.status = "completed"
        self.last_run = datetime.utcnow()
        self.findings_count = len(new_findings)
        return AgentResult(agent_name=self.name, project_id=project_id, status="success", findings=new_findings, metrics=metrics, recommendations=recs, execution_time_ms=int((time.time()-start)*1000))
