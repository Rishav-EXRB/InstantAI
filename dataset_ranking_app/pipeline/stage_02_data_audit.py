import pandas as pd
from dataclasses import dataclass
from typing import Union


@dataclass
class DatasetAudit:
    df: pd.DataFrame
    columns: list
    numeric_columns: list
    text_columns: list


def audit_dataset(source: Union[str, pd.DataFrame]) -> DatasetAudit:
    """
    Accepts either:
    - file path (str)
    - pandas DataFrame

    This prevents accidental type errors across pipeline stages.
    """

    # ---------- LOAD DATA ----------
    if isinstance(source, pd.DataFrame):
        df = source.copy()

    elif isinstance(source, str):
        try:
            df = pd.read_csv(source, encoding="utf-8")
        except Exception:
            df = pd.read_csv(source, encoding="latin1")

    else:
        raise TypeError(
            f"audit_dataset expected str or DataFrame, got {type(source)}"
        )

    # ---------- VALIDATION ----------
    if df.empty or len(df.columns) == 0:
        raise ValueError("Uploaded dataset is empty or invalid")

    # ---------- COLUMN CLASSIFICATION ----------
    numeric_columns = []
    text_columns = []

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            numeric_columns.append(col)
        else:
            text_columns.append(col)

    return DatasetAudit(
        df=df,
        columns=list(df.columns),
        numeric_columns=numeric_columns,
        text_columns=text_columns
    )
