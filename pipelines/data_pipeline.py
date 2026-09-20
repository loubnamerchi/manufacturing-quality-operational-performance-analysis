
import pandas as pd

from src.data.load_data import load_csv
from src.data.validation import run_full_validation
from src.data.data_quality import data_quality_summary
from src.cleaning.clean_data import clean_dataset
from src.utils.config import load_config, resolve_path
from src.utils.helpers import save_dataframe
from src.utils.logger import get_logger

logger = get_logger(__name__)


def engineer_features(df: pd.DataFrame, config: dict) -> pd.DataFrame:

    work = df.copy()
    bands = config["analysis"]

    work["CostPerUnit"] = (work["ProductionCost"] / work["ProductionVolume"].replace(0, pd.NA)).round(2)

    q_bands = bands["quality_bands"]
    work["QualityCategory"] = pd.cut(
        work["QualityScore"],
        bins=[-float("inf"), q_bands["poor_max"], q_bands["average_max"], float("inf")],
        labels=["Poor", "Average", "Good"],
    )

    d_bands = bands["downtime_bands"]
    work["DowntimeCategory"] = pd.cut(
        work["DowntimePercentage"],
        bins=[-float("inf"), d_bands["low_max"], d_bands["medium_max"], float("inf")],
        labels=["Low", "Medium", "High"],
    )

    work["DefectFlagLabel"] = work["DefectStatus"].map({0: "Not Defective", 1: "Defective"})

    logger.info("Feature engineering complete: added CostPerUnit, QualityCategory, "
                "DowntimeCategory, DefectFlagLabel.")
    return work


def run_data_pipeline(config: dict = None) -> pd.DataFrame:

    config = config or load_config()

    logger.info("=== DATA PIPELINE: START ===")

    # Step 1: LOAD
    raw_path = resolve_path(config["data"]["raw_path"])
    df_raw = load_csv(raw_path)

    # Step 2: VALIDATE
    validation_report = run_full_validation(df_raw)
    dq_summary = data_quality_summary(df_raw)
    logger.info(f"Validation report: {validation_report}")

    # Step 3: CLEAN (checkpoint saved to data/interim/)
    df_clean = clean_dataset(df_raw)
    interim_path = resolve_path(config["data"]["interim_path"])
    save_dataframe(df_clean, interim_path)
    logger.info(f"Interim cleaned dataset saved to {interim_path}")

    # Step 4: TRANSFORM (feature engineering)
    df_processed = engineer_features(df_clean, config)

    # Step 5: SAVE final processed dataset
    processed_path = resolve_path(config["data"]["processed_path"])
    save_dataframe(df_processed, processed_path)
    logger.info(f"Processed dataset saved to {processed_path} with shape {df_processed.shape}")

    logger.info("=== DATA PIPELINE: COMPLETE ===")
    return df_processed


if __name__ == "__main__":
    run_data_pipeline()
