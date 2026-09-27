from typing import List, Dict, Any
from app.agents.base_agent import AgentResult

class RiskIntelligenceEngine:
    WEIGHTS = {"safety": 0.30, "site_risk": 0.25, "compliance": 0.25, "insurance": 0.20}

    def calculate_project_risk_score(self, agent_results: Dict[str, AgentResult]) -> float:
        weighted_score = 0
        applied_weight = 0
        for agent, weight in self.WEIGHTS.items():
            if agent in agent_results and agent_results[agent].status == "success":
                metrics = agent_results[agent].metrics
                agent_score = next((metrics[key] for key in ("site_risk_score", "safety_score", "compliance_score", "insurance_risk_score") if key in metrics), 50)
                if isinstance(agent_score, (int, float)):
                    weighted_score += max(0, min(100, agent_score)) * weight
                    applied_weight += weight
        return round(weighted_score / applied_weight, 1) if applied_weight else 50.0

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
        if "insurance" in agent_results:
            exposure = agent_results["insurance"].metrics.get("total_exposure", 0)
            if exposure > 0: recs.append(f"Review insurance exposure of ${exposure:,.0f} across active cases.")
        if not recs: recs.append("All systems operating within normal parameters.")
        return recs
