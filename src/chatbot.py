import pandas as pd
from openai import OpenAI

client = OpenAI()

def load_data():
    return pd.read_csv("data/predictions.csv")


def retrieve_context(question, df):
    """
    Simple retrieval logic
    """

    # case 1: user mentions a date
    for date in df["date"]:
        if str(date) in question:
            row = df[df["date"] == date].iloc[0]

            return f"""
            Date: {row['date']}
            Risk Level: {row['risk_level']}
            Cash Gap: {row['cash_gap']}
            Anomaly Score: {row['ml_score']}
            Top Feature: {row['top_anomaly_feature']}
            """

    # fallback: summary
    anomalies = df[df["ml_anomaly_flag"] == True]

    return f"""
    Total anomalies: {len(anomalies)}
    Average anomaly score: {df['ml_score'].mean()}
    """


def ask_chatbot(question):
    df = load_data()

    context = retrieve_context(question, df)

    prompt = f"""
    You are an AI assistant for a gas station fraud detection system.

    Context:
    {context}

    Question:
    {question}

    Answer clearly and professionally.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content