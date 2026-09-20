

from typing import Dict

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def missing_value_report(df: pd.DataFrame) -> pd.DataFrame:

    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df)) * 100
    report = pd.DataFrame({
        "missing_count": missing_count,
        "missing_percentage": missing_pct.round(2),
    }).sort_values("missing_count", ascending=False)
    return report


def duplicate_report(df: pd.DataFrame) -> Dict[str, float]:

    dup_count = int(df.duplicated().sum())
    dup_pct = round((dup_count / len(df)) * 100, 2) if len(df) else 0.0
    return {"duplicate_rows": dup_count, "duplicate_percentage": dup_pct}


def invalid_value_report(df: pd.DataFrame) -> Dict[str, int]:

    non_negative_cols = [
        "ProductionVolume", "ProductionCost", "MaintenanceHours",
        "EnergyConsumption", "AdditiveMaterialCost",
    ]
    issues = {}
    for col in non_negative_cols:
        if col in df.columns:
            count = int((df[col] < 0).sum())
            if count > 0:
                issues[col] = count
    return issues


def data_quality_summary(df: pd.DataFrame) -> Dict[str, object]:

    summary = {
        "shape": df.shape,
        "missing_values": missing_value_report(df),
        "duplicates": duplicate_report(df),
        "invalid_values": invalid_value_report(df),
    }
    logger.info(
        f"Data quality summary — shape={summary['shape']}, "
        f"duplicate_rows={summary['duplicates']['duplicate_rows']}, "
        f"columns_with_missing={int((summary['missing_values']['missing_count'] > 0).sum())}"
    )
    return summary
