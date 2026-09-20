
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def count_duplicates(df: pd.DataFrame) -> int:

    return int(df.duplicated().sum())


def remove_duplicates(df: pd.DataFrame, keep: str = "first") -> pd.DataFrame:

    before_count = count_duplicates(df)
    df_clean = df.drop_duplicates(keep=keep).reset_index(drop=True)
    logger.info(f"Removed {before_count} duplicate row(s) (keep='{keep}').")
    return df_clean
