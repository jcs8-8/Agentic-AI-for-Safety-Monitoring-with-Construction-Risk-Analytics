from datetime import datetime
from typing import Any

TOOLS = {"query_alerts", "get_risk_scores", "get_analytics", "get_predictions", "generate_report", "assign_alert", "escalate_alert", "create_task", "dismiss_alert", "small_talk"}

def _response(text: str, tool: str, widget: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"text": text, "tool": tool, "source": {"query_alerts": "Safety Agent", "get_risk_scores": "Risk Intelligence Engine", "get_analytics": "Reporting Agent", "get_predictions": "Risk Intelligence Engine", "generate_report": "Reporting Agent"}.get(tool), "asOf": datetime.now().strftime("%H:%M today"), "widget": widget}

def answer(message: str) -> dict[str, Any]:
    query = message.lower()
    if any(word in query for word in ("assign", "escalate", "dismiss", "false positive")):
        tool = "assign_alert" if "assign" in query else "escalate_alert" if "escalate" in query else "dismiss_alert"
        return _response("This workflow change needs your confirmation before it runs.", tool, {"type": "confirm", "action": {"tool": tool, "alertId": "platform-alert", "reason": message}, "label": tool.replace("_", " ").title(), "detail": message})
    if "risk" in query and any(word in query for word in ("score", "riskiest", "today")):
        return _response("The current project risk score is 78/100. Zone B is the riskiest area today.", "get_risk_scores", {"type": "risk", "score": 78, "zones": [{"name": "Zone B", "score": 62, "openHazards": 7}, {"name": "Zone C", "score": 74, "openHazards": 4}, {"name": "Zone A", "score": 86, "openHazards": 2}]})
    if any(word in query for word in ("trend", "compare", "compliance")):
        return _response("Safety compliance improved 8 points this month compared with last month.", "get_analytics", {"type": "chart", "chart": "line", "title": "Safety compliance trend", "xKey": "period", "yKeys": ["current", "previous"], "data": [{"period": "Mon", "current": 86, "previous": 78}, {"period": "Tue", "current": 89, "previous": 80}, {"period": "Wed", "current": 91, "previous": 83}]})
    if any(word in query for word in ("forecast", "tomorrow", "exposure")):
        return _response("Tomorrow night shift is forecast at elevated exposure because open hazards remain.", "get_predictions", {"type": "forecast", "title": "Night shift risk forecast", "value": "Elevated · 71/100", "confidence": "87% confidence", "actions": ["Close or isolate open hazards before shift handover.", "Add a supervisor walkthrough."]})
    if any(word in query for word in ("report", "summary")):
        return _response("I prepared a report preview using site activity and alert data.", "generate_report", {"type": "report", "title": "Yesterday site report", "period": datetime.now().strftime("%d %b %Y"), "reportId": "site-report", "highlights": ["3 critical alerts reviewed", "Safety compliance: 91%", "No recordable incidents"]})
    if any(word in query for word in ("alert", "incident", "ppe", "critical")):
        return _response("I found 2 open high-severity alerts matching platform data.", "query_alerts", {"type": "alerts", "alerts": [{"id": "platform-alert-1", "severity": "Critical", "message": "PPE violation detected near the material hoist.", "zone": "Zone B", "source": "Safety Agent", "createdAt": "Today, 13:28", "acknowledged": False}]})
    return {"text": "I can only answer from BuildSure platform data. Ask about alerts, risk, trends, forecasts, reports, or workflow actions.", "tool": "small_talk"}

def execute(action: dict[str, Any]) -> dict[str, Any]:
    role = action.get("role", "site_manager").lower()
    if action.get("tool") == "dismiss_alert" and role == "executive":
        return _response("Your EXECUTIVE role cannot dismiss alerts.", "dismiss_alert")
    return _response("The action was completed and the workflow has been updated.", action["tool"])