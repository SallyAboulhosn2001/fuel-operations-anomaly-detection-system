from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import plotly.express as px
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
    <head>

    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">

    <style>

    body {
        margin: 0;
        font-family: 'Inter', sans-serif;
        background: #020617;
        color: white;
    }

    /* NAVBAR */

    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 20px 60px;
        background: #020617;
    }

    .logo {
        font-size: 22px;
        font-weight: 700;
        color: #22c55e;
    }

    .nav-links a {
        margin: 0 15px;
        color: #94a3b8;
        text-decoration: none;
        font-size: 14px;
    }

    .nav-right {
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .btn-nav {
        padding: 8px 16px;
        border-radius: 8px;
        background: #16a34a;
        color: white;
        text-decoration: none;
    }

    /* HERO */

    .hero {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 80px 60px;
    }

    .hero-left {
        max-width: 600px;
    }

    h1 {
        font-size: 64px;
        font-weight: 700;
        line-height: 1.1;
        margin: 0;
    }

    .green {
        color: #22c55e;
    }

    .subtitle {
        margin-top: 20px;
        color: #94a3b8;
        font-size: 18px;
        line-height: 1.6;
    }

    /* BADGES */

    .badges {
        display: flex;
        gap: 15px;
        margin-top: 25px;
    }

    .badge {
        background: rgba(255,255,255,0.05);
        padding: 12px 18px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        font-size: 14px;
    }

    /* BUTTONS */

    .buttons {
        margin-top: 30px;
        display: flex;
        gap: 15px;
    }

    .btn-primary {
        background: #16a34a;
        padding: 14px 24px;
        border-radius: 12px;
        color: white;
        text-decoration: none;
        font-weight: 600;
    }

    .btn-secondary {
        background: white;
        color: black;
        padding: 14px 24px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: 600;
    }

    .btn-primary:hover,
    .btn-secondary:hover {
        transform: translateY(-2px);
    }

    /* RIGHT VISUAL */

    .hero-right {
        font-size: 120px;
    }
    .hero-img {
    width: 420px;
    max-width: 100%;
    animation: float 3s ease-in-out infinite;
    }

    @keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-12px); }
    100% { transform: translateY(0px); }
    }

    </style>
    </head>

    <body>

    <!-- NAVBAR -->
    <div class="navbar">
        <div class="logo">⛽ FuelStop</div>

        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#">Services</a>
            <a href="#">Locations</a>
            <a href="#">Rewards</a>
            <a href="#">About</a>
        </div>

        <div class="nav-right">
            <span style="color:#94a3b8;">📍 Find Station</span>
            <a href="#" class="btn-nav">Sign In</a>
        </div>
    </div>

    <!-- HERO -->
    <div class="hero">

        <div class="hero-left">

            <h1>
                Fuel Your Journey<br>
                <span class="green">Power Your Dreams</span>
            </h1>

            <p class="subtitle">
                Monitor fuel operations, detect anomalies, and gain real-time insights 
                with an AI-powered analytics system.
            </p>

            <div class="badges">
                <div class="badge">🟢 Open 24/7</div>
                <div class="badge">📍 Smart Monitoring</div>
                <div class="badge">⛽ AI Detection</div>
            </div>

            <!-- YOUR BUTTONS (IMPORTANT) -->
            <div class="buttons">
                <a href="/dashboard" class="btn-primary">Open Dashboard</a>
                <a href="/chat?q=summary" class="btn-secondary">AI Assistant</a>
            </div>

        </div>

        <div class="hero-right">
            <img src="/static/fuel3d.png" class="hero-img">
        </div>

    </div>

    </body>
    </html>
    """
def load_predictions():
    return pd.read_csv("data/predictions.csv")


# ---------------- EXPLANATION ----------------

def generate_explanation(row):
    explanations = []

    if abs(row.get("cash_gap", 0)) > 300:
        if row["cash_gap"] < 0:
            explanations.append("⚠️ Cash lower than expected → possible revenue leakage")
        else:
            explanations.append("⚠️ Cash higher than expected → accounting inconsistency")

    if row.get("gasoline_share", 0) > 0.35:
        explanations.append("⚠️ High gasoline proportion → possible manipulation")

    if row.get("service_to_fuel_ratio", 0) > 0.2:
        explanations.append("⚠️ Service revenue unusually high")

    if abs(row.get("robust_z", 0)) > 3:
        explanations.append("⚠️ Extreme statistical deviation")

    if not explanations:
        explanations.append("No significant anomaly detected")

    return explanations


# ---------------- CHATBOT ----------------

@app.get("/chat")
def chat(q: str):
    df = load_predictions()
    q = q.lower()

    if "-" in q:
        row = df[df["date"] == q]
        if row.empty:
            return {"response": "❌ Date not found"}

        row = row.iloc[0]
        explanations = generate_explanation(row)

        return {
            "response": f"""
            📅 <b>{row['date']}</b><br>
            ⚠️ Risk: {row['risk_level']}<br>
            📊 Score: {row['ml_score']}<br><br>
            <b>Insights:</b><br>
            - {'<br>- '.join(explanations)}
            """
        }

    if "highest" in q or "worst" in q:
        worst = df.sort_values("ml_score", ascending=False).iloc[0]
        return {
            "response": f"""
            🚨 <b>Highest Risk Day</b><br><br>
            📅 {worst['date']}<br>
            ⚠️ Risk: {worst['risk_level']}<br>
            📊 Score: {worst['ml_score']}
            """
        }

    if "summary" in q:
        total = len(df)
        anomalies = df["ml_anomaly_flag"].sum()
        return {
            "response": f"""
            📊 <b>System Summary</b><br><br>
            Total days: {total}<br>
            Anomalies: {anomalies}<br>
            Normal: {total - anomalies}
            """
        }

    return {"response": "Ask about a date, highest anomaly, or summary 📊"}


# ---------------- DASHBOARD ----------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():

    df = load_predictions()

    # KPIs
    total_revenue = df["fuel_revenue"].sum() + df["service_revenue"].sum()
    total_loss = df[df["cash_gap"] < 0]["cash_gap"].sum()
    anomaly_days = df["ml_anomaly_flag"].sum()
    total_days = len(df)
    highest_risk = df.sort_values("ml_score", ascending=False).iloc[0]["date"]

    # Charts
    fig1 = px.line(df, x="date", y="ml_score", title="Operational Risk Score")
    fig2 = px.line(df, x="date", y="cash_gap", title="Cash Gap")
    fig3 = px.line(df, x="date", y=["fuel_revenue", "service_revenue"], title="Revenue Streams")
    fig4 = px.line(df, x="date", y="gasoline_share", title="Gasoline Share")
    fig5 = px.histogram(df, x="risk_level", title="Risk Distribution")

    graph1 = fig1.to_html(full_html=False)
    graph2 = fig2.to_html(full_html=False)
    graph3 = fig3.to_html(full_html=False)
    graph4 = fig4.to_html(full_html=False)
    graph5 = fig5.to_html(full_html=False)

    return f"""
    <html>
    <head>
    <style>
    body {{
        font-family: Arial;
        background: #f4f6f9;
        margin: 40px;
    }}

    .card {{
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}

    .message {{
        padding: 10px 15px;
        border-radius: 12px;
        margin: 8px 0;
        max-width: 70%;
        font-size: 14px;
    }}

    .user {{
        background: #3498db;
        color: white;
        margin-left: auto;
    }}

    .bot {{
        background: #ecf0f1;
    }}

    </style>
    </head>

    <body>

    <h1>Fuel Operations Intelligence System</h1>

    <!-- KPIs -->
    <div style="display:flex; gap:20px; margin-bottom:30px;">
        <div class="card"><h3>Total Revenue</h3><p>${total_revenue:,.0f}</p></div>
        <div class="card"><h3>Estimated Loss</h3><p>${total_loss:,.0f}</p></div>
        <div class="card"><h3>Anomaly Days</h3><p>{anomaly_days}/{total_days}</p></div>
        <div class="card"><h3>Highest Risk Day</h3><p>{highest_risk}</p></div>
    </div>

    <!-- Charts -->
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
        <div class="card">{graph1}</div>
        <div class="card">{graph2}</div>
        <div class="card">{graph3}</div>
        <div class="card">{graph4}</div>
    </div>

    <div class="card">{graph5}</div>

    <!-- Chatbot -->
    <div class="card">
        <h2>AI Assistant</h2>

        <div id="chatBox" style="
            height:350px;
            overflow-y:auto;
            background:#f9f9f9;
            padding:15px;
            border-radius:10px;
            display:flex;
            flex-direction:column;
        "></div>

        <br>

        <input type="text" id="chatInput" placeholder="Ask about risks, anomalies..."
            style="width:75%; padding:10px; border-radius:8px; border:1px solid #ccc;">

        <button onclick="sendMessage()"
            style="padding:10px 15px; border:none; background:#3498db; color:white; border-radius:8px;">
            Send
        </button>
    </div>

    <script>

    function addMessage(text, sender) {{
        const chatBox = document.getElementById("chatBox");

        const msg = document.createElement("div");
        msg.classList.add("message", sender);

        msg.innerHTML = text;

        chatBox.appendChild(msg);
        chatBox.scrollTop = chatBox.scrollHeight;
    }}

    async function sendMessage() {{
        const input = document.getElementById("chatInput");
        const userText = input.value.trim();

        if (!userText) return;

        addMessage(userText, "user");
        input.value = "";

        addMessage("Typing...", "bot");

        try {{
            const res = await fetch(`/chat?q=${{encodeURIComponent(userText)}}`);
            const data = await res.json();

            const chatBox = document.getElementById("chatBox");
            chatBox.removeChild(chatBox.lastChild);

            addMessage(data.response, "bot");

        }} catch {{
            addMessage("⚠️ Server error", "bot");
        }}
    }}

    </script>

    </body>
    </html>
    """