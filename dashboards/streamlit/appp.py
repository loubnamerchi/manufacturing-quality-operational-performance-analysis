"""
app.py
======

Manufacturing Quality & Operational Performance Dashboard

Interactive Streamlit dashboard for:
- Quality performance
- Defect analysis
- Maintenance performance
- Downtime analysis
- Production performance
- Cost analysis
- Operational relationships
- Filtered data exploration
"""

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# =============================================================================
# PROJECT PATH
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# =============================================================================
# PROJECT IMPORTS
# =============================================================================

from src.analysis.kpi_analysis import calculate_all_kpis
from src.analysis.business_analysis import (
    defect_rate_by_bucket,
    maintenance_vs_quality,
)
from src.utils.config import load_config, resolve_path
from src.utils.logger import get_logger


# =============================================================================
# LOGGER
# =============================================================================

logger = get_logger(__name__)


# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Manufacturing Quality & Operational Performance",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# CUSTOM CSS
# =============================================================================

st.markdown(
    """
    <style>

    /* ---------------------------------------------------------
       Global
    --------------------------------------------------------- */

    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1600px;
    }


    /* ---------------------------------------------------------
       Header
    --------------------------------------------------------- */

    .dashboard-header {
        padding: 1.2rem 1.5rem;
        border-radius: 14px;
        margin-bottom: 1.5rem;
        background: linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a8a 100%
        );
        color: white;
    }

    .dashboard-header h1 {
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
    }

    .dashboard-header p {
        margin-top: 0.4rem;
        margin-bottom: 0;
        color: #dbeafe;
        font-size: 0.95rem;
    }


    /* ---------------------------------------------------------
       KPI Cards
    --------------------------------------------------------- */

    .kpi-card {
        background-color: white;
        padding: 1.2rem;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
        min-height: 125px;
    }

    .kpi-title {
        color: #64748b;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .kpi-value {
        color: #0f172a;
        font-size: 1.7rem;
        font-weight: 700;
        margin-top: 0.35rem;
    }

    .kpi-description {
        color: #94a3b8;
        font-size: 0.75rem;
        margin-top: 0.3rem;
    }


    /* ---------------------------------------------------------
       Section Headers
    --------------------------------------------------------- */

    .section-header {
        margin-top: 1.2rem;
        margin-bottom: 0.8rem;
    }

    .section-header h2 {
        color: #0f172a;
        font-size: 1.35rem;
        margin-bottom: 0.1rem;
    }

    .section-header p {
        color: #64748b;
        font-size: 0.85rem;
    }


    /* ---------------------------------------------------------
       Insight Box
    --------------------------------------------------------- */

    .insight-box {
        background-color: #eff6ff;
        border-left: 4px solid #2563eb;
        padding: 0.9rem 1rem;
        border-radius: 8px;
        margin-bottom: 0.7rem;
        color: #1e293b;
    }


    /* ---------------------------------------------------------
       Sidebar
    --------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #0f172a;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =============================================================================
# DATA LOADING
# =============================================================================

@st.cache_data(show_spinner="Loading manufacturing data...")
def load_data() -> pd.DataFrame:
    """
    Load the dashboard-ready processed dataset.

    Returns
    -------
    pd.DataFrame
        Dashboard dataset.
    """

    config = load_config()

    data_path = resolve_path(
        config["data"]["dashboard_data_path"]
    )

    logger.info("Loading dashboard data from: %s", data_path)

    df = pd.read_csv(data_path)

    logger.info(
        "Dashboard data loaded successfully: %s rows, %s columns",
        len(df),
        len(df.columns),
    )

    return df


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def format_number(value):
    """Format numeric values for KPI cards."""

    if pd.isna(value):
        return "N/A"

    if isinstance(value, float):
        return f"{value:,.2f}"

    return f"{value:,}"


def kpi_card(title, value, description=""):
    """Render a modern KPI card."""

    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-description">{description}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_header(title, description=""):
    """Render a dashboard section header."""

    st.markdown(
        f"""
        <div class="section-header">
            <h2>{title}</h2>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plotly_layout(fig, height=420):
    """Apply common Plotly styling."""

    fig.update_layout(
        height=height,
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20,
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",
        legend_title_text="",
    )

    fig.update_xaxes(
        showgrid=False,
        linecolor="#e2e8f0",
    )

    fig.update_yaxes(
        gridcolor="#e2e8f0",
        zeroline=False,
    )

    return fig


# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():

    # -------------------------------------------------------------------------
    # Load data
    # -------------------------------------------------------------------------

    df = load_data()

    if df.empty:
        st.error("The dashboard dataset is empty.")
        return


    # -------------------------------------------------------------------------
    # Header
    # -------------------------------------------------------------------------

    st.markdown(
        """
        <div class="dashboard-header">
            <h1>🏭 Manufacturing Quality & Operational Performance</h1>
            <p>
                Interactive analysis of manufacturing quality, defects,
                maintenance, downtime, production and cost performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


    # =============================================================================
    # SIDEBAR FILTERS
    # =============================================================================

    st.sidebar.title("🎛️ Dashboard Filters")

    st.sidebar.caption(
        "Use the filters below to dynamically update all dashboard metrics and charts."
    )

    # -------------------------------------------------------------------------
    # Quality filter
    # -------------------------------------------------------------------------

    if "QualityCategory" in df.columns:

        quality_options = sorted(
            df["QualityCategory"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_quality = st.sidebar.multiselect(
            "Quality Category",
            options=quality_options,
            default=quality_options,
        )

    else:
        selected_quality = []


    # -------------------------------------------------------------------------
    # Downtime filter
    # -------------------------------------------------------------------------

    if "DowntimeCategory" in df.columns:

        downtime_options = sorted(
            df["DowntimeCategory"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_downtime = st.sidebar.multiselect(
            "Downtime Category",
            options=downtime_options,
            default=downtime_options,
        )

    else:
        selected_downtime = []


    # -------------------------------------------------------------------------
    # Defect filter
    # -------------------------------------------------------------------------

    if "DefectLabel" in df.columns:

        defect_options = sorted(
            df["DefectLabel"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_defect = st.sidebar.multiselect(
            "Defect Status",
            options=defect_options,
            default=defect_options,
        )

    else:
        selected_defect = []


    # -------------------------------------------------------------------------
    # Optional categorical filters
    # -------------------------------------------------------------------------

    optional_filters = {}

    categorical_columns = [
        "MachineType",
        "ProductionLine",
        "ProductType",
        "Shift",
        "Supplier",
        "Operator",
    ]

    for column in categorical_columns:

        if column in df.columns:

            options = sorted(
                df[column]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            if len(options) <= 30:

                selected = st.sidebar.multiselect(
                    column.replace("_", " "),
                    options=options,
                    default=options,
                )

                optional_filters[column] = selected


    # =============================================================================
    # FILTER DATA
    # =============================================================================

    filtered = df.copy()

    if "QualityCategory" in df.columns:
        filtered = filtered[
            filtered["QualityCategory"].isin(selected_quality)
        ]

    if "DowntimeCategory" in df.columns:
        filtered = filtered[
            filtered["DowntimeCategory"].isin(selected_downtime)
        ]

    if "DefectLabel" in df.columns:
        filtered = filtered[
            filtered["DefectLabel"].isin(selected_defect)
        ]

    for column, selected_values in optional_filters.items():

        filtered = filtered[
            filtered[column].astype(str).isin(selected_values)
        ]


    # -------------------------------------------------------------------------
    # Sidebar summary
    # -------------------------------------------------------------------------

    st.sidebar.divider()

    st.sidebar.metric(
        "Records shown",
        f"{len(filtered):,}",
        f"of {len(df):,}",
    )

    coverage = (
        len(filtered) / len(df) * 100
        if len(df) > 0
        else 0
    )

    st.sidebar.progress(
        min(coverage / 100, 1.0),
        text=f"{coverage:.1f}% of dataset",
    )


    # -------------------------------------------------------------------------
    # Empty data check
    # -------------------------------------------------------------------------

    if filtered.empty:

        st.warning(
            "No records match the selected filters. "
            "Please broaden your filter selection."
        )

        return


    # =============================================================================
    # KPI CALCULATION
    # =============================================================================

    kpis = calculate_all_kpis(filtered)


    # =============================================================================
    # EXECUTIVE OVERVIEW
    # =============================================================================

    section_header(
        "Executive Overview",
        "High-level view of quality, operational efficiency and manufacturing performance.",
    )

    kpi_row_1 = st.columns(4)

    with kpi_row_1[0]:
        kpi_card(
            "Overall Defect Rate",
            f"{kpis['Overall Defect Rate (%)']}%",
            "Share of production records classified as defective",
        )

    with kpi_row_1[1]:
        kpi_card(
            "Average Quality Score",
            format_number(kpis["Average Quality Score"]),
            "Average quality performance score",
        )

    with kpi_row_1[2]:
        kpi_card(
            "Average Downtime",
            f"{kpis['Average Downtime (%)']}%",
            "Average percentage of production downtime",
        )

    with kpi_row_1[3]:
        kpi_card(
            "Safety Incidents",
            format_number(kpis["Total Safety Incidents"]),
            "Total recorded safety incidents",
        )


    kpi_row_2 = st.columns(4)

    with kpi_row_2[0]:
        kpi_card(
            "Average Production Cost",
            f"${kpis['Average Production Cost ($)']:,.0f}",
            "Average production cost per record",
        )

    with kpi_row_2[1]:
        kpi_card(
            "Average Cost / Unit",
            f"${kpis['Average Cost per Unit ($)']:,.2f}",
            "Average manufacturing cost per unit",
        )

    with kpi_row_2[2]:
        kpi_card(
            "Maintenance Hours",
            format_number(kpis["Average Maintenance Hours"]),
            "Average maintenance hours",
        )

    with kpi_row_2[3]:
        kpi_card(
            "Supplier Quality",
            format_number(kpis["Average Supplier Quality"]),
            "Average supplier quality score",
        )


    # =============================================================================
    # TABS
    # =============================================================================

    tab_overview, tab_quality, tab_operations, tab_cost, tab_data = st.tabs(
        [
            "📊 Overview",
            "🔎 Quality & Defects",
            "⚙️ Operations",
            "💰 Production & Cost",
            "📋 Data Explorer",
        ]
    )


    # =============================================================================
    # TAB 1 — OVERVIEW
    # =============================================================================

    with tab_overview:

        section_header(
            "Performance Overview",
            "Distribution of quality outcomes and operational performance.",
        )

        col1, col2 = st.columns(2)

        # ---------------------------------------------------------------------
        # Quality category
        # ---------------------------------------------------------------------

        with col1:

            if "QualityCategory" in filtered.columns:

                quality_counts = (
                    filtered["QualityCategory"]
                    .value_counts()
                    .reset_index()
                )

                quality_counts.columns = [
                    "QualityCategory",
                    "Count",
                ]

                fig = px.pie(
                    quality_counts,
                    names="QualityCategory",
                    values="Count",
                    hole=0.55,
                    title="Quality Category Distribution",
                )

                fig.update_traces(
                    textposition="inside",
                    textinfo="percent+label",
                )

                plotly_layout(fig, 400)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Defect status
        # ---------------------------------------------------------------------

        with col2:

            if "DefectLabel" in filtered.columns:

                defect_counts = (
                    filtered["DefectLabel"]
                    .value_counts()
                    .reset_index()
                )

                defect_counts.columns = [
                    "DefectLabel",
                    "Count",
                ]

                fig = px.bar(
                    defect_counts,
                    x="DefectLabel",
                    y="Count",
                    title="Defect Status Distribution",
                    text_auto=True,
                )

                plotly_layout(fig, 400)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Quality vs downtime
        # ---------------------------------------------------------------------

        if {
            "QualityCategory",
            "DowntimePercentage",
        }.issubset(filtered.columns):

            grouped = (
                filtered.groupby(
                    "QualityCategory",
                    observed=True,
                )["DowntimePercentage"]
                .mean()
                .reset_index()
            )

            fig = px.bar(
                grouped,
                x="QualityCategory",
                y="DowntimePercentage",
                title="Average Downtime by Quality Category",
                text_auto=".2f",
            )

            plotly_layout(fig, 420)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    # =============================================================================
    # TAB 2 — QUALITY & DEFECTS
    # =============================================================================

    with tab_quality:

        section_header(
            "Quality & Defect Analysis",
            "Investigate defect patterns and relationships with maintenance and quality.",
        )

        chart_col1, chart_col2 = st.columns(2)

        # ---------------------------------------------------------------------
        # Defect rate by maintenance
        # ---------------------------------------------------------------------

        with chart_col1:

            if "MaintenanceHours" in filtered.columns:

                maint = defect_rate_by_bucket(
                    filtered,
                    "MaintenanceHours",
                )

                maint_display = maint.copy()

                maint_display[
                    "MaintenanceHours_range"
                ] = maint_display[
                    "MaintenanceHours_range"
                ].astype(str)

                fig = px.bar(
                    maint_display,
                    x="MaintenanceHours_range",
                    y="defect_rate_pct",
                    title="Defect Rate by Maintenance Hours",
                    labels={
                        "MaintenanceHours_range": "Maintenance Hours",
                        "defect_rate_pct": "Defect Rate (%)",
                    },
                    text_auto=".2f",
                )

                plotly_layout(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Quality score by maintenance
        # ---------------------------------------------------------------------

        with chart_col2:

            if "MaintenanceHours" in filtered.columns:

                mq = maintenance_vs_quality(
                    filtered
                )

                mq_display = mq.copy()

                mq_display[
                    "MaintenanceHours_range"
                ] = mq_display[
                    "MaintenanceHours_range"
                ].astype(str)

                fig = px.line(
                    mq_display,
                    x="MaintenanceHours_range",
                    y="avg_quality_score",
                    markers=True,
                    title="Average Quality Score by Maintenance Hours",
                    labels={
                        "MaintenanceHours_range": "Maintenance Hours",
                        "avg_quality_score": "Average Quality Score",
                    },
                )

                plotly_layout(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Quality × defect matrix
        # ---------------------------------------------------------------------

        if {
            "QualityCategory",
            "DefectLabel",
        }.issubset(filtered.columns):

            quality_defect = (
                filtered.groupby(
                    ["QualityCategory", "DefectLabel"],
                    observed=True,
                )
                .size()
                .reset_index(name="Count")
            )

            fig = px.bar(
                quality_defect,
                x="QualityCategory",
                y="Count",
                color="DefectLabel",
                barmode="group",
                title="Defect Status by Quality Category",
                text_auto=True,
            )

            plotly_layout(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        # ---------------------------------------------------------------------
        # Quality score distribution
        # ---------------------------------------------------------------------

        if "QualityScore" in filtered.columns:

            fig = px.histogram(
                filtered,
                x="QualityScore",
                nbins=30,
                marginal="box",
                title="Quality Score Distribution",
            )

            plotly_layout(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    # =============================================================================
    # TAB 3 — OPERATIONS
    # =============================================================================

    with tab_operations:

        section_header(
            "Operational Performance",
            "Analyze maintenance, downtime and production operational behavior.",
        )

        col1, col2 = st.columns(2)

        # ---------------------------------------------------------------------
        # Downtime distribution
        # ---------------------------------------------------------------------

        with col1:

            if "DowntimePercentage" in filtered.columns:

                fig = px.histogram(
                    filtered,
                    x="DowntimePercentage",
                    nbins=30,
                    title="Downtime Percentage Distribution",
                )

                plotly_layout(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Maintenance distribution
        # ---------------------------------------------------------------------

        with col2:

            if "MaintenanceHours" in filtered.columns:

                fig = px.histogram(
                    filtered,
                    x="MaintenanceHours",
                    nbins=30,
                    title="Maintenance Hours Distribution",
                )

                plotly_layout(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Maintenance vs downtime
        # ---------------------------------------------------------------------

        if {
            "MaintenanceHours",
            "DowntimePercentage",
        }.issubset(filtered.columns):

            scatter_columns = [
                "MaintenanceHours",
                "DowntimePercentage",
            ]

            if "QualityCategory" in filtered.columns:
                scatter_columns.append("QualityCategory")

            scatter_df = filtered[scatter_columns].dropna()

            fig = px.scatter(
                scatter_df,
                x="MaintenanceHours",
                y="DowntimePercentage",
                color=(
                    "QualityCategory"
                    if "QualityCategory" in scatter_df.columns
                    else None
                ),
                trendline="ols",
                opacity=0.65,
                title="Maintenance Hours vs Downtime",
                labels={
                    "MaintenanceHours": "Maintenance Hours",
                    "DowntimePercentage": "Downtime (%)",
                },
            )

            plotly_layout(fig, 480)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        # ---------------------------------------------------------------------
        # Operational categories
        # ---------------------------------------------------------------------

        operational_columns = [
            column
            for column in [
                "MachineType",
                "ProductionLine",
                "Shift",
                "Supplier",
                "Operator",
            ]
            if column in filtered.columns
        ]

        if operational_columns:

            selected_dimension = st.selectbox(
                "Analyze operational dimension",
                operational_columns,
            )

            if selected_dimension in filtered.columns:

                grouped = (
                    filtered.groupby(
                        selected_dimension,
                        observed=True,
                    )
                    .agg(
                        Records=(selected_dimension, "size"),
                        Avg_Quality=(
                            "QualityScore",
                            "mean",
                        )
                        if "QualityScore" in filtered.columns
                        else (
                            selected_dimension,
                            "size",
                        ),
                        Avg_Downtime=(
                            "DowntimePercentage",
                            "mean",
                        )
                        if "DowntimePercentage" in filtered.columns
                        else (
                            selected_dimension,
                            "size",
                        ),
                    )
                    .reset_index()
                )

                if "QualityScore" in filtered.columns:

                    fig = px.bar(
                        grouped,
                        x=selected_dimension,
                        y="Avg_Quality",
                        title=f"Average Quality Score by {selected_dimension}",
                        text_auto=".2f",
                    )

                    plotly_layout(fig)

                    st.plotly_chart(
                        fig,
                        use_container_width=True,
                    )


    # =============================================================================
    # TAB 4 — PRODUCTION & COST
    # =============================================================================

    with tab_cost:

        section_header(
            "Production & Cost Performance",
            "Explore production volume, cost behavior and cost efficiency.",
        )

        col1, col2 = st.columns(2)

        # ---------------------------------------------------------------------
        # Production volume
        # ---------------------------------------------------------------------

        with col1:

            if "ProductionVolume" in filtered.columns:

                fig = px.histogram(
                    filtered,
                    x="ProductionVolume",
                    nbins=30,
                    title="Production Volume Distribution",
                )

                plotly_layout(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Production cost
        # ---------------------------------------------------------------------

        with col2:

            if "ProductionCost" in filtered.columns:

                fig = px.histogram(
                    filtered,
                    x="ProductionCost",
                    nbins=30,
                    title="Production Cost Distribution",
                )

                plotly_layout(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )


        # ---------------------------------------------------------------------
        # Production volume vs cost
        # ---------------------------------------------------------------------

        if {
            "ProductionVolume",
            "ProductionCost",
        }.issubset(filtered.columns):

            scatter_df = filtered[
                [
                    "ProductionVolume",
                    "ProductionCost",
                ]
            ].dropna()

            fig = px.scatter(
                scatter_df,
                x="ProductionVolume",
                y="ProductionCost",
                opacity=0.6,
                trendline="ols",
                title="Production Volume vs Production Cost",
                labels={
                    "ProductionVolume": "Production Volume",
                    "ProductionCost": "Production Cost",
                },
            )

            plotly_layout(fig, 480)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


        # ---------------------------------------------------------------------
        # Cost per unit
        # ---------------------------------------------------------------------

        if {
            "ProductionVolume",
            "ProductionCost",
        }.issubset(filtered.columns):

            cost_df = filtered[
                [
                    "ProductionVolume",
                    "ProductionCost",
                ]
            ].copy()

            cost_df = cost_df[
                cost_df["ProductionVolume"] > 0
            ]

            cost_df["CostPerUnit"] = (
                cost_df["ProductionCost"]
                / cost_df["ProductionVolume"]
            )

            fig = px.histogram(
                cost_df,
                x="CostPerUnit",
                nbins=30,
                title="Cost per Unit Distribution",
                labels={
                    "CostPerUnit": "Cost per Unit ($)",
                },
            )

            plotly_layout(fig)

            st.plotly_chart(
                fig,
                use_container_width=True,
            )


    # =============================================================================
    # TAB 5 — DATA EXPLORER
    # =============================================================================

    with tab_data:

        section_header(
            "Data Explorer",
            "Inspect the filtered manufacturing records used by the dashboard.",
        )

        # ---------------------------------------------------------------------
        # Dataset statistics
        # ---------------------------------------------------------------------

        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

        with stat_col1:
            st.metric(
                "Rows",
                f"{len(filtered):,}",
            )

        with stat_col2:
            st.metric(
                "Columns",
                f"{len(filtered.columns):,}",
            )

        with stat_col3:
            st.metric(
                "Missing Values",
                f"{filtered.isna().sum().sum():,}",
            )

        with stat_col4:
            st.metric(
                "Duplicate Rows",
                f"{filtered.duplicated().sum():,}",
            )


        # ---------------------------------------------------------------------
        # Column selector
        # ---------------------------------------------------------------------

        selected_columns = st.multiselect(
            "Select columns to display",
            options=filtered.columns.tolist(),
            default=filtered.columns.tolist(),
        )

        if selected_columns:

            st.dataframe(
                filtered[selected_columns],
                use_container_width=True,
                height=550,
            )


        # ---------------------------------------------------------------------
        # Download
        # ---------------------------------------------------------------------

        csv_data = filtered.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Filtered Data",
            data=csv_data,
            file_name="manufacturing_filtered_data.csv",
            mime="text/csv",
        )


        # ---------------------------------------------------------------------
        # Missing values
        # ---------------------------------------------------------------------

        with st.expander("🔍 Data Quality Check"):

            missing = (
                filtered.isna()
                .sum()
                .reset_index()
            )

            missing.columns = [
                "Column",
                "Missing Values",
            ]

            missing["Missing %"] = (
                missing["Missing Values"]
                / len(filtered)
                * 100
            )

            missing = missing[
                missing["Missing Values"] > 0
            ].sort_values(
                "Missing Values",
                ascending=False,
            )

            if missing.empty:

                st.success(
                    "No missing values were found in the filtered dataset."
                )

            else:

                st.dataframe(
                    missing,
                    use_container_width=True,
                )


    # =============================================================================
    # FOOTER
    # =============================================================================

    st.divider()

    st.caption(
        f"Manufacturing Quality & Operational Performance Dashboard "
        f"• {len(filtered):,} filtered records • "
        f"{len(df.columns)} variables"
    )


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()