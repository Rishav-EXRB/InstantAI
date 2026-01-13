import pandas as pd

class DataTool:
    def __init__(self, df):
        self.df = df

    def get_entity_data(self, entity_col, entity_name):
        """Retrieve all records for a specific entity."""
        return self.df[self.df[entity_col] == entity_name].to_dict(orient="records")

    def get_top_movers(self, ranking_df, n=3):
        """Retrieve top positive and negative rank movers."""
        top_positive = ranking_df.sort_values("rank_change", ascending=False).head(n)
        top_negative = ranking_df.sort_values("rank_change", ascending=True).head(n)
        return {
            "gainers": top_positive.to_dict(orient="records"),
            "decliners": top_negative.to_dict(orient="records")
        }

    def get_metric_stats(self, metric_col):
        """Retrieve basic statistics for a metric."""
        if metric_col not in self.df.columns:
            return f"Error: Metric {metric_col} not found."
        return self.df[metric_col].describe().to_dict()
