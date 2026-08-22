"""
Airline Disruption Detection & Recovery System — Interactive Dashboard
========================================================================
Cross-filtering Streamlit app. Unlike the static Plotly dashboards
(GitHub Pages), selecting an airport or date range here updates every
chart together, live.

Data: reads two small pre-aggregated parquet files directly from the
Hugging Face Hub dataset repo (no auth needed — public dataset).
  - streamlit_ops_aggregate.parquet         (historical KPIs, all years)
  - streamlit_predictive_aggregate.parquet  (model output, 2024 only)
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Airline Disruption Detection — Interactive Dashboard",
    page_icon="✈️",
    layout="wide",
)

NAVY, ALERT_RED, LIGHT_BLUE = "#1e3a8a", "#dc2626", "#93c5fd"
GRID_COLOR, TEXT_MUTED = "#e2e8f0", "#64748b"
FONT_FAMILY = "Helvetica Neue, Arial, sans-serif"

HF_BASE = "https://huggingface.co/datasets/Dev123Hug456Face/airline-disruption-data/resolve/main"

# Approximate coordinates for each hub airport (for the geographic map)
AIRPORT_COORDS = {
    "JFK": (40.6413, -73.7781),
    "ORD": (41.9742, -87.9073),
    "ATL": (33.6407, -84.4277),
    "LAX": (33.9416, -118.4085),
    "DFW": (32.8998, -97.0403),
    "SFO": (37.6213, -122.3790),
    "EWR": (40.6895, -74.1745),
    "MIA": (25.7959, -80.2870),
    "SEA": (47.4502, -122.3088),
    "BOS": (42.3656, -71.0096),
}

# ── Data loading (cached so it only downloads once per session) ────────
@st.cache_data
def load_data():
    ops = pd.read_parquet(f"{HF_BASE}/streamlit_ops_aggregate.parquet")
    ops["FlightDate"] = pd.to_datetime(ops["FlightDate"])

    pred = pd.read_parquet(f"{HF_BASE}/streamlit_predictive_aggregate.parquet")
    pred["FlightDate"] = pd.to_datetime(pred["FlightDate"])

    return ops, pred


with st.spinner("Loading data..."):
    ops_df, pred_df = load_data()

ALL_AIRPORTS = sorted(ops_df["Origin"].unique().tolist())

# ── Sidebar filters (these drive every chart below) ─────────────────────
st.sidebar.title("✈️ Filters")

selected_airports = st.sidebar.multiselect(
    "Airports", options=ALL_AIRPORTS, default=ALL_AIRPORTS
)

min_date, max_date = ops_df["FlightDate"].min(), ops_df["FlightDate"].max()
date_range = st.sidebar.date_input(
    "Date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)
if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = min_date, max_date

st.sidebar.markdown("---")
st.sidebar.caption(
    "Data: BTS On-Time Performance + IEM historical weather, "
    "10 U.S. hub airports, 2022–2024. [GitHub repo](https://github.com/Deva2013/airline-disruption-management-system)"
)

if not selected_airports:
    st.warning("Select at least one airport in the sidebar to see the dashboard.")
    st.stop()

# ── Apply filters ─────────────────────────────────────────────────────────
ops_filtered = ops_df[
    ops_df["Origin"].isin(selected_airports)
    & (ops_df["FlightDate"] >= start_date)
    & (ops_df["FlightDate"] <= end_date)
]
pred_filtered = pred_df[
    pred_df["Origin"].isin(selected_airports)
    & (pred_df["FlightDate"] >= start_date)
    & (pred_df["FlightDate"] <= end_date)
]

if len(ops_filtered) == 0:
    st.warning("No flights match the current filters. Try widening the date range or airport selection.")
    st.stop()

# ── Header ────────────────────────────────────────────────────────────────
st.title("Airline Disruption Detection & Recovery System")
st.caption("Interactive dashboard — filters in the sidebar update every chart below")

# ── KPI row (recomputed live from filtered data) ─────────────────────────
total_flights = ops_filtered["TotalFlights"].sum()
delay_rate = ops_filtered["DelayedFlights"].sum() / total_flights * 100
cancel_rate = ops_filtered["CancelledFlights"].sum() / total_flights * 100
cascade_rate = ops_filtered["CascadeRiskFlights"].sum() / total_flights * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Flights", f"{total_flights:,.0f}")
k2.metric("Delay Rate (≥15 min)", f"{delay_rate:.1f}%")
k3.metric("Cancellation Rate", f"{cancel_rate:.1f}%")
k4.metric("Cascade-Risk Flights", f"{cascade_rate:.1f}%")

st.markdown("---")

# ── Tabs: Operations vs Predictive Risk ─────────────────────────────────
tab1, tab2 = st.tabs(["📊 Operations", "🎯 Predictive Risk (2024)"])

with tab1:
    # ── Geographic map: delay rate + volume across the 10 hub airports ──
    map_data = (
        ops_filtered.groupby("Origin")
        .agg(TotalFlights=("TotalFlights", "sum"), DelayedFlights=("DelayedFlights", "sum"))
        .assign(DelayRate=lambda d: d["DelayedFlights"] / d["TotalFlights"] * 100)
        .reset_index()
    )
    map_data["Lat"] = map_data["Origin"].map(lambda a: AIRPORT_COORDS[a][0])
    map_data["Lon"] = map_data["Origin"].map(lambda a: AIRPORT_COORDS[a][1])
    # Marker size scaled by sqrt of volume so the busiest hub doesn't visually swamp the rest
    map_data["MarkerSize"] = 18 + 32 * np.sqrt(map_data["TotalFlights"] / map_data["TotalFlights"].max())

    fig_map = go.Figure(go.Scattergeo(
        lon=map_data["Lon"], lat=map_data["Lat"],
        text=map_data.apply(
            lambda r: f"<b>{r['Origin']}</b><br>Delay rate: {r['DelayRate']:.1f}%<br>Flights: {r['TotalFlights']:,.0f}",
            axis=1,
        ),
        mode="markers",
        marker=dict(
            size=map_data["MarkerSize"],
            color=map_data["DelayRate"],
            colorscale="YlOrRd",
            cmin=0, cmax=max(30, map_data["DelayRate"].max()),
            colorbar=dict(title="Delay<br>Rate (%)", thickness=14, len=0.7),
            line=dict(color="white", width=1),
        ),
        hoverinfo="text",
    ))
    fig_map.update_layout(
        title="Hub Airports — Delay Rate (color) & Flight Volume (size)",
        geo=dict(
            scope="usa", projection_type="albers usa",
            landcolor="#f1f5f9", subunitcolor="white", countrycolor="white",
        ),
        height=460, font=dict(family=FONT_FAMILY),
        margin=dict(t=50, l=10, r=10, b=10),
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.caption("Marker size reflects flight volume (scaled), color reflects delay rate. Hover for exact figures per airport.")

    col1, col2 = st.columns(2)

    with col1:
        by_airport = (
            ops_filtered.groupby("Origin")
            .agg(TotalFlights=("TotalFlights", "sum"), DelayedFlights=("DelayedFlights", "sum"))
            .assign(DelayRate=lambda d: d["DelayedFlights"] / d["TotalFlights"] * 100)
            .sort_values("DelayRate", ascending=False)
        )
        fig1 = go.Figure(go.Bar(
            x=by_airport.index, y=by_airport["DelayRate"],
            marker_color=NAVY,
            text=[f"{v:.1f}%" for v in by_airport["DelayRate"]], textposition="outside",
        ))
        fig1.update_layout(
            title="Delay Rate by Airport", height=380,
            font=dict(family=FONT_FAMILY), plot_bgcolor="white",
            yaxis_title="Delay Rate (%)", xaxis_title="Airport",
        )
        fig1.update_xaxes(showgrid=False, showline=True, linecolor=GRID_COLOR)
        fig1.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        by_hour = (
            ops_filtered.groupby("ScheduledDepHour")
            .agg(TotalFlights=("TotalFlights", "sum"), DelayedFlights=("DelayedFlights", "sum"))
            .assign(DelayRate=lambda d: d["DelayedFlights"] / d["TotalFlights"] * 100)
        )
        fig2 = go.Figure(go.Bar(
            x=by_hour.index, y=by_hour["DelayRate"], marker_color=LIGHT_BLUE,
        ))
        fig2.update_layout(
            title="Delay Rate by Scheduled Hour", height=380,
            font=dict(family=FONT_FAMILY), plot_bgcolor="white",
            yaxis_title="Delay Rate (%)", xaxis_title="Scheduled Departure Hour (24hr)",
        )
        fig2.update_xaxes(showgrid=False, showline=True, linecolor=GRID_COLOR)
        fig2.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
        st.plotly_chart(fig2, use_container_width=True)

    # Monthly trend, full width
    monthly = (
        ops_filtered.assign(Month=ops_filtered["FlightDate"].dt.to_period("M").dt.to_timestamp())
        .groupby("Month")
        .agg(TotalFlights=("TotalFlights", "sum"), DelayedFlights=("DelayedFlights", "sum"))
        .assign(DelayRate=lambda d: d["DelayedFlights"] / d["TotalFlights"] * 100)
        .reset_index()
    )
    fig3 = go.Figure(go.Scatter(
        x=monthly["Month"], y=monthly["DelayRate"], mode="lines+markers",
        line=dict(color=NAVY, width=3), marker=dict(color=NAVY, size=6),
        fill="tozeroy", fillcolor="rgba(30,58,138,0.08)",
    ))
    fig3.update_layout(
        title="Monthly Delay Rate Trend", height=350,
        font=dict(family=FONT_FAMILY), plot_bgcolor="white",
        yaxis_title="Delay Rate (%)", xaxis_title="Month",
    )
    fig3.update_xaxes(showgrid=False, showline=True, linecolor=GRID_COLOR)
    fig3.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    if len(pred_filtered) == 0:
        st.info("No 2024 flights match the current filters — the predictive model was evaluated on 2024 data only.")
    else:
        total_pred = pred_filtered["TotalFlights"].sum()
        actual_rate = pred_filtered["ActualDelayed"].sum() / total_pred * 100
        flagged_rate = pred_filtered["FlaggedHighRisk"].sum() / total_pred * 100

        c1, c2 = st.columns(2)
        c1.metric("Actual Delay Rate (2024)", f"{actual_rate:.1f}%")
        c2.metric("Flagged High-Risk (model)", f"{flagged_rate:.1f}%")

        by_airport_pred = (
            pred_filtered.groupby("Origin")
            .agg(
                TotalFlights=("TotalFlights", "sum"),
                ActualDelayed=("ActualDelayed", "sum"),
                FlaggedHighRisk=("FlaggedHighRisk", "sum"),
            )
            .assign(
                ActualRate=lambda d: d["ActualDelayed"] / d["TotalFlights"] * 100,
                FlaggedRate=lambda d: d["FlaggedHighRisk"] / d["TotalFlights"] * 100,
            )
            .sort_values("ActualRate", ascending=False)
        )

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=by_airport_pred.index, y=by_airport_pred["ActualRate"],
            name="Actual delay rate", marker_color=NAVY,
        ))
        fig4.add_trace(go.Bar(
            x=by_airport_pred.index, y=by_airport_pred["FlaggedRate"],
            name="Flagged high-risk (model)", marker_color=LIGHT_BLUE,
        ))
        fig4.update_layout(
            title="Actual vs. Flagged Delay Rate by Airport", height=420,
            font=dict(family=FONT_FAMILY), plot_bgcolor="white",
            yaxis_title="Rate (%)", xaxis_title="Airport",
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        )
        fig4.update_xaxes(showgrid=False, showline=True, linecolor=GRID_COLOR)
        fig4.update_yaxes(showgrid=True, gridcolor=GRID_COLOR)
        st.plotly_chart(fig4, use_container_width=True)

        st.caption(
            "Model: XGBoost, 0.72 ROC-AUC on the full 2024 held-out test set (across all airports). "
            "Flagged rates run higher than actual — a deliberate tradeoff from tuning the model toward "
            "catching more real delays (recall) rather than minimizing false alarms. What matters is the "
            "ranking holds: airports with worse actual performance also get flagged more."
        )

st.markdown("---")
st.caption(
    "Static, non-interactive versions of these dashboards are also published via GitHub Pages — "
    "see the [project README](https://github.com/Deva2013/airline-disruption-management-system) for links."
)
