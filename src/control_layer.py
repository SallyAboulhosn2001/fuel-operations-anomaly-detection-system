import numpy as np

def simulate_actual_cash(df, seed=42):
    np.random.seed(seed)

    df = df.copy()

    noise = np.random.normal(0, 800, len(df))

    df["actual_cash"] = df["expected_cash"] + noise
    df["cash_gap"] = df["actual_cash"] - df["expected_cash"]

    return df