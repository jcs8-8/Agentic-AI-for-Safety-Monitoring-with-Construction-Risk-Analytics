import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict

class ProjectBase(BaseModel):
    project_name: str
    location: str
    status: str = "active"

class ProjectCreate(ProjectBase):
    start_date: datetime

class ProjectResponse(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    project_id: uuid.UUID
    start_date: datetime
    created_at: datetime

class ProjectListResponse(BaseModel):
    projects: List[ProjectResponse]
    total: int
