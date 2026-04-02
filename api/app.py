from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
from src.chatbot import ask_chatbot
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from sklearn.metrics import confusion_matrix

from src.monitoring import compute_monitoring_metrics
from src.fraud_model import train_fraud_model

app = FastAPI()


# ---------------- DATA LOADER ----------------

def load_predictions():
    return pd.read_csv("data/predictions.csv")


def format_predictions(df):

    df = df.copy()
    df["ml_anomaly"] = df["ml_anomaly_flag"].astype(bool)

    return df[
        [
            "date",
            "risk_level",
            "ml_anomaly",
            "top_anomaly_feature",
            "ml_score"
        ]
    ].to_dict(orient="records")


# ---------------- API ----------------

@app.get("/predictions")
def get_predictions():
    df = load_predictions()
    return format_predictions(df)


# 🔥 -------- INSANE XAI (MULTI-FACTOR) --------

@app.get("/explain/{date}")
def explain_anomaly(date: str):

    df = load_predictions()
    row = df[df["date"] == date]

    if row.empty:
        return {"error": "Date not found"}

    row = row.iloc[0]

    explanations = []

    # -------- MULTI-FACTOR EXPLANATION --------

    if abs(row["cash_gap"]) > 300:
        if row["cash_gap"] < 0:
            explanations.append("Cash significantly lower than expected → possible theft")
        else:
            explanations.append("Cash higher than expected → possible accounting inconsistency")

    if row["gasoline_share"] > 0.35:
        explanations.append("Gasoline proportion unusually high → possible pump manipulation")

    if row["service_to_fuel_ratio"] > 0.2:
        explanations.append("Service revenue unusually high → possible suspicious services")

    if abs(row["robust_z"]) > 3:
        explanations.append("Extreme statistical deviation detected → abnormal operational behavior")

    # fallback
    if not explanations:
        explanations.append("Minor anomaly detected with no strong risk indicators")

    return {
        "date": row["date"],
        "risk_level": row["risk_level"],
        "ml_anomaly": bool(row["ml_anomaly_flag"]),
        "ml_score": row["ml_score"],
        "explanations": explanations
    }


@app.get("/monitoring")
def get_monitoring():
    df = load_predictions()
    return compute_monitoring_metrics(df)


# ---------------- HOME ----------------

@app.get("/", response_class=HTMLResponse)
def home():

    return """
    <html>
    <head>
    <title>Gas Station AI Monitoring</title>

    <style>
    body{
        font-family:Arial;
        text-align:center;
        background:#f4f6f9;
    }

    h1{
        margin-top:100px;
        color:#2c3e50;
    }

    button{
        padding:15px 30px;
        font-size:18px;
        border:none;
        border-radius:8px;
        background:#3498db;
        color:white;
        cursor:pointer;
    }

    button:hover{
        background:#2980b9;
    }
    </style>

    </head>

    <body>

        <h1>Gas Station AI Monitoring System</h1>

        <br>

        <a href="/dashboard">
        <button>Open Dashboard</button>
        </a>

        <br><br>

        <a href="/docs">API Docs</a>

    </body>
    </html>
    """

@app.get("/chat")
def chat(q: str):
    response = ask_chatbot(q)
    return {"response": response}
# ---------------- DASHBOARD ----------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    df = load_predictions()

    # -------- ANOMALY SCORE --------

    fig = px.line(df, x="date", y="ml_score", title="Anomaly Score")

    anomalies = df[df["ml_anomaly_flag"] == True]

    fig.add_scatter(
        x=anomalies["date"],
        y=anomalies["ml_score"],
        mode="markers",
        marker=dict(color="red", size=10),
        name="Anomaly"
    )

    chart_html = fig.to_html(full_html=False, include_plotlyjs="cdn")


    # -------- CASH GAP --------

    cash_fig = px.line(df, x="date", y="cash_gap", title="Cash Gap")

    cash_chart_html = cash_fig.to_html(full_html=False, include_plotlyjs=False)


    # -------- RISK PIE --------

    risk_counts = df["risk_level"].value_counts().reset_index()
    risk_counts.columns = ["risk_level", "count"]

    pie = px.pie(risk_counts, names="risk_level", values="count", title="Risk Distribution")

    pie_html = pie.to_html(full_html=False, include_plotlyjs=False)


    # -------- FEATURES --------

    feature_counts = df["top_anomaly_feature"].value_counts().reset_index()
    feature_counts.columns = ["feature", "count"]

    feature_fig = px.bar(feature_counts, x="feature", y="count", title="Top Anomaly Features")

    feature_chart_html = feature_fig.to_html(full_html=False, include_plotlyjs=False)


    # -------- CONFUSION MATRIX --------

    model, y_test, y_pred = train_fraud_model(df)

    cm = confusion_matrix(y_test, y_pred)

    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues")

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close()

    cm_html = f'<img src="data:image/png;base64,{img_base64}" width="500"/>'


    # -------- HTML --------

    return f"""
    <html>

    <head>

    <style>

    body{{
        font-family:Arial;
        background:#f4f6f9;
        margin:40px;
    }}

    .card{{
        background:white;
        padding:20px;
        border-radius:10px;
        box-shadow:0 4px 12px rgba(0,0,0,0.08);
        margin-bottom:30px;
    }}

    input{{
        padding:10px;
        width:200px;
    }}

    button{{
        padding:10px 20px;
        background:#3498db;
        color:white;
        border:none;
        border-radius:5px;
        cursor:pointer;
    }}

    pre{{
        background:#eee;
        padding:15px;
        border-radius:8px;
    }}

    </style>

    </head>

    <body>

    <h1>AI Monitoring Dashboard</h1>

    <div class="card" id="anomaly-chart">{chart_html}</div>
    <div class="card">{cash_chart_html}</div>
    <div class="card">{pie_html}</div>
    <div class="card">{feature_chart_html}</div>

    <div class="card">
    <h2>Model Performance</h2>
    {cm_html}
    </div>

    <div class="card">

    <h2>Explain Anomaly</h2>

    <input type="text" id="dateInput" placeholder="YYYY-MM-DD"/>
    <button onclick="getExplanation()">Explain</button>

    <pre id="resultBox"></pre>

    </div>

<script>

document.addEventListener("DOMContentLoaded", function() {{

    var plot = document.querySelector("#anomaly-chart .plotly-graph-div");

    if(plot) {{

        plot.on('plotly_click', function(data) {{

            var date = data.points[0].x;
            window.open("/explain/" + date, "_blank");

        }});

    }}

}});

async function getExplanation() {{

    const date = document.getElementById("dateInput").value;

    const response = await fetch(`/explain/${{date}}`);
    const data = await response.json();

    document.getElementById("resultBox").innerText =
        "Risk Level: " + data.risk_level + "\\n\\n" +
        "Anomaly: " + data.ml_anomaly + "\\n\\n" +
        "ML Score: " + data.ml_score + "\\n\\n" +
        "Top Causes:\\n- " + data.explanations.join("\\n- ");
}}

</script>

    </body>
    </html>
    """