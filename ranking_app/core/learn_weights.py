import pandas as pd
from sklearn.linear_model import LinearRegression

def learn_metric_weights(ranking_df, metrics):
    score_cols = [f"{m}_score" for m in metrics]

    X = ranking_df[score_cols]
    y = ranking_df["final_score"]

    model = LinearRegression()
    model.fit(X, y)

    coefs = abs(model.coef_)
    coef_sum = coefs.sum()

    learned_weights = {}

    for metric, coef in zip(metrics.keys(), coefs):
        learned_weights[metric] = (
            coef / coef_sum if coef_sum > 0 else 0
        )

    return learned_weights
