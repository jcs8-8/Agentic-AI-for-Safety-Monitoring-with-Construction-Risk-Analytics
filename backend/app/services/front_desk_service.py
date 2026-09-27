from datetime import datetime
from typing import Any
from uuid import uuid4

STATE: dict[str, Any] = {"visitors": [], "deliveries": [], "tickets": [], "workers": [], "muster_active": False, "attendance_log": []}

def get_state() -> dict[str, Any]: return STATE
def replace_state(payload: dict[str, Any]) -> dict[str, Any]: STATE.update(payload); return STATE
def create_ticket(payload: dict[str, Any]) -> dict[str, Any]:
    ticket = {**payload, "id": f"ENG-{1000 + len(STATE['tickets']) + 1}", "created_at": datetime.now().isoformat()}; STATE["tickets"].insert(0, ticket); return ticket
def create_visitor(payload: dict[str, Any]) -> dict[str, Any]:
    visitor = {**payload, "id": str(uuid4()), "status": "Expected", "badge": f"VIS-{100 + len(STATE['visitors']) + 1}"}; STATE["visitors"].append(visitor); return visitor
def check_in(visitor_id: str) -> dict[str, Any] | None:
    for visitor in STATE["visitors"]:
        if visitor["id"] == visitor_id: visitor.update({"status": "Checked in", "checked_in_at": datetime.now().isoformat()}); return visitor
    return None