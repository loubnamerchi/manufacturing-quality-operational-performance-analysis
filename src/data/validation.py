

from typing import List, Dict

import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)

# The columns that MUST be present in the raw manufacturing dataset for the
# rest of the pipeline to work correctly.
REQUIRED_COLUMNS: List[str] = [
    "ProductionVolume",
    "ProductionCost",
    "SupplierQuality",
    "DeliveryDelay",
    "DefectRate",
    "QualityScore",
    "MaintenanceHours",
    "DowntimePercentage",
    "InventoryTurnover",
    "StockoutRate",
    "WorkerProductivity",
    "SafetyIncidents",
    "EnergyConsumption",
    "EnergyEfficiency",
    "AdditiveProcessTime",
    "AdditiveMaterialCost",
    "DefectStatus",
]

# Columns that must be numeric for downstream statistical analysis.
NUMERIC_COLUMNS: List[str] = REQUIRED_COLUMNS


def validate_required_columns(df: pd.DataFrame, required: List[str] = None) -> List[str]:

    required = required or REQUIRED_COLUMNS
    missing = [col for col in required if col not in df.columns]
    if missing:
        logger.warning(f"Missing required columns: {missing}")
    else:
        logger.info("All required columns are present.")
    return missing


def validate_numeric_columns(df: pd.DataFrame, columns: List[str] = None) -> List[str]:

    columns = columns or NUMERIC_COLUMNS
    non_numeric = [
        col for col in columns
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col])
    ]
    if non_numeric:
        logger.warning(f"Non-numeric columns detected where numeric was expected: {non_numeric}")
    return non_numeric


def validate_value_ranges(df: pd.DataFrame) -> Dict[str, int]:

    issues: Dict[str, int] = {}

    non_negative_cols = [
        "ProductionVolume", "ProductionCost", "MaintenanceHours",
        "EnergyConsumption", "AdditiveMaterialCost", "DefectRate",
        "DowntimePercentage", "StockoutRate",
    ]
    for col in non_negative_cols:
        if col in df.columns:
            invalid_count = int((df[col] < 0).sum())
            if invalid_count > 0:
                issues[col] = invalid_count

    if "DefectStatus" in df.columns:
        invalid_status = int(~df["DefectStatus"].isin([0, 1]).sum())
        if invalid_status > 0:
            issues["DefectStatus"] = invalid_status

    if issues:
        logger.warning(f"Value range validation issues found: {issues}")
    else:
        logger.info("Value range validation passed: no invalid values detected.")

    return issues


def run_full_validation(df: pd.DataFrame) -> Dict[str, object]:

    report = {
        "missing_columns": validate_required_columns(df),
        "non_numeric_columns": validate_numeric_columns(df),
        "value_range_issues": validate_value_ranges(df),
    }
    return report
