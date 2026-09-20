

from typing import Dict

import pandas as pd

from src.data.load_data import load_csv
from src.analysis.kpi_analysis import calculate_all_kpis
from src.analysis.business_analysis import (
    defect_rate_by_bucket,
    cost_comparison_defective_vs_nondefective,
    downtime_vs_production_performance,
    maintenance_vs_quality,
    supplier_quality_vs_performance,
    energy_efficiency_overview,
    worker_productivity_vs_defects,
    inventory_and_stockout_overview,
)
from src.visualization.dashboard_data import save_dashboard_dataset
from src.utils.config import load_config, resolve_path
from src.utils.logger import get_logger

logger = get_logger(__name__)


def run_business_aggregations(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:

    aggregations = {
        "defect_rate_by_maintenance_hours": defect_rate_by_bucket(df, "MaintenanceHours"),
        "defect_rate_by_quality_score": defect_rate_by_bucket(df, "QualityScore"),
        "cost_comparison_by_defect_status": cost_comparison_defective_vs_nondefective(df),
        "downtime_vs_production": downtime_vs_production_performance(df),
        "maintenance_vs_quality": maintenance_vs_quality(df),
        "supplier_quality_vs_performance": supplier_quality_vs_performance(df),
        "energy_efficiency_overview": energy_efficiency_overview(df),
        "worker_productivity_vs_defects": worker_productivity_vs_defects(df),
        "inventory_and_stockout_overview": inventory_and_stockout_overview(df),
    }
    logger.info(f"Completed {len(aggregations)} business aggregation analyses.")
    return aggregations


def run_analysis_pipeline(config: dict = None):

    config = config or load_config()
    logger.info("=== ANALYSIS PIPELINE: START ===")

    processed_path = resolve_path(config["data"]["processed_path"])
    df = load_csv(processed_path)

    kpis = calculate_all_kpis(df)
    logger.info(f"KPIs calculated: {kpis}")

    aggregations = run_business_aggregations(df)

    dashboard_path = resolve_path(config["data"]["dashboard_data_path"])
    save_dashboard_dataset(df, dashboard_path)

    logger.info("=== ANALYSIS PIPELINE: COMPLETE ===")
    return kpis, aggregations, df


if __name__ == "__main__":
    run_analysis_pipeline()
