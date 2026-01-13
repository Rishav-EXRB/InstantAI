import random

class WebEnrichmentTool:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def search_entity_sentiment(self, entity_name):
        """
        Simulates searching the web for entity sentiment.
        In a real app, this would use SerpApi/Tavily + an LLM to extract a score.
        """
        # Mocking external signals
        signals = [
            "Positive mentions in industry reports",
            "Consistent high ratings on social media",
            "Recent supply chain disruptions mentioned in news",
            "Competitor price cuts impacting sentiment",
            "Stable market presence"
        ]
        
        # Randomly generate a "Web Score" between 0 and 1
        score = round(random.uniform(0.4, 0.9), 2)
        signal = random.choice(signals)
        
        return {
            "entity": entity_name,
            "web_score": score,
            "signal": f"MOCK SIGNAL: {signal}",
            "source": "External Web Search (Simulated)"
        }

    def enrich_ranking(self, ranking_df, entity_col):
        """
        Add a 'web_sentiment' score to the ranking dataframe.
        """
        # In a real scenario, this would be done selectively or cached
        # For demo, we'll apply it to the top 5
        ranking_df["web_sentiment"] = 0.5 # Default
        
        for idx, row in ranking_df.head(5).iterrows():
            result = self.search_entity_sentiment(row[entity_col])
            ranking_df.at[idx, "web_sentiment"] = result["web_score"]
            
        return ranking_df
