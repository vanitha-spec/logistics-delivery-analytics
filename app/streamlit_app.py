"""
streamlit_app.py
----------------
Interactive Streamlit dashboard for the logistics analytics project.

Run with:
    streamlit run app/streamlit_app.py
"""

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.business_analysis import (
    calculate_total_orders, calculate_total_delivered, calculate_total_delayed,
    calculate_on_time_percentage, calculate_average_delivery_days,
    calculate_total_logistics_cost, calculate_average_logistics_cost,
    calculate_damage_rate, calculate_return_rate, calculate_average_customer_rating,
    analyze_route_performance, analyze_route_delays, analyze_route_cost,
    analyze_warehouse_performance, analyze_warehouse_delays,
    analyze_warehouse_processing_time,
    analyze_shipping_mode, analyze_shipping_mode_cost, analyze_shipping_mode_delays,
    analyze_delivery_partner, analyze_partner_cost, analyze_partner_delays,
    analyze_partner_damage_rate,
)

CLEANED_PATH = os.path.join("data", "cleaned", "logistics_cleaned.csv")

st.set_page_config(page_title="Logistics Analytics", layout="wide")
sns.set_theme(style="whitegrid")


@st.cache_data
def load_dashboard_data():
    """Load the cleaned dataset for the dashboard."""
    if not os.path.exists(CLEANED_PATH):
        st.error(
            f"Cleaned data not found at {CLEANED_PATH}. "
            "Please run `python run_pipeline.py` first."
        )
        st.stop()
    df = pd.read_csv(CLEANED_PATH, parse_dates=[
        "order_date", "dispatch_date",
        "expected_delivery_date", "actual_delivery_date"
    ])
    return df


def show_sidebar_filters(df):
    """Render sidebar filters and return the filtered dataframe."""
    st.sidebar.header("🔎 Filters")

    def multiselect(label, col):
        opts = sorted(df[col].dropna().unique().tolist())
        return st.sidebar.multiselect(label, opts, default=[])

    wh = multiselect("Warehouse", "warehouse")
    oc = multiselect("Origin City", "origin_city")
    dc = multiselect("Destination City", "destination_city")
    sm = multiselect("Shipping Mode", "shipping_mode")
    dp = multiselect("Delivery Partner", "delivery_partner")
    ds = multiselect("Delivery Status", "delivery_status")

    fdf = df.copy()
    if wh: fdf = fdf[fdf["warehouse"].isin(wh)]
    if oc: fdf = fdf[fdf["origin_city"].isin(oc)]
    if dc: fdf = fdf[fdf["destination_city"].isin(dc)]
    if sm: fdf = fdf[fdf["shipping_mode"].isin(sm)]
    if dp: fdf = fdf[fdf["delivery_partner"].isin(dp)]
    if ds: fdf = fdf[fdf["delivery_status"].isin(ds)]

    st.sidebar.markdown(f"**Filtered rows:** {len(fdf):,}")
    return fdf


def show_overview(df):
    """Executive overview KPIs."""
    st.header("📊 Executive Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Orders", f"{calculate_total_orders(df):,}")
    c2.metric("Delivered", f"{calculate_total_delivered(df):,}")
    c3.metric("Delayed", f"{calculate_total_delayed(df):,}")
    c4.metric("On-Time %", f"{calculate_on_time_percentage(df)}%")

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Avg Delivery Days", f"{calculate_average_delivery_days(df)}")
    c6.metric("Total Logistics Cost", f"₹{calculate_total_logistics_cost(df):,.0f}")
    c7.metric("Avg Logistics Cost", f"₹{calculate_average_logistics_cost(df):,.0f}")
    c8.metric("Avg Customer Rating", f"{calculate_average_customer_rating(df)}")

    st.subheader("Delivery Status Distribution")
    fig, ax = plt.subplots()
    df["delivery_status"].value_counts().plot(kind="bar", ax=ax, color="#4C72B0")
    ax.set_xlabel("Status"); ax.set_ylabel("Orders")
    plt.xticks(rotation=0)
    st.pyplot(fig)


def show_delivery_analysis(df):
    """Delivery and delay analysis."""
    st.header("🚚 Delivery Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Delay % by Warehouse")
        grp = df.groupby("warehouse")["on_time_flag"].apply(lambda s: (1 - s.mean()) * 100)
        st.bar_chart(grp)

    with col2:
        st.subheader("Delay % by Shipping Mode")
        grp = df.groupby("shipping_mode")["on_time_flag"].apply(lambda s: (1 - s.mean()) * 100)
        st.bar_chart(grp)

    st.subheader("Delay Days Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["delay_days"].dropna(), bins=30, kde=True, ax=ax, color="coral")
    st.pyplot(fig)

    st.subheader("Monthly Order Trend")
    tmp = df.copy()
    tmp["order_month"] = pd.to_datetime(tmp["order_date"]).dt.to_period("M").astype(str)
    st.line_chart(tmp.groupby("order_month").size())


def show_route_analysis(df):
    """Route analysis: volume, delays, costs."""
    st.header("🛣️ Route Analysis")

    st.subheader("Top 10 Routes by Volume")
    r = analyze_route_performance(df).head(10)
    r["route"] = r["origin_city"] + " → " + r["destination_city"]
    st.dataframe(r[["route", "total_shipments", "avg_delay_days", "on_time_pct"]])

    st.subheader("Top 10 Routes by Delay %")
    rd = analyze_route_delays(df).head(10)
    rd["route"] = rd["origin_city"] + " → " + rd["destination_city"]
    st.dataframe(rd[["route", "total_shipments", "delay_pct"]])

    st.subheader("Top 10 Routes by Cost")
    rc = analyze_route_cost(df).head(10)
    rc["route"] = rc["origin_city"] + " → " + rc["destination_city"]
    st.dataframe(rc[["route", "total_logistics_cost", "avg_cost_per_km"]])


def show_warehouse_analysis(df):
    """Warehouse analysis."""
    st.header("🏭 Warehouse Analysis")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Orders per Warehouse")
        st.bar_chart(df["warehouse"].value_counts())
    with col2:
        st.subheader("Delay % by Warehouse")
        grp = df.groupby("warehouse")["on_time_flag"].apply(lambda s: (1 - s.mean()) * 100)
        st.bar_chart(grp)

    st.subheader("Warehouse Processing Time")
    st.dataframe(analyze_warehouse_processing_time(df))

    st.subheader("Warehouse Delay Details")
    st.dataframe(analyze_warehouse_delays(df))


def show_cost_analysis(df):
    """Cost analysis."""
    st.header("💰 Cost Analysis")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Logistics Cost", f"₹{calculate_total_logistics_cost(df):,.0f}")
    c2.metric("Avg Logistics Cost", f"₹{calculate_average_logistics_cost(df):,.0f}")
    c3.metric("Avg Cost per KM", f"₹{df['cost_per_km'].mean():.2f}")

    st.subheader("Average Cost by Shipping Mode")
    st.dataframe(analyze_shipping_mode_cost(df))

    st.subheader("Monthly Cost Trend")
    tmp = df.copy()
    tmp["order_month"] = pd.to_datetime(tmp["order_date"]).dt.to_period("M").astype(str)
    st.line_chart(tmp.groupby("order_month")["total_logistics_cost"].sum())


def show_partner_analysis(df):
    """Delivery partner analysis."""
    st.header("🤝 Delivery Partner Analysis")

    st.subheader("Partner Shipments")
    st.bar_chart(df["delivery_partner"].value_counts())

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("On-Time % by Partner")
        grp = df.groupby("delivery_partner")["on_time_flag"].mean() * 100
        st.bar_chart(grp)
    with col2:
        st.subheader("Damage Rate by Partner")
        st.dataframe(analyze_partner_damage_rate(df))

    st.subheader("Partner Cost Comparison")
    st.dataframe(analyze_partner_cost(df))


def main():
    """Main entry point for the Streamlit dashboard."""
    st.title("📦 Logistics Delivery Performance & Cost Analytics")
    st.markdown("Interactive dashboard for operations and management.")

    df = load_dashboard_data()
    fdf = show_sidebar_filters(df)

    if len(fdf) == 0:
        st.warning("No data matches the selected filters.")
        return

    page = st.sidebar.radio(
        "Navigation",
        ["Executive Overview", "Delivery Analysis", "Route Analysis",
         "Warehouse Analysis", "Cost Analysis", "Partner Analysis"]
    )

    if page == "Executive Overview":
        show_overview(fdf)
    elif page == "Delivery Analysis":
        show_delivery_analysis(fdf)
    elif page == "Route Analysis":
        show_route_analysis(fdf)
    elif page == "Warehouse Analysis":
        show_warehouse_analysis(fdf)
    elif page == "Cost Analysis":
        show_cost_analysis(fdf)
    elif page == "Partner Analysis":
        show_partner_analysis(fdf)


if __name__ == "__main__":
    main()
    