class AgentResult:
    def __init__(self, summary: str, evidence: dict):
        self.summary = summary
        self.evidence = evidence


class BaseAgent:
    def run(self, context: dict, query: str) -> AgentResult:
        raise NotImplementedError
