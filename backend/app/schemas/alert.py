import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class AlertCreate(BaseModel):
    project_id: uuid.UUID
    alert_type: str
    severity: int
    severity_label: str
    message: str
    source_agent: str

class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    alert_id: uuid.UUID
    project_id: uuid.UUID
    alert_type: str
    severity: int
    severity_label: str
    message: str
    created_at: datetime
    acknowledged: bool
    source_agent: str
