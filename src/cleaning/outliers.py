
from typing import Dict

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def iqr_bounds(series: pd.Series, multiplier: float = 1.5) -> Dict[str, float]:

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return {
        "q1": q1,
        "q3": q3,
        "iqr": iqr,
        "lower_bound": q1 - multiplier * iqr,
        "upper_bound": q3 + multiplier * iqr,
    }


def iqr_outlier_report(df: pd.DataFrame, columns=None, multiplier: float = 1.5) -> pd.DataFrame:

    columns = columns or df.select_dtypes(include="number").columns.tolist()
    rows = []
    for col in columns:
        bounds = iqr_bounds(df[col], multiplier)
        outlier_mask = (df[col] < bounds["lower_bound"]) | (df[col] > bounds["upper_bound"])
        outlier_count = int(outlier_mask.sum())
        rows.append({
            "column": col,
            "outlier_count": outlier_count,
            "outlier_percentage": round((outlier_count / len(df)) * 100, 2) if len(df) else 0.0,
            "lower_bound": round(bounds["lower_bound"], 4),
            "upper_bound": round(bounds["upper_bound"], 4),
        })

    report = pd.DataFrame(rows).set_index("column").sort_values("outlier_count", ascending=False)
    logger.info(f"Outlier report generated for {len(columns)} numeric column(s).")
    return report


def flag_outliers(df: pd.DataFrame, column: str, multiplier: float = 1.5) -> pd.DataFrame:

    df = df.copy()
    bounds = iqr_bounds(df[column], multiplier)
    flag_col = f"{column}_is_outlier"
    df[flag_col] = (df[column] < bounds["lower_bound"]) | (df[column] > bounds["upper_bound"])
    return df
