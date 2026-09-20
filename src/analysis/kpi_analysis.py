

from typing import Dict

import pandas as pd

from src.utils.helpers import percentage
from src.utils.logger import get_logger

logger = get_logger(__name__)


def kpi_defect_rate(df: pd.DataFrame) -> float:

    return percentage(int((df["DefectStatus"] == 1).sum()), len(df))


def kpi_average_defect_rate_metric(df: pd.DataFrame) -> float:

    return round(df["DefectRate"].mean(), 3)


def kpi_total_production_volume(df: pd.DataFrame) -> float:

    return round(df["ProductionVolume"].sum(), 2)


def kpi_average_production_volume(df: pd.DataFrame) -> float:

    return round(df["ProductionVolume"].mean(), 2)


def kpi_total_production_cost(df: pd.DataFrame) -> float:

    return round(df["ProductionCost"].sum(), 2)


def kpi_average_production_cost(df: pd.DataFrame) -> float:

    return round(df["ProductionCost"].mean(), 2)


def kpi_average_quality_score(df: pd.DataFrame) -> float:

    return round(df["QualityScore"].mean(), 2)


def kpi_average_downtime_percentage(df: pd.DataFrame) -> float:

    return round(df["DowntimePercentage"].mean(), 3)


def kpi_average_maintenance_hours(df: pd.DataFrame) -> float:

    return round(df["MaintenanceHours"].mean(), 2)


def kpi_average_supplier_quality(df: pd.DataFrame) -> float:

    return round(df["SupplierQuality"].mean(), 2)


def kpi_average_worker_productivity(df: pd.DataFrame) -> float:

    return round(df["WorkerProductivity"].mean(), 2)


def kpi_total_safety_incidents(df: pd.DataFrame) -> int:

    return int(df["SafetyIncidents"].sum())


def kpi_average_energy_consumption(df: pd.DataFrame) -> float:

    return round(df["EnergyConsumption"].mean(), 2)


def kpi_average_energy_efficiency(df: pd.DataFrame) -> float:

    return round(df["EnergyEfficiency"].mean(), 4)


def kpi_average_inventory_turnover(df: pd.DataFrame) -> float:

    return round(df["InventoryTurnover"].mean(), 2)


def kpi_average_stockout_rate(df: pd.DataFrame) -> float:

    return round(df["StockoutRate"].mean(), 4)


def kpi_average_cost_per_unit(df: pd.DataFrame) -> float:

    per_unit = df["ProductionCost"] / df["ProductionVolume"].replace(0, pd.NA)
    return round(per_unit.mean(), 2)


def calculate_all_kpis(df: pd.DataFrame) -> Dict[str, float]:
   
    kpis = {
        "Overall Defect Rate (%)": kpi_defect_rate(df),
        "Average DefectRate Metric": kpi_average_defect_rate_metric(df),
        "Total Production Volume": kpi_total_production_volume(df),
        "Average Production Volume": kpi_average_production_volume(df),
        "Total Production Cost ($)": kpi_total_production_cost(df),
        "Average Production Cost ($)": kpi_average_production_cost(df),
        "Average Cost per Unit ($)": kpi_average_cost_per_unit(df),
        "Average Quality Score": kpi_average_quality_score(df),
        "Average Downtime (%)": kpi_average_downtime_percentage(df),
        "Average Maintenance Hours": kpi_average_maintenance_hours(df),
        "Average Supplier Quality": kpi_average_supplier_quality(df),
        "Average Worker Productivity": kpi_average_worker_productivity(df),
        "Total Safety Incidents": kpi_total_safety_incidents(df),
        "Average Energy Consumption": kpi_average_energy_consumption(df),
        "Average Energy Efficiency": kpi_average_energy_efficiency(df),
        "Average Inventory Turnover": kpi_average_inventory_turnover(df),
        "Average Stockout Rate": kpi_average_stockout_rate(df),
    }
    logger.info(f"Calculated {len(kpis)} manufacturing KPIs.")
    return kpis
