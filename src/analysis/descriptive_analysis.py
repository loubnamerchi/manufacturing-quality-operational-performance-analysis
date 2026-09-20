
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def describe_numeric(df: pd.DataFrame) -> pd.DataFrame:

    return df.describe().T


def summary_by_defect_status(df: pd.DataFrame, target_column: str = "DefectStatus") -> pd.DataFrame:

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if target_column in numeric_cols:
        numeric_cols.remove(target_column)

    summary = df.groupby(target_column)[numeric_cols].mean().T
    return summary


def value_distribution(df: pd.DataFrame, column: str) -> pd.DataFrame:

    counts = df[column].value_counts().sort_index()
    pct = (counts / len(df) * 100).round(2)
    return pd.DataFrame({"count": counts, "percentage": pct})
