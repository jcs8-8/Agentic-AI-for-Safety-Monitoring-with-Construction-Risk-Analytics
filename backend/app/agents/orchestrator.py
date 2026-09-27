from datetime import datetime
from uuid import UUID
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
from app.engine.risk_intelligence import RiskIntelligenceEngine

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
        project_uuid = UUID(str(project_id))
        before = await self.db.execute(select(Alert.alert_id).where(Alert.project_id == project_uuid))
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
        created = await self.db.execute(select(Alert).where(Alert.project_id == project_uuid, Alert.alert_id.not_in(existing_alert_ids)))
        settings = get_settings()
        for alert in created.scalars().all():
            payload = {"alert_id": str(alert.alert_id), "message": alert.message, "severity": alert.severity_label, "source_agent": alert.source_agent}
            await sio.emit(f"new_alert:{project_id}", payload, room=f"project:{project_id}")
            await NotificationService().send_alert(["dashboard", "email"], alert.message, [settings.NOTIFICATION_EMAIL] if settings.NOTIFICATION_EMAIL else [])

        engine = RiskIntelligenceEngine()
        results["project_risk_score"] = engine.calculate_project_risk_score(results)
        results["recommendations"] = engine.generate_recommendations(results)
        results["orchestrated_at"] = datetime.utcnow().isoformat()

        return results
