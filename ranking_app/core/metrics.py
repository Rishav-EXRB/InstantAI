def apply_derived_metrics(df, derived_metrics):
    for name, meta in derived_metrics.items():
        expr = meta["formula"]
        df[name] = df.eval(expr)

    df.replace([float("inf"), -float("inf")], 0, inplace=True)
    df.fillna(0, inplace=True)

    return df
