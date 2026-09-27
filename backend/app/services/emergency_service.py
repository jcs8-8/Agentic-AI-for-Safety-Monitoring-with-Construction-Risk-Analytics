from datetime import datetime
from typing import Any
import os
from app.socket import sio

SESSIONS: dict[str, dict[str, Any]] = {}
REPORTS: list[dict[str, Any]] = []

def notification_status() -> dict[str, Any]:
    return {"sms_sent": 0, "sms_total": 0, "teams": "posted" if os.getenv("TEAMS_WEBHOOK_URL") else "mock-posted", "siren": True, "undelivered": 0, "provider": "twilio" if os.getenv("TWILIO_ACCOUNT_SID") else "mock"}

async def activate(payload: dict[str, Any]) -> dict[str, Any]:
    session_id = f"session-{int(datetime.now().timestamp())}"
    session = {**payload, "id": session_id, "incident_id": f"INC-2026-{len(REPORTS) + 1:03d}", "state": "ACTIVE", "activated_at": datetime.now().isoformat(), "timeline": [], "checklist": [], "cameras": [], "notifications": notification_status()}
    SESSIONS[session_id] = session
    await sio.emit("EMERGENCY_ACTIVATED", session)
    return session

async def update(session_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    SESSIONS[session_id] = {**SESSIONS.get(session_id, {}), **payload}
    await sio.emit("EMERGENCY_UPDATED", SESSIONS[session_id])
    return SESSIONS[session_id]

async def close(session_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    session = SESSIONS.get(session_id, {})
    report = {**session, **payload, "id": session.get("incident_id", f"INC-2026-{len(REPORTS) + 1:03d}"), "closed_at": datetime.now().isoformat(), "state": "CLOSED"}
    REPORTS.insert(0, report)
    SESSIONS.pop(session_id, None)
    await sio.emit("EMERGENCY_DEACTIVATED", report)
    return report