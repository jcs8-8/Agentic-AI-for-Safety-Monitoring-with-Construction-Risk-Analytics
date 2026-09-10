from typing import List, Dict, Any
from app.agents.base_agent import AgentResult

class RiskIntelligenceEngine:
    def calculate_project_risk_score(self, agent_results: Dict[str, AgentResult]) -> float:
        weights = {"safety": 0.30, "site_risk": 0.25, "compliance": 0.25, "insurance": 0.20}
        score = 0
        for agent, weight in weights.items():
            if agent in agent_results and agent_results[agent].status == "success":
                m = agent_results[agent].metrics
                agent_score = m.get("site_risk_score", m.get("safety_score", m.get("compliance_score", m.get("insurance_risk_score", 50))))
                if isinstance(agent_score, str): agent_score = 50
                score += agent_score * weight
        return round(score, 1)

    def generate_recommendations(self, agent_results: Dict[str, AgentResult]) -> List[str]:
        recs = []
        if "safety" in agent_results:
            ppe = agent_results["safety"].metrics.get("ppe_compliance_rate", 100)
            if ppe < 90: recs.append("CRITICAL: PPE compliance below 90%. Immediate safety briefing required.")
        if "site_risk" in agent_results:
            hrz = agent_results["site_risk"].metrics.get("high_risk_zones", 0)
            if hrz > 5: recs.append(f"HIGH PRIORITY: {hrz} high-risk zones detected. Conduct immediate inspection.")
        if "compliance" in agent_results:
            v = agent_results["compliance"].metrics.get("open_violations", 0)
            if v > 0: recs.append(f"{v} compliance violations require attention.")
        if not recs: recs.append("All systems operating within normal parameters.")
        return recs
