from typing import List
from app.models import SiteRisk

def calculate_site_risk_score(risks: List[SiteRisk]) -> float:
    if not risks: return 100.0
    total = sum(r.probability * r.impact * 4 * r.ai_confidence for r in risks)
    return max(0, round(100 - total / len(risks), 1))
