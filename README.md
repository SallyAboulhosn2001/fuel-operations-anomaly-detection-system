# Fuel Operations Decision Support & Anomaly Detection System

Built as a production-oriented system for monitoring fuel station operations, detecting anomalies, and supporting daily decision-making.

## Overview

This project transforms unstructured, real-world fuel station records into a structured analytics system that detects operational inconsistencies and provides actionable insights.

It combines data engineering, statistical methods, and machine learning to identify discrepancies in cash flow, fuel activity, and service revenue while maintaining interpretability for real-world use.

## Problem

Fuel station operations often rely on manual tracking and fragmented records. This leads to:

* Limited visibility into actual vs expected cash flow
* Undetected inconsistencies in fuel and revenue data
* No systematic way to identify anomalies
* Weak support for operational decision-making

## Solution

The system introduces a structured pipeline that:

* Cleans and integrates multiple operational data sources
* Engineers business-focused features for monitoring
* Detects anomalies using both statistical and ML approaches
* Assigns interpretable risk levels
* Exposes results through an API for external use
* Supports dashboard-based monitoring

## System Design

Data ingestion and preprocessing unify fuel sales, services, credit systems, and debt tracking.

Feature engineering constructs key indicators such as:

* cash_gap
* cash_gap_ratio
* gasoline_share
* service_to_fuel_ratio

Statistical detection uses a robust Z-score based on median and MAD, suitable for real-world distributions.

Machine learning detection uses Isolation Forest to capture multi-variable anomaly patterns.

A risk scoring layer combines signals into:

* risk_score
* risk_level
* top_anomaly_feature

A FastAPI layer exposes predictions and explanations:

* /predictions
* /explain/{date}

## Key Features

* Hybrid anomaly detection (statistical + machine learning)
* Interpretable risk scoring
* Explainable anomaly outputs
* API-based access to predictions
* Time-series monitoring

## Demo (What the System Does)

Typical workflow:

1. Raw operational data is processed into structured features
2. The system computes expected vs actual cash
3. Anomaly detection identifies unusual patterns
4. Each record is assigned a risk level
5. The API returns predictions and explanations

Example API response:

```json
{
  "date": "2024-05-12",
  "risk_level": "High",
  "ml_anomaly": true,
  "top_anomaly_feature": "cash_gap",
  "ml_score": -0.42
}
```

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/SallyAboulhosn2001/fuel-operations-anomaly-detection-system.git
cd fuel-operations-anomaly-detection-system
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the pipeline

```bash
python run_pipeline.py
```

### 4. Start the API

```bash
uvicorn api.main:app --reload
```

### 5. Access the API

Open in browser:

```
http://127.0.0.1:8000/docs
```

## Project Structure

```
data/
src/
api/
dashboard/
notebooks/
requirements.txt
run_pipeline.py
README.md
```

## Impact

* Structured 365+ days of operational data into analyzable format
* Detected discrepancies between expected and actual cash
* Enabled continuous monitoring of operational risk
* Provided a foundation for data-driven decision-making

## Future Work

* Real-time data streaming
* Automated alerting system
* Cloud deployment
* Advanced explainability methods

## Author

Sally Aboulhosn
AI & Data Science Developer
