"""
data_cleaner.py
---------------
Reusable cleaning pipeline for the logistics dataset.

Cleaning steps (in order):
    1. handle_missing_values
    2. remove_duplicates
    3. clean_text_columns
    4. clean_date_columns
    5. validate_numeric_columns
    6. validate_business_rules
    7. create_derived_columns
    8. clean_data (orchestrator)
    9. save_cleaned_data
"""

import os
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------

DATE_COLUMNS = [
    "order_date",
    "dispatch_date",
    "expected_delivery_date",
    "actual_delivery_date",
]

NUMERIC_COLUMNS = [
    "distance_km",
    "quantity",
    "weight_kg",
    "shipping_cost",
    "fuel_cost",
    "warehouse_processing_hours",
    "customer_rating",
]

TEXT_COLUMNS = [
    "warehouse",
    "origin_city",
    "destination_city",
    "product_category",
    "shipping_mode",
    "delivery_partner",
    "delivery_status",
    "damage_flag",
    "return_flag",
]


# ---------------------------------------------------------------------
# 1. Missing Values
# ---------------------------------------------------------------------

def handle_missing_values(df):
    """
    Handle missing values according to business rules.

    Rules
    -----
    - Drop rows missing order_id or customer_id (critical identifiers).
    - Numeric columns -> fill with median.
    - Categorical columns -> fill with mode or 'Unknown'.
    - Date columns -> leave as NaT; row-level filtering happens later.
    """
    df = df.copy()

    # Critical identifiers
    before = len(df)
    df = df.dropna(subset=["order_id", "customer_id"])
    print(f"[MissingValues] Dropped {before - len(df)} rows missing critical IDs.")

    # Numeric columns -> median
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            median_val = df[col].median()
            if pd.isna(median_val):
                median_val = 0
            df[col] = df[col].fillna(median_val)

    # Text columns -> mode or 'Unknown'
    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("object")
            mode_series = df[col].mode(dropna=True)
            fill_val = mode_series.iloc[0] if not mode_series.empty else "Unknown"
            df[col] = df[col].fillna(fill_val)

    # Date columns -> leave NaT (they are handled in clean_date_columns)
    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Fuel cost is sometimes missing -> fill with 0 (better than median skew)
    if "fuel_cost" in df.columns:
        df["fuel_cost"] = df["fuel_cost"].fillna(0)

    return df


# ---------------------------------------------------------------------
# 2. Duplicates
# ---------------------------------------------------------------------

def remove_duplicates(df):
    """
    Remove duplicate rows.

    Strategy
    --------
    - Drop fully duplicated rows.
    - Drop duplicated order_id keeping the first occurrence.
    """
    df = df.copy()

    before = len(df)
    df = df.drop_duplicates()
    print(f"[Duplicates] Removed {before - len(df)} fully duplicated rows.")

    before = len(df)
    df = df.drop_duplicates(subset=["order_id"], keep="first")
    print(f"[Duplicates] Removed {before - len(df)} duplicated order_ids.")

    return df


# ---------------------------------------------------------------------
# 3. Text Cleaning
# ---------------------------------------------------------------------

def clean_text_columns(df):
    """
    Standardise text columns.

    - Strip whitespace
    - Title-case categorical values (so 'road', 'ROAD', 'Road' become 'Road')
    - Preserve Yes/No flags in Title case
    - Preserve delivery_status in Title case
    """
    df = df.copy()

    for col in TEXT_COLUMNS:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
                .str.title()
                .replace({"Nan": "Unknown", "None": "Unknown", "": "Unknown"})
            )

    # Fix specific known inconsistencies
    if "shipping_mode" in df.columns:
        df["shipping_mode"] = df["shipping_mode"].replace(
            {"Road": "Road", "Rail": "Rail", "Air": "Air", "Express": "Express"}
        )

    if "delivery_partner" in df.columns:
        df["delivery_partner"] = df["delivery_partner"].replace(
            {"Ecom Express": "Ecom Express", "Xpressbees": "XpressBees",
             "Blue Dart": "Blue Dart", "Dtdc": "DTDC"}
        )

    return df


# ---------------------------------------------------------------------
# 4. Date Cleaning
# ---------------------------------------------------------------------

def clean_date_columns(df):
    """
    Convert date columns to datetime and enforce logical consistency.

    Rules
    -----
    - expected_delivery_date must be >= dispatch_date; otherwise set to NaT.
    - actual_delivery_date must be >= dispatch_date; otherwise set to NaT.
    """
    df = df.copy()

    for col in DATE_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # expected >= dispatch
    if {"expected_delivery_date", "dispatch_date"}.issubset(df.columns):
        mask = df["expected_delivery_date"] < df["dispatch_date"]
        df.loc[mask, "expected_delivery_date"] = pd.NaT

    # actual >= dispatch
    if {"actual_delivery_date", "dispatch_date"}.issubset(df.columns):
        mask = df["actual_delivery_date"] < df["dispatch_date"]
        df.loc[mask, "actual_delivery_date"] = pd.NaT

    return df


# ---------------------------------------------------------------------
# 5. Numeric Validation
# ---------------------------------------------------------------------

def validate_numeric_columns(df):
    """
    Validate numeric columns and clamp/clean out-of-range values.

    Rules
    -----
    - distance_km  >= 0  (negative values set to NaN -> median)
    - quantity     > 0
    - weight_kg    >= 0
    - shipping_cost >= 0  (negative values set to NaN)
    - fuel_cost    >= 0
    - warehouse_processing_hours >= 0
    - 1 <= customer_rating <= 5
    """
    df = df.copy()

    numeric_rules = {
        "distance_km": ("min", 0),
        "quantity": ("min_exclusive", 0),
        "weight_kg": ("min", 0),
        "shipping_cost": ("min", 0),
        "fuel_cost": ("min", 0),
        "warehouse_processing_hours": ("min", 0),
        "customer_rating": ("range", (1, 5)),
    }

    for col, (rule, val) in numeric_rules.items():
        if col not in df.columns:
            continue

        df[col] = pd.to_numeric(df[col], errors="coerce")

        if rule == "min":
            df.loc[df[col] < val, col] = np.nan
        elif rule == "min_exclusive":
            df.loc[df[col] <= val, col] = np.nan
        elif rule == "range":
            low, high = val
            df.loc[(df[col] < low) | (df[col] > high), col] = np.nan

        # Refill with median if we nulled anything
        if df[col].isna().any():
            median_val = df[col].median()
            if pd.isna(median_val):
                median_val = 0
            df[col] = df[col].fillna(median_val)

    return df


# ---------------------------------------------------------------------
# 6. Business Rule Validation
# ---------------------------------------------------------------------

def validate_business_rules(df):
    """
    Enforce the business rules defined in the assignment document.

    Rules
    -----
    BR-01 order_id must not be missing
    BR-02 customer_id must not be missing
    BR-03 distance_km >= 0
    BR-04 quantity > 0
    BR-05 weight_kg >= 0
    BR-06 shipping_cost >= 0
    BR-07 fuel_cost >= 0
    BR-08 1 <= customer_rating <= 5
    BR-09 dates logically consistent (handled in clean_date_columns)
    BR-10 delay_days classification (created later)
    BR-11 cost_per_km safe divide (created later)
    """
    df = df.copy()

    # Drop rows still missing critical IDs
    df = df.dropna(subset=["order_id", "customer_id"])

    # Ensure numeric sanity (re-run as a safety net)
    if "distance_km" in df.columns:
        df = df[df["distance_km"] >= 0]
    if "quantity" in df.columns:
        df = df[df["quantity"] > 0]
    if "weight_kg" in df.columns:
        df = df[df["weight_kg"] >= 0]
    if "shipping_cost" in df.columns:
        df = df[df["shipping_cost"] >= 0]
    if "fuel_cost" in df.columns:
        df = df[df["fuel_cost"] >= 0]
    if "customer_rating" in df.columns:
        df = df[(df["customer_rating"] >= 1) & (df["customer_rating"] <= 5)]

    return df.reset_index(drop=True)


# ---------------------------------------------------------------------
# 7. Derived Columns
# ---------------------------------------------------------------------

def create_derived_columns(df):
    """
    Create derived analytical columns.

    - delivery_days        = actual_delivery_date - dispatch_date
    - delay_days           = actual_delivery_date - expected_delivery_date
    - cost_per_km          = shipping_cost / distance_km  (safe divide)
    - total_logistics_cost = shipping_cost + fuel_cost
    - on_time_flag         = 1 if delay_days <= 0 else 0
    - delay_status         = 'On Time' / 'Delayed' / 'Unknown'
    """
    df = df.copy()

    # delivery_days
    if {"actual_delivery_date", "dispatch_date"}.issubset(df.columns):
        df["delivery_days"] = (
            df["actual_delivery_date"] - df["dispatch_date"]
        ).dt.days
    else:
        df["delivery_days"] = np.nan

    # delay_days
    if {"actual_delivery_date", "expected_delivery_date"}.issubset(df.columns):
        df["delay_days"] = (
            df["actual_delivery_date"] - df["expected_delivery_date"]
        ).dt.days
    else:
        df["delay_days"] = np.nan

    # on_time_flag / delay_status
    df["on_time_flag"] = np.where(
        df["delay_days"].isna(), np.nan,
        np.where(df["delay_days"] <= 0, 1, 0)
    )
    df["delay_status"] = np.where(
        df["delay_days"].isna(), "Unknown",
        np.where(df["delay_days"] <= 0, "On Time", "Delayed")
    )

    # cost_per_km (safe divide)
    if {"shipping_cost", "distance_km"}.issubset(df.columns):
        df["cost_per_km"] = np.where(
            df["distance_km"] > 0,
            df["shipping_cost"] / df["distance_km"],
            np.nan,
        )
    else:
        df["cost_per_km"] = np.nan

    # total_logistics_cost
    if {"shipping_cost", "fuel_cost"}.issubset(df.columns):
        df["total_logistics_cost"] = df["shipping_cost"] + df["fuel_cost"]
    else:
        df["total_logistics_cost"] = np.nan

    return df


# ---------------------------------------------------------------------
# 8. Orchestrator
# ---------------------------------------------------------------------

def clean_data(df):
    """
    Run the complete cleaning pipeline on the raw DataFrame.

    Order
    -----
    handle_missing_values -> remove_duplicates -> clean_text_columns ->
    clean_date_columns -> validate_numeric_columns ->
    validate_business_rules -> create_derived_columns
    """
    print("Starting cleaning pipeline...")
    df = handle_missing_values(df)
    df = remove_duplicates(df)
    df = clean_text_columns(df)
    df = clean_date_columns(df)
    df = validate_numeric_columns(df)
    df = validate_business_rules(df)
    df = create_derived_columns(df)
    print(f"Cleaning complete. Final shape: {df.shape}")
    return df


# ---------------------------------------------------------------------
# 9. Save
# ---------------------------------------------------------------------

def save_cleaned_data(df, output_path):
    """
    Save the cleaned DataFrame to CSV.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe.
    output_path : str
        Destination CSV path.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to: {output_path}")