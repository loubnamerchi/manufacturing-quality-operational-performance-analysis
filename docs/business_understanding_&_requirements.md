# Business Understanding & Requirements

## 1. Business Problem

The manufacturing company is experiencing challenges related to product quality, production efficiency, operational costs, equipment downtime, and resource utilization. Management needs to understand the key factors associated with product defects and operational inefficiencies in order to identify opportunities to improve product quality, reduce production costs and downtime, optimize resource utilization, and improve overall manufacturing performance.

Based on the actual dataset available (`manufacturing_defect_dataset.csv`, 3,240 production records with 17 operational variables), this problem can be refined into a concrete, data-supported version:

> Across 3,240 recorded production batches, **84.0% were flagged as defective**. Management needs to understand which of the recorded operational variables — production cost, supplier quality, maintenance hours, downtime, energy usage, worker productivity, inventory, and safety — are most strongly associated with this defect outcome, so that corrective actions can be prioritized.

Why this matters: every defective unit represents wasted material, wasted production cost, and potential rework or scrap cost. With defects present in the large majority of records in this dataset, even a modest reduction in defect rate would have a proportionally large impact on total production cost efficiency.

How data analysis helps: the dataset allows us to move from "we think maintenance/downtime/quality issues drive defects" to a **quantified, ranked view** of which variables actually correlate with the defect outcome, using correlation analysis, bucketed defect-rate comparisons, and KPI benchmarking.

## 2. Business Context

**Data provenance disclosure (read before the rest of this section):** `manufacturing_defect_dataset.csv` is a **synthetic dataset**, created for educational purposes by Rabie El Kharoua and distributed on Kaggle under CC BY 4.0 (see `docs/data_dictionary.md` for full citation). It does not describe a real manufacturing company. Framing this document around a hypothetical "the manufacturing company," per the original project brief, is a useful exercise for practicing the analytics workflow end-to-end, but every finding, KPI, and recommendation in this project should be understood as **"what this synthetic dataset shows,"** not as evidence about any real manufacturing operation.

Manufacturing businesses compete on the combination of product quality, cost, and delivery reliability. A few points of general context, clearly separated from what the data itself shows:

- **General manufacturing context** (industry knowledge, not derived from this dataset): Product quality directly affects customer satisfaction, warranty costs, and brand reputation. Production efficiency (output per unit of cost/time) determines competitiveness. Equipment downtime removes capacity from the schedule and can cascade into missed delivery commitments. Resource utilization (energy, inventory, labor) is a major cost lever in manufacturing operations, and data-driven decision-making increasingly replaces intuition-based management in these areas.
- **What this dataset actually supports:** Because the dataset has no date column, it cannot show whether performance is improving or worsening over time — it is a cross-sectional snapshot. It also has no supplier or plant identifiers, so it cannot attribute problems to specific business units. It CAN, however, show which of the 16 recorded operational variables are statistically associated with the recorded defect outcome (`DefectStatus`) within this snapshot. Note also that some of these variables are officially defined at different time cadences (`ProductionVolume` per day, `MaintenanceHours` per week, `SafetyIncidents` per month — see `docs/data_dictionary.md`), which is a further reason to treat this as a synthetic, illustrative snapshot rather than a literal daily operating record.

## 3. Stakeholders

| Stakeholder | Role | Interest in the Analysis | Decisions Supported |
|---|---|---|---|
| Manufacturing Management | Owns overall plant/production performance | Wants a clear, prioritized view of defect drivers and cost impact | Where to invest improvement resources |
| Operations Managers | Runs day-to-day production operations | Needs to know which operational levers (downtime, maintenance, productivity) matter most | Scheduling, staffing, process adjustments |
| Production Managers | Responsible for meeting production volume/cost targets | Wants to understand cost vs. defect trade-offs | Production planning, cost control |
| Quality Assurance Teams | Owns product quality outcomes | Needs evidence-based defect drivers, not assumptions | Quality control checkpoints, inspection focus |
| Quality Control Teams | Executes inspection and defect detection | Wants to know which conditions correlate with higher defect rates | Where to focus inspection effort |
| Maintenance Teams | Manages equipment upkeep and downtime | Needs to know whether maintenance hours/downtime relate to quality outcomes | Maintenance scheduling and prioritization |
| Supply Chain Managers | Manages inventory and supplier relationships | Wants visibility into inventory turnover / stockout patterns | Inventory policy adjustments |
| Procurement Teams | Manages supplier relationships and quality | Wants to know if supplier quality scores relate to defect outcomes | Supplier evaluation criteria |
| Finance Teams | Owns cost control and budgeting | Needs the cost impact of defects and operational inefficiency quantified | Budget allocation, cost-reduction targets |
| Plant Managers | Owns overall plant performance | Wants a consolidated KPI view across quality, cost, safety, and efficiency | Plant-wide improvement priorities |
| Data Analysts | Build and maintain this analysis | Needs a reproducible, well-documented pipeline | Ongoing monitoring and refresh of the analysis |

## 4. Business Objectives

All objectives below are directly supported by columns present in the dataset:

1. Understand overall manufacturing quality performance (via `DefectStatus`, `DefectRate`, `QualityScore`).
2. Identify which operational factors are most strongly associated with product defects (via correlation and bucketed comparisons across all 16 feature columns).
3. Analyze production performance (via `ProductionVolume`, `ProductionCost`, `CostPerUnit`).
4. Identify cost patterns associated with defective vs. non-defective production (via `ProductionCost`, `DefectStatus`).
5. Analyze equipment downtime and maintenance patterns (via `DowntimePercentage`, `MaintenanceHours`).
6. Analyze supplier quality's relationship to manufacturing outcomes (via `SupplierQuality`).
7. Analyze worker productivity's relationship to defects (via `WorkerProductivity`).
8. Analyze energy consumption and efficiency patterns (via `EnergyConsumption`, `EnergyEfficiency`).
9. Analyze inventory turnover and stockout patterns (via `InventoryTurnover`, `StockoutRate`).
10. Analyze safety incident patterns (via `SafetyIncidents`).
11. Identify concrete, data-supported operational improvement opportunities.

**Objectives explicitly out of scope** (not supported by the data): time-trend analysis, supplier-by-supplier comparison, plant-by-plant comparison, and product-line comparison — because no date, supplier ID, plant ID, or product ID columns exist in the dataset.

## 5. Functional Requirements

The analytical solution must:

- Load the raw manufacturing dataset from `data/raw/`.
- Validate data quality (required columns, data types, value ranges) before analysis.
- Clean the dataset (handle missing values, duplicates, standardize types) even though this dataset currently requires no changes, so the pipeline is robust to future data refreshes.
- Calculate the manufacturing KPIs defined in Section 7 below.
- Analyze production, quality, cost, downtime, maintenance, supplier, productivity, energy, inventory, and safety patterns using only the available columns.
- Identify factors statistically associated with defects, using correlation and bucketed defect-rate analysis.
- Generate professional visualizations (distributions, boxplots, correlation heatmap, business-question bar charts).
- Provide an interactive Streamlit dashboard for exploring the KPIs and data.
- Generate written reports (insights and final report) summarizing findings and recommendations.
- Automate the full workflow through a single, reproducible entry point (`main.py`).

## 6. Non-Functional Requirements

- **Reproducibility:** Running `python main.py` on a fresh clone of the repository (after `pip install -r requirements.txt`) must regenerate all processed data, KPIs, and figures identically.
- **Maintainability:** Business logic lives in `src/` modules with docstrings, not duplicated across notebooks.
- **Scalability:** The data-loading and pipeline structure supports adding further datasets (`src/data/load_data.py` supports multiple CSV/Excel files) without redesigning the project.
- **Performance:** The full pipeline (data + analysis + reporting) runs in a few seconds on this dataset size (3,240 rows), well within interactive use.
- **Reliability:** Every pipeline stage validates its inputs and logs progress/errors via `src/utils/logger.py`.
- **Documentation:** Every module, function, and notebook section is documented (this is a core requirement of this project, see the project's coding standard).
- **Data quality:** Automated tests (`tests/test_data_quality.py`) enforce the data-quality assumptions the rest of the project relies on.
- **Code organization:** Clear separation between data access (`src/data`), cleaning (`src/cleaning`), analysis (`src/analysis`), visualization (`src/visualization`), and orchestration (`pipelines/`, `main.py`).
- **Automation:** The three pipelines can be run independently or together via `main.py`.

## 7. KPIs and Metrics

All KPIs below are calculated in `src/analysis/kpi_analysis.py` using only columns present in the dataset.

| KPI Name | Business Definition | Formula | Business Importance | Required Columns |
|---|---|---|---|---|
| Overall Defect Rate (%) | Share of production records flagged as defective | `(count(DefectStatus=1) / total records) × 100` | Primary quality health indicator | `DefectStatus` |
| Average DefectRate Metric | Average of the dataset's continuous defect-rate measurement | `mean(DefectRate)` | Complements the binary defect flag with a continuous quality signal | `DefectRate` |
| Total / Average Production Volume | Overall and per-record production output | `sum(ProductionVolume)` / `mean(ProductionVolume)` | Tracks production scale | `ProductionVolume` |
| Total / Average Production Cost | Overall and per-record production cost | `sum(ProductionCost)` / `mean(ProductionCost)` | Tracks cost exposure | `ProductionCost` |
| Average Cost per Unit | Normalized cost efficiency metric | `mean(ProductionCost / ProductionVolume)` | Enables fair cost comparison across different production volumes | `ProductionCost`, `ProductionVolume` |
| Average Quality Score | Overall product quality level | `mean(QualityScore)` | Direct quality benchmark | `QualityScore` |
| Average Downtime (%) | Average share of time equipment is down | `mean(DowntimePercentage)` | Core operational-efficiency indicator | `DowntimePercentage` |
| Average Maintenance Hours | Average maintenance effort per record | `mean(MaintenanceHours)` | Maintenance workload indicator | `MaintenanceHours` |
| Average Supplier Quality | Average supplier quality score | `mean(SupplierQuality)` | Upstream quality indicator | `SupplierQuality` |
| Average Worker Productivity | Average worker productivity score | `mean(WorkerProductivity)` | Labor efficiency indicator | `WorkerProductivity` |
| Total Safety Incidents | Sum of recorded safety incidents | `sum(SafetyIncidents)` | Safety performance indicator | `SafetyIncidents` |
| Average Energy Consumption / Efficiency | Average energy usage and efficiency | `mean(EnergyConsumption)` / `mean(EnergyEfficiency)` | Resource-utilization indicator | `EnergyConsumption`, `EnergyEfficiency` |
| Average Inventory Turnover | Average inventory turnover ratio | `mean(InventoryTurnover)` | Inventory efficiency indicator | `InventoryTurnover` |
| Average Stockout Rate | Average rate of stockouts | `mean(StockoutRate)` | Supply-continuity risk indicator | `StockoutRate` |

*(KPIs such as "Material Cost" and "Additive Process Time" are also computable from `AdditiveMaterialCost` / `AdditiveProcessTime` and are included in the exploratory analysis; they are omitted from the primary KPI table above to keep the core dashboard focused, but are available in `src/analysis/kpi_analysis.py` naming conventions for extension.)*

## 8. Business Questions

**Quality questions**
- What is the overall defect rate? *(Supported — Section 7 KPI)*
- Which factors are associated with product defects? *(Supported — correlation + bucketed analysis across all 16 features)*
- How does quality performance vary across ranges of maintenance hours, supplier quality, downtime, etc.? *(Supported — bucketed analysis)*

**Production questions**
- Which factors are associated with higher production output? *(Supported — correlation with `ProductionVolume`)*
- How does production cost per unit vary across the dataset? *(Supported — `CostPerUnit`)*

**Cost questions**
- Are defects associated with increased operational costs? *(Supported — cost comparison by `DefectStatus`)*

**Operational questions**
- How does equipment downtime affect production performance? *(Supported — downtime buckets vs. production volume/defect rate)*
- Are maintenance-related variables associated with downtime or quality problems? *(Supported — maintenance buckets vs. quality score/defect rate)*

**Supplier questions**
- How does supplier quality relate to manufacturing quality? *(Supported — supplier-quality buckets vs. quality score/defect rate)*

**Resource questions**
- How efficient is energy consumption, and are there differences between defective and non-defective batches? *(Supported)*
- What is the relationship between inventory turnover and stockout rate? *(Supported)*

**Questions explicitly NOT supported by this dataset:** time-trend questions ("is quality improving month over month?"), supplier-specific questions ("which named supplier has the worst quality?"), and product/plant-specific questions — because the required identifier or date columns do not exist in the data.

## 9. Success Criteria

- **Technical:** `python main.py` runs end-to-end without errors and reproduces all outputs; all tests in `tests/test_data_quality.py` pass.
- **Analytical:** Every KPI and business question answer in Section 7/8 is backed by a specific, traceable calculation in `src/analysis/`.
- **Business:** Findings clearly identify which operational variables are most associated with defects, giving management a prioritized starting point for improvement efforts.
- **Data quality:** Zero missing values, zero duplicates, and zero invalid values confirmed and enforced by automated tests.
- **Dashboard:** The Streamlit dashboard loads the processed dataset and displays the core KPIs, filters, and charts without errors.

## 10. Analytical Thinking and Problem Framing

```
Business Problem
   (Quality and operational challenges affecting cost, downtime, and efficiency)
        ↓
Business Objectives
   (Understand defect drivers; benchmark production, cost, quality, and resource KPIs)
        ↓
Business Questions
   (Which variables associate with defects? How do cost, downtime, and quality relate?)
        ↓
Data Requirements
   (17-column manufacturing_defect_dataset.csv: production, cost, quality, defect,
    maintenance, downtime, inventory, productivity, safety, energy, additive-process data)
        ↓
KPIs
   (Defect rate, avg. production cost/volume, avg. quality score, downtime %,
    maintenance hours, supplier quality, worker productivity, energy metrics, etc.)
        ↓
Analysis
   (Descriptive statistics, correlation analysis, bucketed defect-rate comparisons,
    cost-by-defect-status comparison, EDA visualizations)
        ↓
Insights
   (e.g. defect rate rises sharply as maintenance hours increase; see reports/insights.md)
        ↓
Recommendations
   (Prioritize investigation of high-maintenance-hour production runs; monitor
    quality-score bands most associated with defects; see reports/insights.md)
        ↓
Business Decisions
   (Where to focus quality-improvement and maintenance-scheduling resources)
```

This structure is what the rest of the project (notebooks 01–07, `src/analysis/`, and `reports/`) implements step by step, ensuring every recommendation can be traced back through an insight, an analysis, a KPI, a business question, and ultimately back to the original business problem.
