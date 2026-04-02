import streamlit as st
import pandas as pd
from run_pipeline import run_pipeline
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from sklearn.metrics import confusion_matrix
from src.fraud_model import train_fraud_model


st.title("Gas Station Anomaly Detection Dashboard")

df = run_pipeline()

model, y_test, y_pred = train_fraud_model(df)
cm = confusion_matrix(y_test, y_pred)

plt.figure(figsize=(5,4))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")
plt.title("Fraud Classification Matrix")

buf = io.BytesIO()
plt.savefig(buf, format="png")
buf.seek(0)

img_base64 = base64.b64encode(buf.read()).decode("utf-8")
cm_html = f'<img src="data:image/png;base64,{img_base64}" width="400"/>'
plt.close()

st.subheader("Anomaly Detection Results")

st.dataframe(df)

st.subheader("ML Score Over Time")

st.line_chart(df.set_index("date")["ml_score"])

st.subheader("Cash Gap Over Time")

st.line_chart(df.set_index("date")["cash_gap"])

st.subheader("High Risk Days")

high_risk = df[df["risk_level"] == "High Risk"]

st.dataframe(high_risk)