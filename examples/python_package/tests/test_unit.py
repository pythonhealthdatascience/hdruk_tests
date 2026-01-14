"""
Unit testing examples for import_patient_data.
"""

import pandas as pd
import pytest

from waitingtimes.patient_analysis import import_patient_data


def test_import_success(tmp_path):
    """Small CSV with correct columns should work."""

    expected_cols = [
        "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]

    # Create temporary CSV file
    df_in = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=expected_cols,
    )
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Run function and check it looks correct
    result = import_patient_data(csv_path)
    assert isinstance(result, pd.DataFrame)
    assert list(result.columns) == expected_cols
    pd.testing.assert_frame_equal(result, df_in)


@pytest.mark.parametrize(
    "columns",
    [
        # Example 1: Missing columns
        [
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME", "SERVICE_DATE"
        ],
        # Example 2: Extra columns
        [
            "PATIENT_ID", "ARRIVAL_DATE", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME", "EXTRA",
        ],
        # Example 3: Right columns, wrong order
        [
            "ARRIVAL_DATE", "PATIENT_ID", "ARRIVAL_TIME",
            "SERVICE_DATE", "SERVICE_TIME",
        ],
    ],
)
def test_import_errors(tmp_path, columns):
    """Incorrect columns should trigger ValueError."""

    # Create temporary CSV file
    df_in = pd.DataFrame([range(len(columns))], columns=columns)
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Check it raises ValueError
    with pytest.raises(ValueError):
        import_patient_data(csv_path)


def test_import_path_types(tmp_path):
    """str and Path inputs should behave identically."""
    # Create temporary CSV file
    expected_cols = [
        "PATIENT_ID",
        "ARRIVAL_DATE", "ARRIVAL_TIME",
        "SERVICE_DATE", "SERVICE_TIME",
    ]
    df_in = pd.DataFrame(
        [["p1", "2024-01-01", "08:00", "2024-01-01", "09:00"]],
        columns=expected_cols,
    )
    csv_path = tmp_path / "patients.csv"
    df_in.to_csv(csv_path, index=False)

    # Run function with str or Path inputs
    df_str = import_patient_data(str(csv_path))
    df_path = import_patient_data(csv_path)

    # Check that results are the same
    pd.testing.assert_frame_equal(df_str, df_path)