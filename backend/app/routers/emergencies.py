from typing import Any
from fastapi import APIRouter
from app.schemas import APIResponse
from app.services import emergency_service

router = APIRouter()

@router.post("/emergencies", response_model=APIResponse)
async def create_emergency(payload: dict[str, Any]): return APIResponse(data=await emergency_service.activate(payload))

@router.post("/emergencies/request", response_model=APIResponse)
async def request_emergency(payload: dict[str, Any]): return APIResponse(data={"requested": True, "payload": payload}, message="Emergency activation request sent to authorized managers")

@router.put("/emergencies/{session_id}", response_model=APIResponse)
async def update_emergency(session_id: str, payload: dict[str, Any]): return APIResponse(data=await emergency_service.update(session_id, payload))

@router.post("/emergencies/{session_id}/close", response_model=APIResponse)
async def close_emergency(session_id: str, payload: dict[str, Any]): return APIResponse(data=await emergency_service.close(session_id, payload))

@router.get("/emergencies", response_model=APIResponse)
async def list_emergencies(): return APIResponse(data=emergency_service.REPORTS)