from fastapi import FastAPI
import pandas as pd

from src.anomaly_model import run_isolation_forest
from src.features import create_features
from src.evaluation import classify_risk

app = FastAPI(
    title="Fuel Station AI Monitoring API",
    description="Anomaly detection service for fuel station operations",
    version="1.0"
)


@app.get("/")
def home():
    return {"message": "Fuel AI monitoring system is running"}


@app.post("/detect_anomaly")
def detect_anomaly(data: dict):

    df = pd.DataFrame([data])

    df = create_features(df)

    df = run_isolation_forest(df)

    df = classify_risk(df)

    return df.to_dict(orient="records")

from api.schemas import FuelInput

@app.post("/detect_anomaly")

def detect_anomaly(data: FuelInput):

    df = pd.DataFrame([data.dict()])