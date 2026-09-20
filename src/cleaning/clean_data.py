
import pandas as pd

from src.cleaning.missing_values import fill_missing_numeric, missing_value_summary
from src.cleaning.duplicates import remove_duplicates, count_duplicates
from src.utils.logger import get_logger

logger = get_logger(__name__)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    return df


def enforce_numeric_types(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:

    logger.info("Starting data cleaning process...")

    df = standardize_column_names(df)
    df = enforce_numeric_types(df)

    missing_before = missing_value_summary(df)
    duplicates_before = count_duplicates(df)
    df = remove_duplicates(df)

    logger.info(
        f"Cleaning complete. Missing-value decision: {missing_before['decision']} "
        f"| Duplicate rows removed: {duplicates_before}"
    )

    return df
