
import pandas as pd

from src.data.load_data import load_csv
from src.analysis.business_analysis import (
    defect_rate_by_bucket,
    downtime_vs_production_performance,
    maintenance_vs_quality,
)
from src.visualization.charts import (
    plot_histogram,
    plot_boxplot,
    plot_correlation_heatmap,
    plot_bar,
)
from src.utils.config import load_config, resolve_path
from src.utils.logger import get_logger

logger = get_logger(__name__)


def generate_distribution_charts(df: pd.DataFrame, figures_dir):

    columns_to_plot = [
        "ProductionVolume", "ProductionCost", "QualityScore",
        "DefectRate", "DowntimePercentage", "MaintenanceHours",
    ]
    for col in columns_to_plot:
        plot_histogram(df, col, save_path=figures_dir / f"hist_{col}.png")


def generate_correlation_chart(df: pd.DataFrame, figures_dir):

    numeric_df = df.select_dtypes(include="number")
    plot_correlation_heatmap(numeric_df, save_path=figures_dir / "correlation_heatmap.png")


def generate_defect_comparison_charts(df: pd.DataFrame, figures_dir):

    columns_to_compare = ["MaintenanceHours", "QualityScore", "ProductionCost", "DefectRate"]
    for col in columns_to_compare:
        plot_boxplot(df, col, by="DefectStatus",
                     title=f"{col} by Defect Status",
                     save_path=figures_dir / f"boxplot_{col}_by_defect_status.png")


def generate_business_question_charts(df: pd.DataFrame, figures_dir):

    maint = defect_rate_by_bucket(df, "MaintenanceHours")
    plot_bar(
        maint["MaintenanceHours_range"], maint["defect_rate_pct"],
        title="Defect Rate (%) by Maintenance Hours Range",
        xlabel="Maintenance Hours Range", ylabel="Defect Rate (%)",
        save_path=figures_dir / "bar_defect_rate_by_maintenance.png",
    )

    downtime = downtime_vs_production_performance(df)
    plot_bar(
        downtime["DowntimePercentage_range"], downtime["defect_rate_pct"],
        title="Defect Rate (%) by Downtime Percentage Range",
        xlabel="Downtime Percentage Range", ylabel="Defect Rate (%)",
        save_path=figures_dir / "bar_defect_rate_by_downtime.png",
    )

    maint_quality = maintenance_vs_quality(df)
    plot_bar(
        maint_quality["MaintenanceHours_range"], maint_quality["avg_quality_score"],
        title="Average Quality Score by Maintenance Hours Range",
        xlabel="Maintenance Hours Range", ylabel="Average Quality Score",
        save_path=figures_dir / "bar_quality_score_by_maintenance.png",
    )


def run_reporting_pipeline(config: dict = None):

    config = config or load_config()
    logger.info("=== REPORTING PIPELINE: START ===")

    processed_path = resolve_path(config["data"]["processed_path"])
    df = load_csv(processed_path)

    figures_dir = resolve_path(config["outputs"]["figures_dir"])
    figures_dir.mkdir(parents=True, exist_ok=True)

    generate_distribution_charts(df, figures_dir)
    generate_correlation_chart(df, figures_dir)
    generate_defect_comparison_charts(df, figures_dir)
    generate_business_question_charts(df, figures_dir)

    logger.info(f"All figures saved to {figures_dir}")
    logger.info("=== REPORTING PIPELINE: COMPLETE ===")


if __name__ == "__main__":
    run_reporting_pipeline()
