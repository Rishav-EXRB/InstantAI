from agents.base_agent import BaseAgent, AgentResult
from semantic.model import get_ranking_data

class RankingAgent(BaseAgent):
    def run(self, context: dict, query: str) -> AgentResult:
        data = get_ranking_data()

        ranked = sorted(
            data,
            key=lambda x: x["score"],
            reverse=True
        )

        summary = f"{ranked[0]['name']} is currently ranked #1"

        evidence = {
            "ranking": ranked,
            "metrics_used": ["revenue", "conversion", "activity"],
            "time_window": "last_30_days"
        }

        return AgentResult(summary, evidence)
