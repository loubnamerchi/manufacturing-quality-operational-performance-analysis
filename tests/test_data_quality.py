

import sys
from pathlib import Path

import pandas as pd
import pytest

# Ensure the project root is importable when running `pytest` from any
# working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.data.load_data import load_csv
from src.data.validation import validate_required_columns, validate_value_ranges, REQUIRED_COLUMNS
from src.cleaning.duplicates import count_duplicates
from src.cleaning.clean_data import clean_dataset


RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "manufacturing_defect_dataset.csv"


@pytest.fixture(scope="module")
def raw_df() -> pd.DataFrame:
    """Load the raw manufacturing dataset once for all tests in this module."""
    return load_csv(RAW_DATA_PATH)


def test_raw_file_exists():
    """The raw dataset file must exist at the expected path."""
    assert RAW_DATA_PATH.exists(), f"Raw data file not found at {RAW_DATA_PATH}"


def test_required_columns_present(raw_df):
    """All 17 expected manufacturing columns must be present in the raw data."""
    missing = validate_required_columns(raw_df, REQUIRED_COLUMNS)
    assert missing == [], f"Missing required columns: {missing}"


def test_dataset_is_not_empty(raw_df):
    """The dataset must contain at least one row and all expected columns."""
    assert len(raw_df) > 0, "Dataset has zero rows."
    assert len(raw_df.columns) == len(REQUIRED_COLUMNS), (
        f"Expected {len(REQUIRED_COLUMNS)} columns, found {len(raw_df.columns)}."
    )


def test_no_missing_values(raw_df):

    total_missing = int(raw_df.isnull().sum().sum())
    assert total_missing == 0, f"Found {total_missing} missing values in raw dataset."


def test_no_duplicate_rows(raw_df):
    """The raw dataset is known to have zero duplicate rows."""
    dup_count = count_duplicates(raw_df)
    assert dup_count == 0, f"Found {dup_count} duplicate rows in raw dataset."


def test_defect_status_is_binary(raw_df):
    """DefectStatus must only ever contain the values 0 or 1."""
    invalid_values = set(raw_df["DefectStatus"].unique()) - {0, 1}
    assert not invalid_values, f"DefectStatus contains invalid values: {invalid_values}"


def test_no_negative_values_in_physical_columns(raw_df):

    issues = validate_value_ranges(raw_df)
    assert issues == {}, f"Found invalid (e.g. negative) values: {issues}"


def test_numeric_columns_are_numeric(raw_df):
    """Every required column must have a numeric dtype."""
    non_numeric = [
        col for col in REQUIRED_COLUMNS
        if not pd.api.types.is_numeric_dtype(raw_df[col])
    ]
    assert non_numeric == [], f"Non-numeric columns found: {non_numeric}"


def test_clean_dataset_preserves_row_count_when_no_duplicates(raw_df):

    cleaned = clean_dataset(raw_df)
    assert len(cleaned) == len(raw_df), (
        "clean_dataset() changed the row count even though the raw data "
        "has no duplicates or missing values."
    )


def test_production_volume_within_expected_range(raw_df):

    assert raw_df["ProductionVolume"].min() >= 0
    assert raw_df["ProductionVolume"].max() <= 100000


def test_quality_score_within_0_to_100(raw_df):
    """QualityScore should logically fall within a 0-100 scale."""
    assert raw_df["QualityScore"].min() >= 0
    assert raw_df["QualityScore"].max() <= 100
