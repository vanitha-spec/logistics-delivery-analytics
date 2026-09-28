"""
run_pipeline.py
---------------
Entry point to run the full cleaning pipeline.

Usage
-----
    python run_pipeline.py
"""

import os
from src.data_loader import load_data
from src.data_cleaner import clean_data, save_cleaned_data


RAW_PATH = os.path.join("data", "raw", "logistics_data.csv")
CLEANED_PATH = os.path.join("data", "cleaned", "logistics_cleaned.csv")


def run_pipeline():
    """Run the complete logistics data cleaning pipeline."""
    print("Loading raw data...")
    df = load_data(RAW_PATH)

    print("Checking data quality...")
    print(f"  Shape: {df.shape}")
    print(f"  Missing values per column:\n{df.isna().sum()}")

    print("Cleaning data...")
    df_clean = clean_data(df)

    print("Applying business rules...")
    print("Creating derived columns...")
    print("Saving cleaned data...")
    save_cleaned_data(df_clean, CLEANED_PATH)

    print("Pipeline completed successfully.")
    return df_clean


if __name__ == "__main__":
    run_pipeline()
    