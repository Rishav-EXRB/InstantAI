from agents.llm import get_llm
import json

class NarrativeGenerator:
    def __init__(self):
        self.llm = get_llm()

    def generate_impact_report(self, entity_name, ranking_df, metrics_meta):
        """
        Generates a detailed narrative report on an entity's performance impact.
        """
        row = ranking_df[ranking_df.iloc[:, 0] == entity_name].iloc[0].to_dict()
        
        prompt = f"""
        Generate a professional "Impact Report" for {entity_name}.
        
        DATA:
        {json.dumps(row, indent=2)}
        
        METRICS RELEVANCE:
        {json.dumps(metrics_meta, indent=2)}
        
        The report should include:
        1. Executive Summary (1 sentence)
        2. Primary Performance Drivers (Positive and Negative)
        3. Peer Comparison Sentiment
        4. Strategic Recommendation
        
        Use a formal business tone.
        """
        
        messages = [
            {"role": "system", "content": "You are a senior business consultant."},
            {"role": "user", "content": prompt}
        ]
        
        return self.llm.chat(messages)
