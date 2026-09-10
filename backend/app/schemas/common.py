from typing import Any, Optional
from pydantic import BaseModel
from datetime import datetime

class APIResponse(BaseModel):
    success: bool = True
    data: Any = None
    message: str = "Operation completed successfully"
    timestamp: datetime = datetime.utcnow()
    request_id: Optional[str] = None
