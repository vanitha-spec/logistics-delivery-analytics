"""
test_pipeline.py
----------------
Basic pytest-based tests for the logistics cleaning pipeline.
Run with:
    pytest tests/test_pipeline.py -v
"""

import os
import sys
import pandas as pd
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.data_loader import load_data, check_file_exists
from src.data_cleaner import (
    remove_duplicates, create_derived_columns, clean_data,
    save_cleaned_data,
)
from src.business_analysis import (
    calculate_total_orders, calculate_on_time_percentage,
)

RAW_PATH = os.path.join("data", "raw", "logistics_data.csv")
TMP_CLEANED = os.path.join("data", "cleaned", "_test_cleaned.csv")


def test_load_data():
    """Test that the raw data loads successfully."""
    assert check_file_exists(RAW_PATH), "Raw data file missing."
    df = load_data(RAW_PATH)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_remove_duplicates():
    """Test that duplicates are removed."""
    df = pd.DataFrame({"order_id": ["A", "A", "B"], "x": [1, 1, 2]})
    out = remove_duplicates(df)
    assert len(out) == 2


def test_create_derived_columns():
    """Test that derived columns are created correctly."""
    df = pd.DataFrame({
        "order_id": ["A"],
        "dispatch_date": pd.to_datetime(["2025-01-01"]),
        "expected_delivery_date": pd.to_datetime(["2025-01-05"]),
        "actual_delivery_date": pd.to_datetime(["2025-01-07"]),
        "shipping_cost": [100.0],
        "fuel_cost": [50.0],
        "distance_km": [10.0],
    })
    out = create_derived_columns(df)
    for c in ["delivery_days", "delay_days", "cost_per_km",
              "total_logistics_cost", "on_time_flag"]:
        assert c in out.columns
    assert out["delay_days"].iloc[0] == 2
    assert out["on_time_flag"].iloc[0] == 0
    assert out["total_logistics_cost"].iloc[0] == 150.0


def test_clean_data():
    """Test that clean_data returns a non-empty DataFrame."""
    df = load_data(RAW_PATH)
    cleaned = clean_data(df)
    assert isinstance(cleaned, pd.DataFrame)
    assert len(cleaned) > 0
    assert "on_time_flag" in cleaned.columns


def test_calculate_total_orders():
    """Test total orders KPI."""
    df = pd.DataFrame({"order_id": ["A", "B", "C"]})
    assert calculate_total_orders(df) == 3


def test_calculate_on_time_percentage():
    """Test on-time percentage KPI."""
    df = pd.DataFrame({
        "delivery_status": ["Delivered", "Delivered", "Delivered", "Delayed"],
        "delay_days": [0, -1, 2, 3],
    })
    pct = calculate_on_time_percentage(df)
    assert 0 <= pct <= 100
    assert pct == pytest.approx(66.67, rel=0.1)


def test_save_cleaned_data():
    """Test that cleaned data is saved to disk."""
    df = pd.DataFrame({
        "order_id": ["A"], "delay_days": [0], "on_time_flag": [1]
    })
    save_cleaned_data(df, TMP_CLEANED)
    assert os.path.exists(TMP_CLEANED)
    os.remove(TMP_CLEANED)
    