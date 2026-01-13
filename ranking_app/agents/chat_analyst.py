import json
from agents.llm import get_llm

class ChatAnalyst:
    def __init__(self):
        self.llm = get_llm()
        self.system_prompt = """
        You are the InstantAI Ranking Analyst, an expert in business performance, metric analysis, and strategic coaching.
        Your goal is to help users understand why rankings change and how to improve them.
        
        Guidelines:
        1. Be objective and data-driven.
        2. Focus on root causes (key drivers) of rank changes.
        3. Provide actionable recommendations.
        4. If you don't have enough data, ask the user for specific details.
        5. Explain mathematical impacts clearly (e.g., "Rank dropped because Revenue fell 15% while peers grew 5%").
        """

    def analyze(self, user_query, ranking_df, entity_key, config_meta):
        """
        Analyze the ranking data based on a user query.
        """
        # Prepare context
        top_entities = ranking_df.head(5).to_dict(orient="records")
        bottom_entities = ranking_df.tail(5).to_dict(orient="records")
        
        context = {
            "entity_type": entity_key,
            "metrics_defined": config_meta.get("ranking", {}).get("metrics", {}),
            "top_performers": top_entities,
            "bottom_performers": bottom_entities,
            "total_entities": len(ranking_df)
        }
        
        prompt = f"""
        CONTEXT:
        {json.dumps(context, indent=2)}
        
        USER QUERY:
        {user_query}
        
        Based on the data and the user query, provide a detailed analysis. 
        If the user asks for a specific entity, focus on their performance metrics and gap analysis against peers.
        """
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.llm.chat(messages)

    def generate_why_trace(self, entity_name, row_data, metrics_meta):
        """
        Produce a concise mathematical explanation for an entity's rank.
        """
        prompt = f"""
        ENTITY: {entity_name}
        PERFORMANCE DATA: {json.dumps(row_data.to_dict(), indent=2)}
        METRICS DEFS: {json.dumps(metrics_meta, indent=2)}
        
        Explain in 2-3 bullet points WHY this entity has its current rank. 
        Focus on the highest and lowest scoring metrics and their weights.
        """
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": prompt}
        ]
        
        return self.llm.chat(messages, temperature=0.0)
