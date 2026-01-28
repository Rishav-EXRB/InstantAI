import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def rank_entities(df, entity_column, metric_map):
    """
    Cluster-based ranking that supports BOTH metric_map formats:

    Format A:
    {
        "sales": 0.6,
        "profit": 0.4
    }

    Format B:
    {
        "sales": {"column": "SALES", "weight": 0.6},
        "profit": {"column": "PROFIT", "weight": 0.4}
    }
    """

    columns = []
    weights = []

    # ------------------ Normalize metric_map ------------------
    for metric, meta in metric_map.items():

        # Case 1: meta is a float → column name == metric
        if isinstance(meta, (int, float)):
            column = metric
            weight = float(meta)

        # Case 2: meta is dict
        elif isinstance(meta, dict):
            column = meta.get("column", metric)
            weight = float(meta.get("weight", 1.0))

        else:
            raise ValueError(f"Invalid metric_map entry for '{metric}': {meta}")

        if column not in df.columns:
            raise ValueError(
                f"Metric column '{column}' not found in dataset columns {list(df.columns)}"
            )

        columns.append(column)
        weights.append(weight)

    # ------------------ Prepare Data ------------------
    data = df[columns].copy()
    data = data.apply(pd.to_numeric, errors="coerce")
    data = data.fillna(data.median(numeric_only=True))

    if data.empty:
        raise ValueError("No numeric data available for ranking")

    # ------------------ Standardize ------------------
    scaler = StandardScaler()
    X = scaler.fit_transform(data)

    weights = np.array(weights)
    X_weighted = X * weights

    n_samples = X_weighted.shape[0]

    # ------------------ Choose K ------------------
    if n_samples < 6:
        k = 1
    else:
        k = min(5, max(2, n_samples // 5))

    # ------------------ Clustering ------------------
    model = KMeans(
        n_clusters=k,
        n_init=10,
        random_state=42
    )

    clusters = model.fit_predict(X_weighted)
    centroids = model.cluster_centers_

    # ------------------ Cluster Strength ------------------
    centroid_scores = centroids.sum(axis=1)

    cluster_rank = {
        cluster_id: rank
        for rank, cluster_id in enumerate(
            np.argsort(-centroid_scores),
            start=1
        )
    }

    # ------------------ Distance to Centroid ------------------
    distances = np.linalg.norm(
        X_weighted - centroids[clusters],
        axis=1
    )

    # ------------------ Final Score ------------------
    scores = (
        pd.Series(clusters).map(cluster_rank).values
        - distances
    )

    result = pd.DataFrame({
        "entity": df[entity_column],
        "cluster": clusters,
        "score": scores
    })

    result = result.sort_values(
        by="score",
        ascending=False
    ).reset_index(drop=True)

    result["rank"] = result.index + 1

    # JSON-safe cleanup
    result = result.replace([np.inf, -np.inf], None)
    result = result.fillna(0)

    return result
