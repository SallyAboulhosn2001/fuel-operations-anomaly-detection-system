def compute_monitoring_metrics(df):

    total_days = len(df)
    anomaly_days = df["ml_anomaly"].sum()

    anomaly_rate = anomaly_days / total_days

    avg_score = df["ml_score"].mean()

    high_risk_days = (df["risk_level"] == "High Risk").sum()

    return {
        "total_days": int(total_days),
        "anomaly_days": int(anomaly_days),
        "anomaly_rate": float(anomaly_rate),
        "average_ml_score": float(avg_score),
        "high_risk_days": int(high_risk_days)
    }