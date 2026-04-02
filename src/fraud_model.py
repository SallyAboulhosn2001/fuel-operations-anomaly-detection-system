from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.utils import resample
import pandas as pd

def train_fraud_model(df):

    features = [
        "cash_gap",
        "cash_gap_abs",
        "fuel_total",
        "service_ratio"
    ]
    df_balanced = []

    for fraud_class in df["fraud_type"].unique():
        subset = df[df["fraud_type"] == fraud_class]

        if len(subset) < 50:
            subset = resample(subset, replace=True, n_samples=50, random_state=42)

        df_balanced.append(subset)

    df = pd.concat(df_balanced)
    X = df[features]
    y = df["fraud_type"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")

    model.fit(X_train, y_train)

    # predictions ONLY on test set
    y_pred = model.predict(X_test)


    return model, y_test, y_pred