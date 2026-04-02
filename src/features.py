def create_features(df):

    df = df.copy()

    df["cash_gap_ratio"] = df["cash_gap"] / df["expected_cash"]

    df["gasoline_share"] = df["gasoline"] / (
        df["gasoline"] + df["diesel"]
    )

    df["service_to_fuel_ratio"] = (
        df["service_revenue"] / df["fuel_revenue"]
    )
    df["cash_gap_abs"] = abs(df["cash_gap"])
    df["fuel_total"] = df["gasoline"] + df["diesel"]
    df["service_ratio"] = df["service_revenue"] / (df["fuel_revenue"] + 1)
    return df