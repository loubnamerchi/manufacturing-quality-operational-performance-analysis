# Manufacturing Quality and Operational Performance Analysis

## 1. Project Overview

An end-to-end, professional data analytics project analyzing 3,240 manufacturing production records to understand the factors associated with product defects and operational performance. The project follows a full 14-step analytics workflow, from business understanding through monitoring and maintenance, and is built entirely on the actual columns present in the uploaded dataset — no data, metrics, or relationships were invented.

## 2. Business Problem

The manufacturing company is experiencing challenges related to product quality, production efficiency, operational costs, equipment downtime, and resource utilization. Management needs to understand the key factors associated with product defects and operational inefficiencies in order to identify opportunities to improve product quality, reduce production costs and downtime, optimize resource utilization, and improve overall manufacturing performance.

See `docs/business_understanding_&_requirements.md` for the complete, data-adapted problem statement, stakeholders, objectives, and business questions.

## 3. Objectives

- Understand overall manufacturing quality and defect performance.
- Identify which operational variables are most strongly associated with product defects.
- Analyze production, cost, downtime, maintenance, supplier-quality, worker-productivity, energy, and inventory patterns supported by the data.
- Deliver KPIs, visualizations, an interactive dashboard, and a written report.

## 4. Dataset Description

- **File:** `data/raw/manufacturing_defect_dataset.csv`
- **Source:** *Predicting Manufacturing Defects Dataset*, created by **Rabie El Kharoua**, published on Kaggle under **CC BY 4.0**. This is a **synthetic** dataset generated for educational purposes — it does not describe a real manufacturing plant. Please credit the original author if you reuse this dataset or work derived from it.
- **Shape:** 3,240 rows × 17 columns.
- **Quality:** 0 missing values, 0 duplicate rows, all columns numeric.
- **Target:** `DefectStatus` (1 = High Defects, 0 = Low Defects), 84.0% defective / 16.0% not defective — intentionally imbalanced per the source data card, which recommends rebalancing before any machine learning use (not applicable here, as this is a descriptive/diagnostic project, not a predictive-modeling one).
- **Grain caveat:** some columns are defined at different native time cadences (`ProductionVolume` per day, `MaintenanceHours` per week, `SafetyIncidents` per month) despite sharing a row — see `docs/data_dictionary.md` for the full explanation.
- **Limitations:** no date, supplier ID, product ID, or plant ID columns — see `docs/data_dictionary.md` for the full column reference and limitations.

## 5. Project Architecture

```
manufacturing-quality-operational-performance-analysis/
├── main.py                  # Single entry point coordinating all pipelines
├── config/config.yaml       # Central configuration (paths, thresholds)
├── data/                    # raw / interim / processed / external datasets
├── docs/                    # Business requirements, data dictionary, methodology
├── notebooks/                # 7 notebooks covering the full workflow
├── pipelines/                # data_pipeline.py, analysis_pipeline.py, reporting_pipeline.py
├── src/                     # Reusable, documented Python modules
├── sql/                     # Exploration, cleaning, and business-analysis SQL
├── dashboards/               # Streamlit app + Power BI / Tableau / Excel guides
├── reports/                  # insights.md, final_report.md, figures/
└── tests/                    # Automated data-quality tests
```

## 6. Project Workflow

1. Business Problem → 2. Requirements Gathering → 3. Data Collection → 4. Data Understanding → 5. Data Cleaning → 6. Exploratory Data Analysis → 7. Feature Engineering → 8. Business Analysis → 9. Visualization → 10. Interactive Dashboard → 11. Insights & Recommendations → 12. Reporting → 13. Deployment & Automation → 14. Monitoring & Maintenance.

Full detail: `docs/methodology.md`.

## 7. Technologies Used

Python (pandas, numpy, matplotlib, seaborn), PyYAML, Streamlit, pytest, Jupyter/nbformat, SQL (ANSI-standard, documented for PostgreSQL/MySQL/SQLite).

## 8. Installation

```bash
git clone <repository-url>
cd manufacturing-quality-operational-performance-analysis
pip install -r requirements.txt
```

## 9. Requirements

See `requirements.txt`. Core packages: `pandas`, `numpy`, `matplotlib`, `seaborn`, `PyYAML`, `streamlit`, `pytest`, `jupyter`, `nbformat`.

## 10. How to Run

Run the complete pipeline (data → analysis → reporting) with one command from the project root:

```bash
python main.py
```

This produces `data/interim/manufacturing_interim.csv`, `data/processed/manufacturing_processed.csv`, `data/processed/dashboard_data.csv`, PNG charts in `reports/figures/`, and a full run log in `logs/pipeline.log`.

## 11. Pipeline Execution

Each pipeline can also be run independently:

```bash
python pipelines/data_pipeline.py       # load -> validate -> clean -> transform -> save
python pipelines/analysis_pipeline.py   # KPIs, business aggregations, dashboard data
python pipelines/reporting_pipeline.py  # generate and save all report figures
```

## 12. Notebook Workflow

Run notebooks in order for the full narrative:

1. `01_initial_inspection.ipynb`
2. `02_data_understanding.ipynb`
3. `03_data_cleaning.ipynb`
4. `04_exploratory_data_analysis.ipynb`
5. `05_feature_engineering.ipynb`
6. `06_business_analysis.ipynb`
7. `07_visualization.ipynb`

All notebooks are pre-executed and contain real outputs from the actual dataset.

## 13. Dashboard Information

- **Streamlit (functional):** `streamlit run dashboards/streamlit/app.py` — interactive KPI cards, filters, and charts built on `data/processed/dashboard_data.csv`.
- **Power BI:** implementation guide in `dashboards/powerbi/README.md`.
- **Tableau:** implementation guide in `dashboards/tableau/README.md`.
- **Excel:** implementation guide in `dashboards/excel/README.md`.

## 14. Key KPIs

Overall Defect Rate (84.04%), Average Production Cost ($12,423.02), Average Quality Score (80.13), Average Maintenance Hours (11.48), Average Downtime (2.50%), and more — full table in `reports/final_report.md`, Section 7.

## 15. Project Outputs

- Cleaned and processed datasets (`data/interim/`, `data/processed/`)
- 17+ PNG charts (`reports/figures/`)
- Written reports (`reports/insights.md`, `reports/final_report.md`)
- Interactive Streamlit dashboard and BI-tool documentation (`dashboards/`)
- Automated test suite (`tests/test_data_quality.py`)

## 16. Project Structure

See Section 5 above and the full repository tree for the complete file listing.

## 17. Limitations

- No date/time column → no time-trend analysis possible.
- No supplier, product, or plant identifiers → no entity-level comparisons possible.
- All relationships found are correlational, not proven causal.
- The defect-status target is imbalanced (84.0% / 16.0%).

Full detail: `reports/final_report.md`, Section 13.

## 18. Future Improvements

- Add a production date column to enable time-trend and monitoring analysis.
- Add supplier/product/equipment identifiers to enable entity-level analysis.
- Expand automated testing to include pipeline-level integration tests.
- Package the project for CI/CD (e.g. GitHub Actions running `pytest` and `python main.py` on every commit).
- If extending this project toward predictive modeling, rebalance `DefectStatus` first, per the source data card's explicit recommendation.

## 19. Dataset Citation

This project uses the *Predicting Manufacturing Defects Dataset*, created by **Rabie El Kharoua** and distributed on Kaggle under a **CC BY 4.0** license. The dataset is synthetic and was generated for educational purposes. If you reuse this dataset, or an analysis substantially derived from it, please credit the original author per the license terms.
