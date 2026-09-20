# Data Dictionary

**Dataset:** `manufacturing_defect_dataset.csv`
**Location:** `data/raw/manufacturing_defect_dataset.csv`
**Shape:** 3,240 rows × 17 columns
**Source:** This is a **synthetic** dataset created for educational purposes by **Rabie El Kharoua**, published on Kaggle under a **CC BY 4.0** license. It has no real-world manufacturing plant behind it. Per the license, any use of this dataset or the analysis derived from it should credit the original author.
**Grain:** Each row is a single synthetic record combining several manufacturing metrics. **Important caveat (see Limitations below): several of these metrics are defined at different native time cadences (per day, per week, per month) but are packed into the same row**, so "one row = one directly comparable snapshot" should not be over-interpreted.
**Missing values:** None (0 across all columns).
**Duplicate rows:** None (0 fully duplicated rows).

| Column | Official Description (per source data card) | Data Type | Official Range | Example Values (this file) | Analytical Role | Missing Values |
|---|---|---|---|---|---|---|
| `ProductionVolume` | Number of units produced **per day** | Integer | 100 – 1,000 units/day | 202, 535, 960 | Feature / production metric | 0 |
| `ProductionCost` | Cost incurred for production **per day** | Float ($) | $5,000 – $20,000 | 13175.40, 19770.05 | Feature / cost metric | 0 |
| `SupplierQuality` | Quality rating of suppliers | Float (%) | 80% – 100% | 86.65, 82.13 | Feature / supplier metric | 0 |
| `DeliveryDelay` | Average delay in delivery | Integer (days) | 0 – 5 days | 0, 1, 4 | Feature / operational metric | 0 |
| `DefectRate` | **Defects per thousand units produced** | Float | 0.5 – 5.0 | 3.12, 0.82 | Feature / quality metric | 0 |
| `QualityScore` | Overall quality assessment | Float (%) | 60% – 100% | 63.46, 83.70 | Feature / quality metric | 0 |
| `MaintenanceHours` | Hours spent on maintenance **per week** | Integer | 0 – 24 hours | 9, 20, 1 | Feature / maintenance metric | 0 |
| `DowntimePercentage` | Percentage of production downtime | Float (%) | 0% – 5% | 0.052, 4.91 | Feature / operational metric | 0 |
| `InventoryTurnover` | Ratio of inventory turnover | Float | 2 – 10 | 8.63, 9.30 | Feature / inventory metric | 0 |
| `StockoutRate` | Rate of inventory stockouts | Float (%) | 0% – 10% | 0.081, 0.038 (stored as fraction, e.g. 0.081 = 8.1%) | Feature / inventory metric | 0 |
| `WorkerProductivity` | Productivity level of the workforce | Float (%) | 80% – 100% | 85.04, 99.66 | Feature / productivity metric | 0 |
| `SafetyIncidents` | Number of safety incidents **per month** | Integer | 0 – 10 incidents | 0, 7, 2 | Feature / safety metric | 0 |
| `EnergyConsumption` | Energy consumed in **kWh** | Float | 1,000 – 5,000 kWh | 2419.62, 3915.57 | Feature / energy metric | 0 |
| `EnergyEfficiency` | Efficiency factor of energy usage | Float | 0.1 – 0.5 | 0.469, 0.119 | Feature / energy metric | 0 |
| `AdditiveProcessTime` | Time taken for additive manufacturing, in **hours** | Float (hours) | 1 – 10 hours | 5.55, 9.08 | Feature / process metric | 0 |
| `AdditiveMaterialCost` | Cost of additive materials **per unit** | Float ($) | $100 – $500 | 236.44, 353.96 | Feature / cost metric | 0 |
| `DefectStatus` | **Target variable.** Predicted defect status: 0 = Low Defects, 1 = High Defects | Binary (int64) | 0 or 1 | 0, 1 | Target / label | 0 |

*Ranges in the "Official Range" column are taken directly from the source data card, not re-derived from this specific file; the "Example Values" column shows actual values observed in `manufacturing_defect_dataset.csv`, which fall within those official ranges.*

## Important correction from an earlier version of this document

An earlier draft of this data dictionary marked the units of `AdditiveProcessTime` and `EnergyConsumption` as "unspecified" or "unconfirmed," because they could not be determined from the CSV file alone. The source data card (reproduced above) confirms these explicitly: `AdditiveProcessTime` is in **hours**, and `EnergyConsumption` is in **kWh**. This table has been corrected accordingly. This is a reminder that this project's early "unit not specified" notes reflected the limits of what the CSV alone could prove — not a claim that no such information existed anywhere.

## Engineered Columns (created in `pipelines/data_pipeline.py` / `notebooks/05_feature_engineering.ipynb`)

| Column | Description | Formula | Data Type |
|---|---|---|---|
| `CostPerUnit` | Production cost normalized per unit produced | `ProductionCost / ProductionVolume` | float64 |
| `QualityCategory` | Categorical band derived from `QualityScore` | `Poor` (≤70), `Average` (70–85), `Good` (>85) | category |
| `DowntimeCategory` | Categorical band derived from `DowntimePercentage` | `Low` (≤1.5%), `Medium` (1.5–3.5%), `High` (>3.5%) | category |
| `DefectFlagLabel` | Human-readable version of `DefectStatus` | `0 → "Not Defective"`, `1 → "Defective"` | object |

## Known Dataset Limitations

- **Synthetic data.** Per the source data card, this dataset was generated for educational purposes and does not describe a real manufacturing plant. All findings in this project describe patterns *within this synthetic dataset*, not real-world manufacturing behavior.
- **Mixed time granularity within one row.** The source data card defines `ProductionVolume` as a **per-day** metric, `MaintenanceHours` as a **per-week** metric, and `SafetyIncidents` as a **per-month** metric — three different native cadences bundled into a single row alongside cross-sectional metrics like `QualityScore` and `SupplierQuality`. This means a row should not be read as "everything that happened to one batch on one day"; it is better understood as a synthetic combination of metrics sampled at different cadences. No aggregation or re-scaling across these cadences is attempted anywhere in this project, and this caveat should be kept in mind whenever comparing these three columns directly against each other.
- **No date/time column.** Despite the metrics above having day/week/month cadences *by definition*, there is no actual date or timestamp column in the data, so it is still not possible to know *which* day, week, or month a given row's `ProductionVolume`, `MaintenanceHours`, or `SafetyIncidents` value refers to, or to build any real time-trend analysis. `AdditiveProcessTime` also contains "time" in its name but is a **duration** (hours), not a calendar date — it does not resolve this limitation.
- **No supplier ID, product ID, plant ID, or equipment ID.** `SupplierQuality` is a continuous per-record score rather than a link to a specific, named supplier, so supplier-level comparisons (e.g. "Supplier A vs. Supplier B") cannot be performed — only supplier-quality-*level* analysis (e.g. "records with SupplierQuality 80–85 vs. 95–100").
- **No categorical/text columns** other than the derived bands listed above — all 17 raw columns are numeric.
- **Single flat table.** There is only one dataset (no separate maintenance log, inventory ledger, or supplier master table to join against), so all analysis is performed on this one table.
- **`DefectStatus` is heavily imbalanced** (84.0% defective vs. 16.0% not defective in this file). The source data card confirms this is intentional — the dataset was built to focus on defect instances, with non-defect instances added afterward — and explicitly recommends rebalancing the data before applying machine learning techniques. This project does not build a machine learning model (per the original project brief, this is a descriptive/diagnostic analysis project), so no rebalancing was performed, but this note is included for anyone extending this project toward predictive modeling.

## Citation

Dataset: *Predicting Manufacturing Defects Dataset*, created by Rabie El Kharoua, distributed on Kaggle under CC BY 4.0. Any redistribution of this dataset or work substantially derived from it should credit the original author per the license terms.
