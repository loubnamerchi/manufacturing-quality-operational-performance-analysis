
import pandas as pd

from src.utils.logger import get_logger

logger = get_logger(__name__)


def defect_rate_by_bucket(df: pd.DataFrame, column: str, bins: int = 5) -> pd.DataFrame:

    work = df.copy()
    work["_bucket"] = pd.cut(work[column], bins=bins)
    grouped = work.groupby("_bucket", observed=True).agg(
        record_count=("DefectStatus", "size"),
        defect_rate_pct=("DefectStatus", lambda s: round(s.mean() * 100, 2)),
    ).reset_index()
    grouped = grouped.rename(columns={"_bucket": f"{column}_range"})
    return grouped


def cost_comparison_defective_vs_nondefective(df: pd.DataFrame) -> pd.DataFrame:

    work = df.copy()
    work["CostPerUnit"] = work["ProductionCost"] / work["ProductionVolume"].replace(0, pd.NA)

    summary = work.groupby("DefectStatus").agg(
        avg_production_cost=("ProductionCost", "mean"),
        avg_cost_per_unit=("CostPerUnit", "mean"),
        avg_production_volume=("ProductionVolume", "mean"),
        record_count=("DefectStatus", "size"),
    ).round(2)
    summary.index = summary.index.map({0: "Non-Defective", 1: "Defective"})
    return summary


def downtime_vs_production_performance(df: pd.DataFrame, bins: int = 5) -> pd.DataFrame:

    work = df.copy()
    work["_bucket"] = pd.cut(work["DowntimePercentage"], bins=bins)
    grouped = work.groupby("_bucket", observed=True).agg(
        avg_production_volume=("ProductionVolume", "mean"),
        defect_rate_pct=("DefectStatus", lambda s: round(s.mean() * 100, 2)),
        record_count=("DefectStatus", "size"),
    ).round(2).reset_index()
    grouped = grouped.rename(columns={"_bucket": "DowntimePercentage_range"})
    return grouped


def maintenance_vs_quality(df: pd.DataFrame, bins: int = 5) -> pd.DataFrame:

    work = df.copy()
    work["_bucket"] = pd.cut(work["MaintenanceHours"], bins=bins)
    grouped = work.groupby("_bucket", observed=True).agg(
        avg_quality_score=("QualityScore", "mean"),
        defect_rate_pct=("DefectStatus", lambda s: round(s.mean() * 100, 2)),
        record_count=("DefectStatus", "size"),
    ).round(2).reset_index()
    grouped = grouped.rename(columns={"_bucket": "MaintenanceHours_range"})
    return grouped


def supplier_quality_vs_performance(df: pd.DataFrame, bins: int = 5) -> pd.DataFrame:

    work = df.copy()
    work["_bucket"] = pd.cut(work["SupplierQuality"], bins=bins)
    grouped = work.groupby("_bucket", observed=True).agg(
        avg_quality_score=("QualityScore", "mean"),
        defect_rate_pct=("DefectStatus", lambda s: round(s.mean() * 100, 2)),
        record_count=("DefectStatus", "size"),
    ).round(2).reset_index()
    grouped = grouped.rename(columns={"_bucket": "SupplierQuality_range"})
    return grouped


def energy_efficiency_overview(df: pd.DataFrame) -> pd.DataFrame:

    summary = df.groupby("DefectStatus").agg(
        avg_energy_consumption=("EnergyConsumption", "mean"),
        avg_energy_efficiency=("EnergyEfficiency", "mean"),
        record_count=("DefectStatus", "size"),
    ).round(3)
    summary.index = summary.index.map({0: "Non-Defective", 1: "Defective"})
    return summary


def worker_productivity_vs_defects(df: pd.DataFrame, bins: int = 5) -> pd.DataFrame:

    work = df.copy()
    work["_bucket"] = pd.cut(work["WorkerProductivity"], bins=bins)
    grouped = work.groupby("_bucket", observed=True).agg(
        defect_rate_pct=("DefectStatus", lambda s: round(s.mean() * 100, 2)),
        record_count=("DefectStatus", "size"),
    ).round(2).reset_index()
    grouped = grouped.rename(columns={"_bucket": "WorkerProductivity_range"})
    return grouped


def inventory_and_stockout_overview(df: pd.DataFrame) -> pd.DataFrame:

    summary = df.groupby("DefectStatus").agg(
        avg_inventory_turnover=("InventoryTurnover", "mean"),
        avg_stockout_rate=("StockoutRate", "mean"),
        record_count=("DefectStatus", "size"),
    ).round(4)
    summary.index = summary.index.map({0: "Non-Defective", 1: "Defective"})
    return summary
