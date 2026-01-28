import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def generate_pca_data(df, entity_column, metric_map, ranked_df):
    # ---- Extract numeric columns used for ranking ----
    columns = []
    for meta in metric_map.values():
        if isinstance(meta, dict) and "column" in meta:
            columns.append(meta["column"])

    columns = list(set(columns))

    # PCA requires at least 2 numeric dimensions
    if len(columns) < 2:
        return {
            "available": False,
            "reason": "Not enough numeric dimensions for PCA"
        }

    # ---- Build PCA matrix ----
    X = df[columns].copy()

    # Convert to numeric safely
    for c in columns:
        X[c] = pd.to_numeric(X[c], errors="coerce")

    X = X.fillna(0.0)

    if X.shape[0] < 2:
        return {
            "available": False,
            "reason": "Not enough rows for PCA"
        }

    # ---- Scale ----
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # ---- PCA ----
    pca = PCA(n_components=2)
    coords = pca.fit_transform(X_scaled)

    # ---- Align with ranking ----
    ranked_entities = ranked_df[entity_column].tolist()

    points = []
    for i, entity in enumerate(ranked_entities):
        points.append({
            "entity": entity,
            "x": float(coords[i, 0]),
            "y": float(coords[i, 1]),
            "rank": int(ranked_df.iloc[i]["rank"])
        })

    return {
        "available": True,
        "points": points,
        "explained_variance": [
            float(pca.explained_variance_ratio_[0]),
            float(pca.explained_variance_ratio_[1])
        ]
    }
