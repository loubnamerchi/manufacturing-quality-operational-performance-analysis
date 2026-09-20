

from typing import List

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:

    return df.select_dtypes(include="number").corr()


def top_correlated_with(df: pd.DataFrame, target: str, n: int = 10) -> pd.Series:

    corr = df.select_dtypes(include="number").corr()[target].drop(target)
    ranked = corr.reindex(corr.abs().sort_values(ascending=False).index)
    return ranked.head(n)


def group_means_by_bins(df: pd.DataFrame, value_col: str, bin_col: str, bins: int = 5) -> pd.DataFrame:

    df = df.copy()
    df["_bucket"] = pd.cut(df[bin_col], bins=bins)
    result = df.groupby("_bucket", observed=True)[value_col].mean().reset_index()
    result.columns = [f"{bin_col}_range", f"mean_{value_col}"]
    return result


def numeric_columns_excluding(df: pd.DataFrame, exclude: List[str]) -> List[str]:

    return [c for c in df.select_dtypes(include="number").columns if c not in exclude]
