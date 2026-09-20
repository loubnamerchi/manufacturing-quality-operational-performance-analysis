

import pandas as pd

from src.utils.helpers import save_dataframe
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_dashboard_dataset(df: pd.DataFrame) -> pd.DataFrame:

    work = df.copy()

    work["DefectLabel"] = work["DefectStatus"].map({0: "Not Defective", 1: "Defective"})

    if "QualityCategory" not in work.columns:
        work["QualityCategory"] = pd.cut(
            work["QualityScore"], bins=[0, 70, 85, 100],
            labels=["Poor", "Average", "Good"], include_lowest=True,
        )

    if "DowntimeCategory" not in work.columns:
        work["DowntimeCategory"] = pd.cut(
            work["DowntimePercentage"], bins=[-0.01, 1.5, 3.5, 100],
            labels=["Low", "Medium", "High"],
        )

    return work


def save_dashboard_dataset(df: pd.DataFrame, path: str) -> None:

    dashboard_df = build_dashboard_dataset(df)
    save_dataframe(dashboard_df, path)
    logger.info(f"Dashboard dataset saved to {path} with shape {dashboard_df.shape}")
