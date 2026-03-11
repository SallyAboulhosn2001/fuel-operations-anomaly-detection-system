import joblib
import os
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler


MODEL_PATH = "models/isolation_forest.pkl"
SCALER_PATH = "models/scaler.pkl"


def run_isolation_forest(df):

    df = df.copy()

    features = df[
        [
            "cash_gap",
            "gasoline",
            "diesel",
            "service_revenue"
        ]
    ]

    # If model already exists → load it
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):

        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)

        X = scaler.transform(features)

    else:

        scaler = StandardScaler()
        X = scaler.fit_transform(features)

        model = IsolationForest(
            contamination=0.06,
            random_state=42
        )

        model.fit(X)

        os.makedirs("models", exist_ok=True)

        joblib.dump(model, MODEL_PATH)
        joblib.dump(scaler, SCALER_PATH)

    preds = model.predict(X)

    df["ml_anomaly_flag"] = preds == -1
    df["ml_score"] = model.decision_function(X)

    return df