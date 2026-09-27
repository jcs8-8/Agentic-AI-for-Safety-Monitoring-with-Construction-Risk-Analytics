from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.schemas import APIResponse
from app.services.copilot_service import answer, execute

router = APIRouter()

class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    history: list[dict[str, Any]] = []

class ActionRequest(BaseModel):
    tool: str
    role: str = "site_manager"
    alertId: str | None = None
    assignee: str | None = None
    reason: str | None = None

@router.post("/copilot/chat", response_model=APIResponse)
async def copilot_chat(request: ChatRequest):
    return APIResponse(data=answer(request.message))

@router.post("/copilot/action", response_model=APIResponse)
async def copilot_action(request: ActionRequest):
    return APIResponse(data=execute(request.model_dump()))