"""
data_loader.py
--------------
Handles loading the raw logistics dataset into a Pandas DataFrame.
"""

import os
import pandas as pd


def check_file_exists(file_path):
    """
    Check whether a file exists at the given path.

    Parameters
    ----------
    file_path : str
        Path to the file to check.

    Returns
    -------
    bool
        True if the file exists, False otherwise.
    """
    return os.path.isfile(file_path)


def load_data(file_path):
    """
    Load the logistics CSV data into a Pandas DataFrame.

    Parameters
    ----------
    file_path : str
        Path to the raw CSV file.

    Returns
    -------
    pd.DataFrame
        The raw logistics dataset.

    Raises
    ------
    FileNotFoundError
        If the file does not exist at the given path.
    """
    if not check_file_exists(file_path):
        raise FileNotFoundError(f"Raw data file not found: {file_path}")

    df = pd.read_csv(file_path, low_memory=False)
    print(f"Loaded raw data: {df.shape[0]} rows x {df.shape[1]} columns")
    return df