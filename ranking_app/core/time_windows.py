import pandas as pd

def slice_time_window(df, start_date, end_date):
    start_ts = pd.to_datetime(start_date)
    end_ts = pd.to_datetime(end_date)

    mask = (df["order_date"] >= start_ts) & (df["order_date"] <= end_ts)
    return df.loc[mask].copy()
