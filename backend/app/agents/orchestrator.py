from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.agents.site_risk_agent import SiteRiskAgent
from app.agents.safety_agent import SafetyAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.insurance_agent import InsuranceAgent
from app.agents.reporting_agent import ReportingAgent
from app.agents.base_agent import AgentResult
from app.models import Alert
from app.socket import sio
from app.services.notification_service import NotificationService
from app.config import get_settings

class AgentOrchestrator:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.agents = {
            "site_risk": SiteRiskAgent(),
            "safety": SafetyAgent(),
            "compliance": ComplianceAgent(),
            "insurance": InsuranceAgent(),
            "reporting": ReportingAgent(),
        }

    async def run_all_agents(self, project_id: str) -> dict:
        before = await self.db.execute(select(Alert.alert_id).where(Alert.project_id == project_id))
        existing_alert_ids = set(before.scalars().all())
        core_results = []
        for agent_name in ("site_risk", "safety", "compliance", "insurance"):
            core_results.append(await self.agents[agent_name].execute(project_id, self.db))

        results = {
            "site_risk": core_results[0],
            "safety": core_results[1],
            "compliance": core_results[2],
            "insurance": core_results[3],
        }

        results["reporting"] = await self.agents["reporting"].execute(project_id, self.db, results)

        await self.db.flush()
        created = await self.db.execute(select(Alert).where(Alert.project_id == project_id, Alert.alert_id.not_in(existing_alert_ids)))
        settings = get_settings()
        for alert in created.scalars().all():
            payload = {"alert_id": str(alert.alert_id), "message": alert.message, "severity": alert.severity_label, "source_agent": alert.source_agent}
            await sio.emit(f"new_alert:{project_id}", payload, room=f"project:{project_id}")
            await NotificationService().send_alert(["dashboard", "email"], alert.message, [settings.NOTIFICATION_EMAIL] if settings.NOTIFICATION_EMAIL else [])

        # Calculate project risk score
        weights = {"safety": 0.30, "site_risk": 0.25, "compliance": 0.25, "insurance": 0.20}
        score = 0
        for agent, weight in weights.items():
            if agent in results and results[agent].status == "success":
                agent_score = results[agent].metrics.get("site_risk_score", results[agent].metrics.get("safety_score", results[agent].metrics.get("compliance_score", results[agent].metrics.get("insurance_risk_score", 50))))
                if isinstance(agent_score, str): agent_score = 50
                score += agent_score * weight

        results["project_risk_score"] = round(score, 1)
        results["orchestrated_at"] = datetime.utcnow().isoformat()

        return results
