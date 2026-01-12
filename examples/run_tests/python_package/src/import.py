"""
Function to import and process our patient data.
"""

from pathlib import Path

import pandas as pd


def import_patient_data(path):
    """
    Import patient data, validate columns, and create datetime columns.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the CSV file containing the patient data.

    Returns
    -------
    pandas.DataFrame
        Patient-level data with additional datetime columns.
    """
    # Import patient data
    df = pd.read_csv(Path(path))

    # Check whether the dataset contains all the columns we expect it to
    expected = [
        "PATIENT_ID",
        "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
        "DEPARTURE_DATE", "DEPARTURE_TIME"
    ]
    if list(df.columns) != expected:
        raise ValueError(
            f"Unexpected columns: {list(df.columns)} (expected {expected})"
        )

    # Add combined datetime columns
    for prefix in ("ARRIVAL", "SERVICE", "DEPARTURE"):
        df[f"{prefix}_DATETIME"] = pd.to_datetime(
            df[f"{prefix}_DATE"].astype(str)
            + " "
            + df[f"{prefix}_TIME"].astype(str),
            dayfirst=True,
        )

    return df
