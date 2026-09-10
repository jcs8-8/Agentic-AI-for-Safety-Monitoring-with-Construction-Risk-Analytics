from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class AgentStatus(BaseModel):
    agent_name: str
    status: str
    last_run: Optional[datetime] = None
    findings_count: int = 0
    is_running: bool = False

class AgentTriggerRequest(BaseModel):
    project_id: str

class AgentResult(BaseModel):
    agent_name: str
    project_id: str
    status: str
    findings: List[Dict[str, Any]] = []
    metrics: Dict[str, Any] = {}
    recommendations: List[str] = []
    execution_time_ms: int = 0
    created_at: datetime = datetime.utcnow()
