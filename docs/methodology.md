# Methodology

This document explains the complete analytical methodology and workflow used in the Manufacturing Quality and Operational Performance Analysis project, and documents the project's monitoring and maintenance approach.

## 1. Workflow Overview

The project follows a 14-step professional data analytics workflow, adapted to the realities of the actual dataset (a single flat CSV file with no date, supplier, or product identifiers):

| Step | Description | Where implemented |
|---|---|---|
| 1. Business Problem | Define and refine the business problem using the actual data | `docs/business_understanding_&_requirements.md` |
| 2. Requirements Gathering | Stakeholders, objectives, KPIs, business questions | `docs/business_understanding_&_requirements.md` |
| 3. Data Collection | Document data source and store raw data unchanged | `data/raw/`, `docs/data_dictionary.md` |
| 4. Data Understanding | Inspect shape, types, missing values, duplicates, distributions | `notebooks/01_initial_inspection.ipynb`, `notebooks/02_data_understanding.ipynb` |
| 5. Data Cleaning | Validate, clean, document cleaning decisions | `notebooks/03_data_cleaning.ipynb`, `src/cleaning/` |
| 6. Exploratory Data Analysis | Distributions, correlations, comparisons | `notebooks/04_exploratory_data_analysis.ipynb`, `src/analysis/exploratory_analysis.py` |
| 7. Feature Engineering | Create `CostPerUnit`, `QualityCategory`, `DowntimeCategory` | `notebooks/05_feature_engineering.ipynb`, `pipelines/data_pipeline.py` |
| 8. Business Analysis | Answer the defined business questions with real evidence | `notebooks/06_business_analysis.ipynb`, `src/analysis/business_analysis.py` |
| 9. Visualization | Professional charts for every analysis | `notebooks/07_visualization.ipynb`, `src/visualization/charts.py` |
| 10. Interactive Dashboard | Streamlit app + BI tool documentation | `dashboards/` |
| 11. Insights & Recommendations | Business-facing interpretation of findings | `reports/insights.md` |
| 12. Reporting | Consolidated final report | `reports/final_report.md` |
| 13. Deployment & Automation | Modular, reproducible pipeline | `pipelines/`, `main.py` |
| 14. Monitoring & Maintenance | Logging, tests, data quality checks | `src/utils/logger.py`, `tests/test_data_quality.py`, Section 4 below |

The workflow is designed to be **iterative**: for example, if EDA (step 6) reveals a data quality issue not caught in step 5, the analyst returns to the cleaning step, updates the cleaning functions, and re-runs the pipeline (`python main.py`) to propagate the fix through every downstream output.

## 2. Analytical Approach

Because the dataset is a single flat table of 3,240 records with 16 numeric feature columns and one binary target (`DefectStatus`), the analytical approach centers on two complementary techniques:

1. **Correlation analysis** — computing Pearson correlation between every numeric feature and the target (`DefectStatus`, `DefectRate`) to rank which variables move together with defect outcomes.
2. **Bucketed comparison analysis** — since there are no natural categories in the data, continuous variables (e.g. `MaintenanceHours`, `SupplierQuality`, `DowntimePercentage`) are split into equal-width buckets, and the defect rate / quality score is compared across buckets. This turns continuous relationships into business-readable tables and charts (see `src/analysis/business_analysis.py`).

No machine learning model is built, per the project brief ("this is primarily a DATA ANALYSIS project") — the goal is descriptive and diagnostic analysis, not predictive modeling.

## 3. Data Cleaning Methodology

The raw dataset was found, through direct inspection in `notebooks/01_initial_inspection.ipynb`, to already be clean:

- 0 missing values across all 17 columns.
- 0 duplicate rows.
- 0 negative values in columns that cannot logically be negative.
- All columns already stored as numeric types.

Despite this, a full cleaning pipeline (`src/cleaning/`) was still implemented and is run on every pipeline execution, because:
- It documents, in code, exactly what WOULD happen if a future data refresh introduced missing values, duplicates, or invalid values.
- It is unit-tested (`tests/test_data_quality.py`) so any regression in data quality is caught automatically.

**Outlier handling policy:** outliers were investigated using the IQR method (`src/cleaning/outliers.py`) but were **not automatically removed**. Given that every numeric column in this dataset represents a real operational measurement (cost, hours, percentages, rates) with a plausible business range, values outside the IQR bounds are more likely to reflect genuine operational variation (e.g. an unusually long maintenance event) than data entry errors. Automatically deleting them could remove exactly the signal a defect-driver analysis is looking for.

## 4. Monitoring and Maintenance

- **Logging:** every pipeline run writes structured, timestamped log entries to `logs/pipeline.log` via `src/utils/logger.py`, recording each pipeline stage, dataset shapes, and any validation warnings.
- **Data quality checks:** `src/data/validation.py` and `src/data/data_quality.py` run automatically at the start of every `data_pipeline.py` execution, checking required columns, data types, and value ranges before any cleaning or analysis proceeds.
- **Automated tests:** `tests/test_data_quality.py` contains 11 tests covering schema, missing values, duplicates, value ranges, and cleaning-pipeline behavior. These should be run (`pytest tests/`) after every data refresh, and ideally wired into a CI pipeline if the project is version-controlled in a shared repository.
- **Error handling:** pipeline functions raise clear exceptions (e.g. `FileNotFoundError` in `src/data/load_data.py`) rather than failing silently, so problems surface immediately rather than producing misleading downstream results.
- **Data refresh considerations:** if a new extract of the manufacturing dataset becomes available, replace `data/raw/manufacturing_defect_dataset.csv` with the new file (keeping the same column names), then run `pytest tests/test_data_quality.py` before running `python main.py`, so any schema drift is caught before the full pipeline executes.
