def explain_entity(row, metrics):
    explanations = []

    for name, meta in metrics.items():
        score = row[f"{name}_score"]
        weight = meta["weight"]

        if score < weight * 0.4:
            explanations.append(f"{name} is negatively impacting the rank")
        elif score > weight * 0.7:
            explanations.append(f"{name} is a strong positive driver")

    return explanations
