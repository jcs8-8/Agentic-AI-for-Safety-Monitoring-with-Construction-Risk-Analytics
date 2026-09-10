from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import APIResponse, AgentStatus, AgentTriggerRequest
from app.agents.site_risk_agent import SiteRiskAgent
from app.agents.safety_agent import SafetyAgent
from app.agents.compliance_agent import ComplianceAgent
from app.agents.insurance_agent import InsuranceAgent
from app.agents.reporting_agent import ReportingAgent
from app.agents.orchestrator import AgentOrchestrator
from app.socket import sio

router = APIRouter()

AGENTS = {
    "site_risk": SiteRiskAgent(),
    "safety": SafetyAgent(),
    "compliance": ComplianceAgent(),
    "insurance": InsuranceAgent(),
    "reporting": ReportingAgent(),
}

@router.get("", response_model=APIResponse)
async def list_agents():
    agents = [AgentStatus(agent_name=name, status=agent.status, last_run=agent.last_run, findings_count=agent.findings_count, is_running=agent.status == "running") for name, agent in AGENTS.items()]
    return APIResponse(data=agents)

@router.post("/{agent_name}/trigger", response_model=APIResponse)
async def trigger_agent(agent_name: str, req: AgentTriggerRequest, db: AsyncSession = Depends(get_db)):
    if agent_name not in AGENTS:
        return APIResponse(success=False, message=f"Agent {agent_name} not found")
    agent = AGENTS[agent_name]
    await sio.emit("agent_status_change", {"agent_name": agent_name, "status": "running", "project_id": str(req.project_id)}, room=f"project:{req.project_id}")
    result = await agent.execute(req.project_id, db)
    await sio.emit("agent_status_change", {"agent_name": agent_name, "status": "completed", "project_id": str(req.project_id)}, room=f"project:{req.project_id}")
    await sio.emit(f"dashboard_update:{req.project_id}", {"project_id": str(req.project_id), "agent": agent_name}, room=f"project:{req.project_id}")
    return APIResponse(data=result, message=f"Agent {agent_name} completed")

@router.post("/orchestrate", response_model=APIResponse)
async def orchestrate(req: AgentTriggerRequest, db: AsyncSession = Depends(get_db)):
    await sio.emit("agent_status_change", {"status": "running", "project_id": str(req.project_id)}, room=f"project:{req.project_id}")
    orch = AgentOrchestrator(db)
    results = await orch.run_all_agents(req.project_id)
    await sio.emit("agent_status_change", {"status": "completed", "project_id": str(req.project_id)}, room=f"project:{req.project_id}")
    await sio.emit(f"dashboard_update:{req.project_id}", {"project_id": str(req.project_id), "results": jsonable_encoder(results)}, room=f"project:{req.project_id}")
    return APIResponse(data=results, message="All agents orchestrated successfully")
