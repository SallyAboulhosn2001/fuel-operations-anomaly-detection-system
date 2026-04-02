import shap
import pandas as pd

def explain_anomalies(model, df, feature_cols):

    X = df[feature_cols]

    explainer = shap.Explainer(model, X)

    shap_values = explainer(X)

    shap_df = pd.DataFrame(
        shap_values.values,
        columns=feature_cols
    )

    return shap_df