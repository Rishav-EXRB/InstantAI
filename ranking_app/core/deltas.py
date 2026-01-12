def compute_rank_delta(current_df, previous_df, entity_col):
    merged = current_df.merge(
        previous_df[[entity_col, "rank"]],
        on=entity_col,
        how="left",
        suffixes=("", "_prev")
    )

    merged["previous_rank"] = merged["rank_prev"].fillna(
        merged["rank"].max() + 1
    ).astype(int)

    merged["rank_change"] = merged["previous_rank"] - merged["rank"]

    return merged.drop(columns=["rank_prev"])
