def min_max(series, inverse=False):
    if series.max() == series.min():
        return 0.5
    if inverse:
        return (series.max() - series) / (series.max() - series.min())
    return (series - series.min()) / (series.max() - series.min())
