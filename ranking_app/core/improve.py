def improvement_plan(row, ranking_df, metrics, top_n=10):
    plans = []

    top_peers = ranking_df.nsmallest(top_n, "rank")

    for name, meta in metrics.items():
        score_col = f"{name}_score"

        if score_col not in ranking_df.columns:
            continue

        entity_score = row[score_col]
        peer_median = top_peers[score_col].median()

        gap = peer_median - entity_score

        if gap > 0:
            direction = "increase" if meta["direction"] == "high" else "decrease"
            plans.append({
                "metric": name,
                "gap": round(gap, 3),
                "recommendation": (
                    f"{direction.capitalize()} {name} "
                    f"to peer median level"
                )
            })

    plans = sorted(plans, key=lambda x: x["gap"], reverse=True)
    return plans
