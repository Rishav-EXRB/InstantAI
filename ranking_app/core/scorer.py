from core.normalizers import min_max

def score_entities(df, ranking_config):
    entity = ranking_config["entity"]
    metrics = ranking_config["metrics"]

    agg = df.groupby(entity).mean(numeric_only=True).reset_index()
    score_df = agg[[entity]].copy()

    for name, meta in metrics.items():
        col = meta["column"]

        if col not in agg.columns:
            raise KeyError(
                f"Metric '{col}' not found in dataset. "
                f"Available columns: {list(agg.columns)}"
            )

        inverse = meta["direction"] == "low"
        weight = meta["weight"]

        score_df[f"{name}_score"] = min_max(
            agg[col], inverse=inverse
        ) * weight

    score_cols = [c for c in score_df.columns if c.endswith("_score")]
    score_df["final_score"] = score_df[score_cols].sum(axis=1)

    score_df["rank"] = (
        score_df["final_score"]
        .rank(ascending=False, method="dense")
        .astype(int)
    )

    return score_df.sort_values("rank")
