"""
visualization.py
----------------
Matplotlib + Seaborn chart functions for the logistics project.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid", palette="Set2")
plt.rcParams["figure.figsize"] = (10, 5)
plt.rcParams["axes.titlesize"] = 13
plt.rcParams["axes.labelsize"] = 11


def _finish(title, xlabel, ylabel, rotate=0):
    """Helper to apply consistent chart styling."""
    plt.title(title, fontweight="bold")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if rotate:
        plt.xticks(rotation=rotate, ha="right")
    plt.tight_layout()


# ---------- DELIVERY ----------

def plot_delivery_status(df):
    """Bar chart of delivery status counts."""
    counts = df["delivery_status"].value_counts()
    ax = sns.barplot(x=counts.index, y=counts.values, palette="Set2")
    for i, v in enumerate(counts.values):
        ax.text(i, v, str(v), ha="center", va="bottom")
    _finish("Delivery Status Distribution", "Status", "Number of Orders")
    plt.show()


def plot_monthly_orders(df):
    """Line chart of monthly order volume."""
    tmp = df.copy()
    tmp["order_month"] = pd.to_datetime(tmp["order_date"]).dt.to_period("M").astype(str)
    monthly = tmp.groupby("order_month").size()
    plt.plot(monthly.index, monthly.values, marker="o")
    _finish("Monthly Order Trend", "Month", "Orders", rotate=45)
    plt.show()


def plot_monthly_delivery_performance(df):
    """Monthly on-time vs delayed counts."""
    tmp = df.copy()
    tmp["order_month"] = pd.to_datetime(tmp["order_date"]).dt.to_period("M").astype(str)
    grp = tmp.groupby(["order_month", "delivery_status"]).size().unstack(fill_value=0)
    grp.plot(kind="bar", stacked=True, colormap="Set2")
    _finish("Monthly Delivery Performance", "Month", "Orders", rotate=45)
    plt.show()


# ---------- DELAY ----------

def plot_delay_by_warehouse(df):
    """Bar chart of delay percentage by warehouse."""
    grp = df.groupby("warehouse")["on_time_flag"].apply(
        lambda s: (1 - s.mean()) * 100
    ).sort_values(ascending=False)
    ax = sns.barplot(x=grp.index, y=grp.values, palette="Reds_r")
    for i, v in enumerate(grp.values):
        ax.text(i, v, f"{v:.1f}%", ha="center", va="bottom")
    _finish("Delay Percentage by Warehouse", "Warehouse", "Delay %")
    plt.show()


def plot_delay_by_shipping_mode(df):
    """Bar chart of delay percentage by shipping mode."""
    grp = df.groupby("shipping_mode")["on_time_flag"].apply(
        lambda s: (1 - s.mean()) * 100
    ).sort_values(ascending=False)
    ax = sns.barplot(x=grp.index, y=grp.values, palette="Oranges_r")
    for i, v in enumerate(grp.values):
        ax.text(i, v, f"{v:.1f}%", ha="center", va="bottom")
    _finish("Delay Percentage by Shipping Mode", "Shipping Mode", "Delay %")
    plt.show()


def plot_delay_by_route(df):
    """Top 10 routes by delay percentage."""
    grp = df.groupby(["origin_city", "destination_city"])["on_time_flag"].apply(
        lambda s: (1 - s.mean()) * 100
    ).reset_index()
    grp["route"] = grp["origin_city"] + " -> " + grp["destination_city"]
    grp = grp.sort_values("on_time_flag", ascending=False).head(10)
    ax = sns.barplot(x="on_time_flag", y="route", data=grp, palette="Reds_r")
    _finish("Top 10 Routes by Delay %", "Delay %", "Route")
    plt.show()


def plot_delay_distribution(df):
    """Histogram of delay_days."""
    sns.histplot(df["delay_days"].dropna(), bins=30, kde=True, color="coral")
    _finish("Delay Days Distribution", "Delay Days", "Frequency")
    plt.show()


# ---------- COST ----------

def plot_cost_by_shipping_mode(df):
    """Average logistics cost by shipping mode."""
    grp = df.groupby("shipping_mode")["total_logistics_cost"].mean().sort_values(ascending=False)
    ax = sns.barplot(x=grp.index, y=grp.values, palette="Blues_r")
    for i, v in enumerate(grp.values):
        ax.text(i, v, f"{v:.0f}", ha="center", va="bottom")
    _finish("Average Logistics Cost by Shipping Mode", "Shipping Mode", "Avg Cost")
    plt.show()


def plot_cost_by_route(df):
    """Top 10 routes by average logistics cost."""
    grp = df.groupby(["origin_city", "destination_city"])["total_logistics_cost"].mean().reset_index()
    grp["route"] = grp["origin_city"] + " -> " + grp["destination_city"]
    grp = grp.sort_values("total_logistics_cost", ascending=False).head(10)
    sns.barplot(x="total_logistics_cost", y="route", data=grp, palette="Blues_r")
    _finish("Top 10 Routes by Avg Logistics Cost", "Avg Cost", "Route")
    plt.show()


def plot_cost_trend(df):
    """Monthly total logistics cost trend."""
    tmp = df.copy()
    tmp["order_month"] = pd.to_datetime(tmp["order_date"]).dt.to_period("M").astype(str)
    grp = tmp.groupby("order_month")["total_logistics_cost"].sum()
    plt.plot(grp.index, grp.values, marker="o", color="teal")
    _finish("Monthly Logistics Cost Trend", "Month", "Total Cost", rotate=45)
    plt.show()


# ---------- WAREHOUSE ----------

def plot_orders_by_warehouse(df):
    """Orders per warehouse."""
    counts = df["warehouse"].value_counts()
    ax = sns.barplot(x=counts.index, y=counts.values, palette="Set3")
    for i, v in enumerate(counts.values):
        ax.text(i, v, str(v), ha="center", va="bottom")
    _finish("Orders by Warehouse", "Warehouse", "Orders")
    plt.show()


def plot_processing_time_by_warehouse(df):
    """Average warehouse processing hours."""
    grp = df.groupby("warehouse")["warehouse_processing_hours"].mean().sort_values(ascending=False)
    ax = sns.barplot(x=grp.index, y=grp.values, palette="Purples_r")
    for i, v in enumerate(grp.values):
        ax.text(i, v, f"{v:.2f}", ha="center", va="bottom")
    _finish("Average Processing Time by Warehouse", "Warehouse", "Hours")
    plt.show()


# ---------- PARTNER ----------

def plot_shipments_by_partner(df):
    """Shipments per delivery partner."""
    counts = df["delivery_partner"].value_counts()
    ax = sns.barplot(x=counts.index, y=counts.values, palette="Set2")
    for i, v in enumerate(counts.values):
        ax.text(i, v, str(v), ha="center", va="bottom")
    _finish("Shipments by Delivery Partner", "Partner", "Shipments")
    plt.show()


def plot_partner_delivery_performance(df):
    """On-time % by delivery partner."""
    grp = df.groupby("delivery_partner")["on_time_flag"].mean().sort_values(ascending=False) * 100
    ax = sns.barplot(x=grp.index, y=grp.values, palette="Greens_r")
    for i, v in enumerate(grp.values):
        ax.text(i, v, f"{v:.1f}%", ha="center", va="bottom")
    _finish("On-Time % by Delivery Partner", "Partner", "On-Time %")
    plt.show()


def plot_partner_cost(df):
    """Average logistics cost by delivery partner."""
    grp = df.groupby("delivery_partner")["total_logistics_cost"].mean().sort_values(ascending=False)
    ax = sns.barplot(x=grp.index, y=grp.values, palette="Blues_r")
    for i, v in enumerate(grp.values):
        ax.text(i, v, f"{v:.0f}", ha="center", va="bottom")
    _finish("Average Cost by Delivery Partner", "Partner", "Avg Cost")
    plt.show()


# ---------- CUSTOMER ----------

def plot_customer_rating_distribution(df):
    """Distribution of customer ratings."""
    sns.countplot(x="customer_rating", data=df, palette="coolwarm")
    _finish("Customer Rating Distribution", "Rating", "Count")
    plt.show()


def plot_rating_by_delivery_status(df):
    """Average customer rating by delivery status."""
    grp = df.groupby("delivery_status")["customer_rating"].mean().sort_values(ascending=False)
    ax = sns.barplot(x=grp.index, y=grp.values, palette="coolwarm")
    for i, v in enumerate(grp.values):
        ax.text(i, v, f"{v:.2f}", ha="center", va="bottom")
    _finish("Average Customer Rating by Delivery Status", "Delivery Status", "Avg Rating")
    plt.show()
    