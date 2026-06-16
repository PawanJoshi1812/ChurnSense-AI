import numpy as np
import pandas as pd

def validate_input_data(df, expected_features):
    
    errors = []

    # 1. Check empty dataframe
    if df is None or df.empty:
        return False, ["Empty dataset received"]

    # 2. Check missing columns
    missing_cols = [col for col in expected_features if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing columns: {missing_cols}")

    # 3. Check NaN values
    nan_counts = df.isna().sum()
    if nan_counts.sum() > 0:
        errors.append(f"Dataset contains missing values:\n{nan_counts.to_dict()}")

    # 4. Check infinite values
    if np.isinf(df.select_dtypes(include=[np.number])).values.any():
        errors.append("Dataset contains infinite values")

    # 5. Check row count
    if len(df) == 0:
        errors.append("No rows found in dataset")

    if errors:
        return False, errors

    return True, ["Validation passed"]