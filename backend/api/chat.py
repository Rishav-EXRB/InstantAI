from fastapi import APIRouter
from agents.ranking_agent import RankingAgent

router = APIRouter()
ranking_agent = RankingAgent()

@router.post("/chat")
def chat(query: str):
    result = ranking_agent.run(context={}, query=query)
    return {
        "summary": result.summary,
        "evidence": result.evidence
    }
