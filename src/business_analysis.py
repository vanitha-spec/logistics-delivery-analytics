"""
business_analysis.py
--------------------
Reusable KPI and business analysis functions for the logistics dataset.
All function names are mandated by the assignment specification.
"""

import pandas as pd
import numpy as np


# =====================================================================
# BASIC KPIs
# =====================================================================

def calculate_total_orders(df):
    """Return the number of unique orders in the dataset."""
    return int(df["order_id"].nunique())


def calculate_total_delivered(df):
    """Return the number of delivered orders."""
    return int((df["delivery_status"] == "Delivered").sum())


def calculate_total_delayed(df):
    """Return the number of delayed orders."""
    return int((df["delivery_status"] == "Delayed").sum())


def calculate_on_time_percentage(df):
    """On-Time Deliveries / Delivered Orders * 100."""
    delivered = df[df["delivery_status"] == "Delivered"]
    if len(delivered) == 0:
        return 0.0
    on_time = (delivered["delay_days"] <= 0).sum()
    return round(on_time / len(delivered) * 100, 2)


def calculate_average_delivery_days(df):
    """Average of delivery_days."""
    return round(df["delivery_days"].mean(), 2)


def calculate_average_delay_days(df):
    """Average delay_days for delayed shipments only."""
    delayed = df[df["delay_days"] > 0]
    if len(delayed) == 0:
        return 0.0
    return round(delayed["delay_days"].mean(), 2)


# =====================================================================
# COST KPIs
# =====================================================================

def calculate_total_shipping_cost(df):
    """Total shipping cost."""
    return round(df["shipping_cost"].sum(), 2)


def calculate_average_shipping_cost(df):
    """Average shipping cost per order."""
    return round(df["shipping_cost"].mean(), 2)


def calculate_total_fuel_cost(df):
    """Total fuel cost."""
    return round(df["fuel_cost"].sum(), 2)


def calculate_total_logistics_cost(df):
    """Total logistics cost = shipping + fuel."""
    return round(df["total_logistics_cost"].sum(), 2)


def calculate_average_logistics_cost(df):
    """Average logistics cost per order."""
    return round(df["total_logistics_cost"].mean(), 2)


def calculate_average_cost_per_km(df):
    """Average cost per km."""
    return round(df["cost_per_km"].mean(), 2)


# =====================================================================
# ROUTE ANALYSIS
# =====================================================================

def analyze_route_performance(df):
    """Route-level performance summary (count, avg delay, on-time %)."""
    grp = df.groupby(["origin_city", "destination_city"]).agg(
        total_shipments=("order_id", "count"),
        avg_delay_days=("delay_days", "mean"),
        avg_delivery_days=("delivery_days", "mean"),
    ).reset_index()
    grp["on_time_pct"] = df.groupby(
        ["origin_city", "destination_city"]
    )["on_time_flag"].mean().values * 100
    grp = grp.sort_values("total_shipments", ascending=False)
    return grp


def analyze_route_cost(df):
    """Route-level cost summary."""
    grp = df.groupby(["origin_city", "destination_city"]).agg(
        total_shipments=("order_id", "count"),
        total_logistics_cost=("total_logistics_cost", "sum"),
        avg_logistics_cost=("total_logistics_cost", "mean"),
        avg_cost_per_km=("cost_per_km", "mean"),
    ).reset_index()
    grp = grp.sort_values("total_logistics_cost", ascending=False)
    return grp


def analyze_route_delays(df):
    """Route-level delay summary."""
    grp = df.groupby(["origin_city", "destination_city"]).agg(
        total_shipments=("order_id", "count"),
        avg_delay_days=("delay_days", "mean"),
        max_delay_days=("delay_days", "max"),
    ).reset_index()
    grp["delay_pct"] = df.groupby(
        ["origin_city", "destination_city"]
    )["on_time_flag"].apply(lambda s: (1 - s.mean()) * 100).values
    grp = grp.sort_values("delay_pct", ascending=False)
    return grp


# =====================================================================
# WAREHOUSE ANALYSIS
# =====================================================================

def analyze_warehouse_performance(df):
    """Warehouse-level order volume and performance."""
    grp = df.groupby("warehouse").agg(
        total_orders=("order_id", "count"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_delay_days=("delay_days", "mean"),
    ).reset_index()
    grp["on_time_pct"] = df.groupby("warehouse")["on_time_flag"].mean().values * 100
    grp = grp.sort_values("total_orders", ascending=False)
    return grp


def analyze_warehouse_delays(df):
    """Warehouse-level delay percentage."""
    grp = df.groupby("warehouse").agg(
        total_orders=("order_id", "count"),
        delayed_orders=("on_time_flag", lambda s: (s == 0).sum()),
    ).reset_index()
    grp["delay_pct"] = (grp["delayed_orders"] / grp["total_orders"] * 100).round(2)
    grp = grp.sort_values("delay_pct", ascending=False)
    return grp


def analyze_warehouse_processing_time(df):
    """Warehouse-level processing time."""
    grp = df.groupby("warehouse").agg(
        avg_processing_hours=("warehouse_processing_hours", "mean"),
        median_processing_hours=("warehouse_processing_hours", "median"),
        max_processing_hours=("warehouse_processing_hours", "max"),
        total_orders=("order_id", "count"),
    ).reset_index()
    grp = grp.sort_values("avg_processing_hours", ascending=False)
    return grp


# =====================================================================
# SHIPPING MODE ANALYSIS
# =====================================================================

def analyze_shipping_mode(df):
    """Shipping mode frequency and performance."""
    grp = df.groupby("shipping_mode").agg(
        total_shipments=("order_id", "count"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_delay_days=("delay_days", "mean"),
    ).reset_index()
    grp["on_time_pct"] = df.groupby("shipping_mode")["on_time_flag"].mean().values * 100
    grp = grp.sort_values("total_shipments", ascending=False)
    return grp


def analyze_shipping_mode_cost(df):
    """Shipping mode cost analysis."""
    grp = df.groupby("shipping_mode").agg(
        total_shipments=("order_id", "count"),
        avg_shipping_cost=("shipping_cost", "mean"),
        avg_logistics_cost=("total_logistics_cost", "mean"),
        avg_cost_per_km=("cost_per_km", "mean"),
    ).reset_index()
    grp = grp.sort_values("avg_logistics_cost", ascending=False)
    return grp


def analyze_shipping_mode_delays(df):
    """Shipping mode delay percentage."""
    grp = df.groupby("shipping_mode").agg(
        total_shipments=("order_id", "count"),
        delayed_shipments=("on_time_flag", lambda s: (s == 0).sum()),
    ).reset_index()
    grp["delay_pct"] = (grp["delayed_shipments"] / grp["total_shipments"] * 100).round(2)
    grp = grp.sort_values("delay_pct", ascending=False)
    return grp


# =====================================================================
# DELIVERY PARTNER ANALYSIS
# =====================================================================

def analyze_delivery_partner(df):
    """Partner shipment volume and performance."""
    grp = df.groupby("delivery_partner").agg(
        total_shipments=("order_id", "count"),
        avg_delivery_days=("delivery_days", "mean"),
        avg_delay_days=("delay_days", "mean"),
    ).reset_index()
    grp["on_time_pct"] = df.groupby("delivery_partner")["on_time_flag"].mean().values * 100
    grp = grp.sort_values("total_shipments", ascending=False)
    return grp


def analyze_partner_cost(df):
    """Partner cost comparison."""
    grp = df.groupby("delivery_partner").agg(
        total_shipments=("order_id", "count"),
        avg_shipping_cost=("shipping_cost", "mean"),
        avg_logistics_cost=("total_logistics_cost", "mean"),
    ).reset_index()
    grp = grp.sort_values("avg_logistics_cost", ascending=False)
    return grp


def analyze_partner_delays(df):
    """Partner delay percentage."""
    grp = df.groupby("delivery_partner").agg(
        total_shipments=("order_id", "count"),
        delayed_shipments=("on_time_flag", lambda s: (s == 0).sum()),
    ).reset_index()
    grp["delay_pct"] = (grp["delayed_shipments"] / grp["total_shipments"] * 100).round(2)
    grp = grp.sort_values("delay_pct", ascending=False)
    return grp


def analyze_partner_damage_rate(df):
    """Partner damage rate."""
    grp = df.groupby("delivery_partner").agg(
        total_shipments=("order_id", "count"),
        damaged_shipments=("damage_flag", lambda s: (s == "Yes").sum()),
    ).reset_index()
    grp["damage_rate"] = (grp["damaged_shipments"] / grp["total_shipments"] * 100).round(2)
    grp = grp.sort_values("damage_rate", ascending=False)
    return grp


# =====================================================================
# CUSTOMER ANALYSIS
# =====================================================================

def calculate_average_customer_rating(df):
    """Average customer rating."""
    return round(df["customer_rating"].mean(), 2)


def calculate_return_rate(df):
    """Returned Shipments / Total Shipments * 100."""
    if "return_flag" not in df.columns:
        return 0.0
    returns = (df["return_flag"] == "Yes").sum()
    return round(returns / len(df) * 100, 2)


def calculate_damage_rate(df):
    """Damaged Shipments / Total Shipments * 100."""
    if "damage_flag" not in df.columns:
        return 0.0
    damage = (df["damage_flag"] == "Yes").sum()
    return round(damage / len(df) * 100, 2)