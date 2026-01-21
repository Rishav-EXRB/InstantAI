import pandas as pd
import numpy as np


def generate_explanations(
    df: pd.DataFrame,
    entity_column: str,
    ranked_df: pd.DataFrame,
    metric_map: dict
):
    """
    Generate explanations for each metric used in ranking.
    Fully defensive:
    - Supports float-only metric maps
    - Supports rich metric metadata
    - Ignores missing / invalid columns
    - Never throws
    """

    explanations = {}

    for metric, meta in metric_map.items():

        # ---------- NORMALIZE METRIC META ----------
        if isinstance(meta, dict):
            column = meta.get("column", metric)
            weight = meta.get("weight", 1.0)
        else:
            column = metric
            weight = float(meta)

        if column not in df.columns:
            continue

        series = pd.to_numeric(df[column], errors="coerce").dropna()

        if series.empty:
            continue

        explanations[metric] = {
            "column_used": column,
            "weight": round(float(weight), 4),
            "mean": round(float(series.mean()), 4),
            "max": round(float(series.max()), 4),
            "min": round(float(series.min()), 4),
            "explanation": (
                f"Entities with higher {column.replace('_', ' ')} "
                f"receive a higher ranking contribution."
            )
        }

    return explanations
