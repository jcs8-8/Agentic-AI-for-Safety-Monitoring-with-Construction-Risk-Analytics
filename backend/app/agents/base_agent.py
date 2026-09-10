from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel

class AgentResult(BaseModel):
    agent_name: str
    project_id: str
    status: str
    findings: List[Dict[str, Any]] = []
    metrics: Dict[str, Any] = {}
    recommendations: List[str] = []
    execution_time_ms: int = 0
    created_at: datetime = datetime.utcnow()

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self.status = "idle"
        self.last_run = None
        self.findings_count = 0

    @abstractmethod
    async def execute(self, project_id: str, db=None) -> AgentResult:
        pass
