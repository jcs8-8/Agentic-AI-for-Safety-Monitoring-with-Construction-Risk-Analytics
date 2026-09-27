from typing import Any
from fastapi import APIRouter, HTTPException
from app.schemas import APIResponse
from app.services import front_desk_service as service

router = APIRouter()
@router.get('/front-desk', response_model=APIResponse)
async def get_front_desk(): return APIResponse(data=service.get_state())
@router.put('/front-desk', response_model=APIResponse)
async def put_front_desk(payload: dict[str, Any]): return APIResponse(data=service.replace_state(payload))
@router.post('/front-desk/tickets', response_model=APIResponse)
async def post_ticket(payload: dict[str, Any]): return APIResponse(data=service.create_ticket(payload))
@router.patch('/front-desk/tickets/{ticket_id}', response_model=APIResponse)
async def patch_ticket(ticket_id: str, payload: dict[str, Any]):
    for ticket in service.STATE['tickets']:
        if ticket['id'] == ticket_id: ticket.update(payload); return APIResponse(data=ticket)
    raise HTTPException(404, 'Ticket not found')
@router.post('/front-desk/visitors', response_model=APIResponse)
async def post_visitor(payload: dict[str, Any]): return APIResponse(data=service.create_visitor(payload))
@router.post('/front-desk/visitors/{visitor_id}/check-in', response_model=APIResponse)
async def post_check_in(visitor_id: str):
    visitor = service.check_in(visitor_id)
    if not visitor: raise HTTPException(404, 'Visitor not found')
    return APIResponse(data=visitor)