
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

# Ensure the project root is importable regardless of the working directory
# `streamlit run` is invoked from.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis.kpi_analysis import calculate_all_kpis
from src.analysis.business_analysis import defect_rate_by_bucket, maintenance_vs_quality
from src.utils.config import load_config, resolve_path

st.set_page_config(
    page_title="Manufacturing Quality & Operational Performance",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    """Load the dashboard-ready processed dataset (cached across reruns)."""
    config = load_config()
    path = resolve_path(config["data"]["dashboard_data_path"])
    return pd.read_csv(path)


def main():
    st.title("🏭 Manufacturing Quality and Operational Performance Analysis")
    st.caption(
        "Interactive dashboard built on manufacturing_defect_dataset.csv "
        "(3,240 production records, 17 operational variables)."
    )

    df = load_data()
    st.sidebar.header("Filters")

    quality_options = sorted(df["QualityCategory"].dropna().unique().tolist())
    selected_quality = st.sidebar.multiselect(
        "Quality Category", options=quality_options, default=quality_options
    )

    downtime_options = sorted(df["DowntimeCategory"].dropna().unique().tolist())
    selected_downtime = st.sidebar.multiselect(
        "Downtime Category", options=downtime_options, default=downtime_options
    )

    defect_options = df["DefectLabel"].unique().tolist()
    selected_defect = st.sidebar.multiselect(
        "Defect Status", options=defect_options, default=defect_options
    )

    filtered = df[
        df["QualityCategory"].isin(selected_quality)
        & df["DowntimeCategory"].isin(selected_downtime)
        & df["DefectLabel"].isin(selected_defect)
    ]

    st.sidebar.markdown(f"**Records shown:** {len(filtered):,} / {len(df):,}")

    if filtered.empty:
        st.warning("No records match the selected filters. Please broaden your filter selection.")
        return

    kpis = calculate_all_kpis(filtered)

    st.subheader("Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Overall Defect Rate", f"{kpis['Overall Defect Rate (%)']}%")
    col2.metric("Avg Production Cost", f"${kpis['Average Production Cost ($)']:,.0f}")
    col3.metric("Avg Quality Score", f"{kpis['Average Quality Score']}")
    col4.metric("Avg Maintenance Hours", f"{kpis['Average Maintenance Hours']}")

    col5, col6, col7, col8 = st.columns(4)
    col5.metric("Avg Downtime (%)", f"{kpis['Average Downtime (%)']}%")
    col6.metric("Avg Supplier Quality", f"{kpis['Average Supplier Quality']}")
    col7.metric("Total Safety Incidents", f"{kpis['Total Safety Incidents']}")
    col8.metric("Avg Cost per Unit", f"${kpis['Average Cost per Unit ($)']:,.2f}")

    st.divider()

    st.subheader("Defect Analysis")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.markdown("**Defect Rate by Maintenance Hours Range**")
        maint = defect_rate_by_bucket(filtered, "MaintenanceHours")
        maint_display = maint.copy()
        maint_display["MaintenanceHours_range"] = maint_display["MaintenanceHours_range"].astype(str)
        st.bar_chart(maint_display.set_index("MaintenanceHours_range")["defect_rate_pct"])

    with chart_col2:
        st.markdown("**Average Quality Score by Maintenance Hours Range**")
        mq = maintenance_vs_quality(filtered)
        mq_display = mq.copy()
        mq_display["MaintenanceHours_range"] = mq_display["MaintenanceHours_range"].astype(str)
        st.bar_chart(mq_display.set_index("MaintenanceHours_range")["avg_quality_score"])

    st.markdown("**Defect Status Count by Quality Category**")
    quality_defect = filtered.groupby(["QualityCategory", "DefectLabel"], observed=True).size().unstack(fill_value=0)
    st.bar_chart(quality_defect)

    st.divider()

    st.subheader("Production and Cost Overview")

    prod_col1, prod_col2 = st.columns(2)
    with prod_col1:
        st.markdown("**Production Volume Distribution**")
        st.bar_chart(filtered["ProductionVolume"].value_counts(bins=15).sort_index())

    with prod_col2:
        st.markdown("**Production Cost Distribution**")
        st.bar_chart(filtered["ProductionCost"].value_counts(bins=15).sort_index())

    st.divider()

    st.subheader("Filtered Data")
    st.dataframe(filtered, use_container_width=True)


if __name__ == "__main__":
    main()
