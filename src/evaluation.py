def classify_risk(df):

    df = df.copy()

    df["risk_score"] = (
        df["investigate_robust"].astype(int) * 2
        + df["ml_anomaly_flag"].astype(int)
    )

    def classify(score):

        if score >= 3:
            return "High Risk"

        elif score == 2:
            return "Medium Risk"

        elif score == 1:
            return "Low Risk"

        else:
            return "Normal"

    df["risk_level"] = df["risk_score"].apply(classify)

    return df