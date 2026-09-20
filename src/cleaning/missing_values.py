

from typing import Dict

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def report_missing_values(df: pd.DataFrame) -> pd.Series:

    return df.isnull().sum()


def fill_missing_numeric(df: pd.DataFrame, strategy: str = "median") -> pd.DataFrame:

    df = df.copy()
    numeric_cols = df.select_dtypes(include="number").columns

    for col in numeric_cols:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            fill_value = df[col].median() if strategy == "median" else df[col].mean()
            df[col] = df[col].fillna(fill_value)
            logger.info(f"Filled {missing_count} missing values in '{col}' using {strategy}={fill_value:.4f}")

    return df


def drop_rows_with_missing(df: pd.DataFrame, subset=None) -> pd.DataFrame:

    before = len(df)
    df_clean = df.dropna(subset=subset)
    dropped = before - len(df_clean)
    if dropped > 0:
        logger.info(f"Dropped {dropped} rows due to missing values (subset={subset}).")
    return df_clean


def missing_value_summary(df: pd.DataFrame) -> Dict[str, object]:

    df_clean = df.copy()

    missing = report_missing_values(df_clean)
    total_missing_before = int(missing.sum())
    columns_affected = int((missing > 0).sum())
    imputed_columns = []
    dropped_columns = []
    skipped_columns = []
    
    for col in df.columns:

        missing_count = int(missing[col])
        if missing_count == 0:
            continue

        missing_percentage = (missing_count / len(df)) * 100

        if missing_percentage < 50:
            if pd.api.types.is_numeric_dtype(df_clean[col]):
                df_clean = fill_missing_numeric(
                    df_clean,
                    columns=[col],
                    strategy="median"
                )
                imputed_columns.append(col)
                logger.info(
                    f"'{col}': {missing_percentage:.2f}% missing "
                    f"-> median imputation."
                )
            else:
                skipped_columns.append(col)
                logger.warning(
                    f"'{col}': {missing_percentage:.2f}% missing. "
                    f"Non-numeric column was not automatically imputed."
                )
        # 50% or more missing
        else:
            df_clean = df_clean.drop(columns=[col])
            dropped_columns.append(col)
            logger.info(
                f"'{col}': {missing_percentage:.2f}% missing "
                f"-> column dropped."
            )
    total_missing_after = int(df_clean.isnull().sum().sum())
    if total_missing_before == 0:
        decision = (
            "No missing values were found. "
            "No missing-value handling was necessary."
        )
    else:
        decision = (
            f"Missing values were handled using a 50% threshold. "
            f"Numeric columns with less than 50% missing values "
            f"were imputed using the median. Columns with 50% or "
            f"more missing values were dropped."
        )
    return {
        "dataframe": df_clean,
        "total_missing_before": total_missing_before,
        "total_missing_after": total_missing_after,
        "columns_affected": columns_affected,
        "imputed_columns": imputed_columns,
        "dropped_columns": dropped_columns,
        "skipped_columns": skipped_columns,
        "decision": decision,
    }