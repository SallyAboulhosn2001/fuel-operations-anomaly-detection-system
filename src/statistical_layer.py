import numpy as np


def apply_robust_zscore(df, threshold=3):
    """
    Applies robust z-score using Median Absolute Deviation (MAD)
    to detect abnormal cash gaps.
    """

    df = df.copy()

    median = np.median(df["cash_gap"])
    mad = np.median(np.abs(df["cash_gap"] - median))

    # Avoid division by zero
    if mad == 0:
        df["robust_z"] = 0
        df["investigate_robust"] = False
        return df

    df["robust_z"] = 0.6745 * (df["cash_gap"] - median) / mad
    df["investigate_robust"] = np.abs(df["robust_z"]) > threshold

    return df