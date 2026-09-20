"""
main.py
=======

ROLE IN THE PROJECT
--------------------
This is the single entry point that runs the COMPLETE, end-to-end
manufacturing analytics workflow, from raw data to final analytical
outputs, by coordinating the three pipelines in pipelines/:

    1. data_pipeline.py       -> load, validate, clean, transform, save
    2. analysis_pipeline.py   -> calculate KPIs, run business analysis,
                                  prepare dashboard data
    3. reporting_pipeline.py  -> generate and save all report figures

WHY main.py IS KEPT SMALL
-----------------------------
Following professional software engineering practice, main.py does NOT
contain any business logic itself. It only imports and calls the pipeline
functions in the right order, and reports a final summary. This keeps the
project modular: every pipeline can also be run and tested independently
(e.g. `python pipelines/data_pipeline.py`).

HOW TO RUN
------------
From the project root directory:

    pip install -r requirements.txt
    python main.py

This will:
- Read data/raw/manufacturing_defect_dataset.csv
- Write data/interim/manufacturing_interim.csv
- Write data/processed/manufacturing_processed.csv
- Write data/processed/dashboard_data.csv
- Write PNG charts to reports/figures/
- Write a full run log to logs/pipeline.log
"""

import time

from pipelines.data_pipeline import run_data_pipeline
from pipelines.analysis_pipeline import run_analysis_pipeline
from pipelines.reporting_pipeline import run_reporting_pipeline
from src.utils.config import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    """
    Run the complete Manufacturing Quality and Operational Performance
    Analysis workflow end-to-end.

    Step-by-step logic
    -------------------
    1. Load the project configuration once, so it is not re-read from
       disk by every pipeline.
    2. Run the data pipeline (raw -> cleaned -> processed dataset).
    3. Run the analysis pipeline (processed dataset -> KPIs, business
       aggregations, dashboard-ready dataset).
    4. Run the reporting pipeline (processed dataset -> saved figures).
    5. Print a short, human-readable summary of what was produced and how
       long the run took.
    """
    start_time = time.time()
    logger.info("################ MANUFACTURING ANALYTICS PIPELINE START ################")

    config = load_config()

    # Step 1: Data pipeline
    processed_df = run_data_pipeline(config)

    # Step 2: Analysis pipeline
    kpis, aggregations, _ = run_analysis_pipeline(config)

    # Step 3: Reporting pipeline
    run_reporting_pipeline(config)

    elapsed = round(time.time() - start_time, 2)
    logger.info(f"################ PIPELINE COMPLETE in {elapsed}s ################")

    print("\n" + "=" * 70)
    print("MANUFACTURING QUALITY AND OPERATIONAL PERFORMANCE ANALYSIS")
    print("=" * 70)
    print(f"Processed dataset shape : {processed_df.shape}")
    print(f"KPIs calculated         : {len(kpis)}")
    print(f"Business aggregations   : {len(aggregations)}")
    print(f"Total runtime           : {elapsed} seconds")
    print("\nKey KPIs:")
    for name, value in kpis.items():
        print(f"  - {name}: {value}")
    print("\nOutputs written to: data/interim/, data/processed/, reports/figures/")
    print("Full log available at: logs/pipeline.log")
    print("=" * 70)


if __name__ == "__main__":
    main()
