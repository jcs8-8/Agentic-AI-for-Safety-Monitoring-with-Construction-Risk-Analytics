import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class ReportBase(BaseModel):
    report_type: str
    file_format: str = "pdf"
    content_summary: Optional[str] = None
    generated_by: str = "Reporting Agent"

class ReportCreate(ReportBase):
    project_id: uuid.UUID


class ReportRequest(BaseModel):
    report_type: str
    file_format: str = "txt"

class ReportResponse(ReportBase):
    model_config = ConfigDict(from_attributes=True)
    report_id: uuid.UUID
    project_id: uuid.UUID
    generated_at: datetime
    file_path: Optional[str] = None
