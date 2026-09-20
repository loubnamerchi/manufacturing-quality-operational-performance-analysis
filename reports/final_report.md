# Final Report: Manufacturing Quality and Operational Performance Analysis

## 1. Executive Summary

This project analyzed 3,240 manufacturing production records (`manufacturing_defect_dataset.csv`, 17 operational variables) to identify the factors most strongly associated with product defects and to benchmark key manufacturing performance indicators. The overall defect rate across the dataset is **84.0%**. Of all variables analyzed, **`MaintenanceHours` and `QualityScore` show the strongest association with defect outcomes**; cost, downtime, supplier quality, worker productivity, energy, and inventory variables show comparatively weak relationships with defects in this dataset. Full findings and recommendations are detailed below and in `reports/insights.md`.

## 2. Business Problem

The manufacturing company is experiencing challenges related to product quality, production efficiency, operational costs, equipment downtime, and resource utilization. Management needs to understand the key factors associated with product defects and operational inefficiencies in order to identify opportunities to improve product quality, reduce production costs and downtime, optimize resource utilization, and improve overall manufacturing performance. See `docs/business_understanding_&_requirements.md` for the full, data-adapted problem statement.

## 3. Business Objectives

Understand manufacturing quality performance, identify factors associated with product defects, analyze production and cost performance, and analyze operational efficiency, supplier quality, worker productivity, energy, and inventory patterns — all scoped to what the actual dataset supports (see `docs/business_understanding_&_requirements.md`, Section 4).

## 4. Data Overview

- **Source file:** `data/raw/manufacturing_defect_dataset.csv`
- **Shape:** 3,240 rows × 17 columns
- **Grain:** one row per production record/batch
- **Data quality:** 0 missing values, 0 duplicate rows, all columns numeric
- **Target variable:** `DefectStatus` (binary: 1 = defective, 0 = not defective), imbalanced at 84.0% / 16.0%
- **Key limitation:** no date, supplier ID, product ID, or plant ID columns exist — see `docs/data_dictionary.md` for the complete column-by-column reference.

## 5. Data Preparation

- **Validation:** required columns, data types, and value ranges were checked (`src/data/validation.py`) before any cleaning occurred.
- **Cleaning:** the dataset required no missing-value imputation or duplicate removal (both were confirmed absent); the full cleaning pipeline (`src/cleaning/`) was still run and documented for reproducibility (`notebooks/03_data_cleaning.ipynb`).
- **Outliers:** investigated with the IQR method but intentionally **not removed**, since they represent plausible operational values rather than data errors (see `docs/methodology.md`, Section 3).
- **Feature engineering:** four features were added — `CostPerUnit`, `QualityCategory`, `DowntimeCategory`, `DefectFlagLabel` (`notebooks/05_feature_engineering.ipynb`, `pipelines/data_pipeline.py`).

## 6. Methodology

A 14-step professional analytics workflow was followed, from business understanding through monitoring and maintenance. Because the dataset is a single flat table with no date or entity identifiers, the core analytical technique used was **correlation analysis combined with bucketed (binned) comparison analysis** rather than time-series or entity-level analysis. Full methodology detail is in `docs/methodology.md`.

## 7. Key KPIs

| KPI | Value |
|---|---|
| Overall Defect Rate | 84.04% |
| Average DefectRate Metric | 2.749 |
| Total Production Volume | 1,777,215 units |
| Average Production Volume | 548.52 units |
| Total Production Cost | $40,250,579.86 |
| Average Production Cost | $12,423.02 |
| Average Cost per Unit | $32.06 |
| Average Quality Score | 80.13 |
| Average Downtime | 2.501% |
| Average Maintenance Hours | 11.48 |
| Average Supplier Quality | 89.83 |
| Average Worker Productivity | 90.04 |
| Total Safety Incidents | 14,877 |
| Average Energy Consumption | 2,988.49 |
| Average Energy Efficiency | 0.2998 |
| Average Inventory Turnover | 6.02 |
| Average Stockout Rate | 0.0509 |

*(Calculated by `src/analysis/kpi_analysis.py::calculate_all_kpis()`; reproducible via `python main.py`.)*

## 8. Key Findings

1. The dataset-wide defect rate is **84.0%** — very high, making defect reduction the highest-leverage opportunity area.
2. **`MaintenanceHours` is the strongest identified defect driver**: defect rate rises from ~70% to ~97% across maintenance-hours buckets.
3. **`QualityScore` is strongly, inversely associated with defects**, consistent with the intuitive relationship between measured quality and defect outcome.
4. Cost, downtime, supplier quality, worker productivity, energy, and inventory variables show weak or inconsistent associations with defect status in this dataset.

## 9. Business Analysis

Full, question-by-question analysis is documented in `notebooks/06_business_analysis.ipynb` and summarized in `reports/insights.md`, covering: overall defect rate, defect drivers, cost impact of defects, downtime vs. production performance, maintenance vs. quality, supplier quality vs. performance, energy efficiency, worker productivity, and inventory/stockout patterns.

## 10. Visualizations

All figures are saved in `reports/figures/`, including:
- Distribution histograms for production volume, cost, quality score, defect rate, downtime, and maintenance hours.
- Boxplots comparing defective vs. non-defective records across key variables.
- A full correlation heatmap.
- Bar charts for defect rate by maintenance-hours range, defect rate by downtime range, and quality score by maintenance-hours range.

Generated by `pipelines/reporting_pipeline.py` and `notebooks/07_visualization.ipynb`.

## 11. Insights

See `reports/insights.md` for the complete, section-by-section insights write-up (executive, quality, defect, production, cost, operational, and resource-utilization insights).

## 12. Recommendations

1. Investigate the `MaintenanceHours`–defect relationship operationally to determine whether it is causal or reactive.
2. Use `QualityScore` as an early-warning monitoring indicator.
3. Deprioritize cost-, downtime-, supplier-quality-, and energy-focused initiatives relative to maintenance and quality-score investigations, based on the weak associations found here.
4. Collect a date field in future data extracts to enable time-trend analysis.
5. Collect supplier/product/equipment identifiers to enable entity-specific analysis.

(Full detail and rationale for each recommendation is in `reports/insights.md`, Section 10.)

## 13. Limitations

- No date/time column — no trend analysis possible.
- No supplier, product, or plant identifiers — no entity-level comparisons possible.
- All relationships found are correlational, not proven causal mechanisms.
- The defect-status target is imbalanced (84.0% / 16.0%).
- Single flat table with no external benchmarking data.

## 14. Conclusion

This project delivered a complete, reproducible analytics pipeline — from raw data validation through cleaning, feature engineering, exploratory and business analysis, visualization, and an interactive dashboard — built entirely on the actual columns present in `manufacturing_defect_dataset.csv`. The headline finding, that maintenance hours and quality score are the strongest identified factors associated with product defects, gives management a concrete, evidence-based starting point for improvement efforts, while the documented limitations make clear what additional data (dates, entity identifiers) would be needed to extend this analysis further.
