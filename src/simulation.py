import numpy as np
import pandas as pd


def simulate_pump_data(days=365, start_date="2023-01-01", seed=42):
    """
    Simulates realistic seasonal fuel pump data for a multi-pump gas station.
    Returns a DataFrame with cumulative meter readings and daily liters.
    """

    np.random.seed(seed)

    # ---------------------------
    # Configuration
    # ---------------------------

    PUMPS = {
        "gasoline_LBP_1": {"fuel_type": "gasoline", "currency": "LBP"},
        "gasoline_LBP_2": {"fuel_type": "gasoline", "currency": "LBP"},
        "gasoline_USD_1": {"fuel_type": "gasoline", "currency": "USD"},
        "gasoline_USD_2": {"fuel_type": "gasoline", "currency": "USD"},
        "diesel_LBP_1": {"fuel_type": "diesel", "currency": "LBP"},
        "diesel_USD_1": {"fuel_type": "diesel", "currency": "USD"},
    }

    BASE_DAILY_VOLUME = {
        "gasoline": 750,      # per pump average
        "diesel": 3750
    }

    SEASONAL_AMPLITUDE = {
        "gasoline": 250,      # gasoline drops in summer
        "diesel": 1250        # diesel rises in summer
    }

    dates = pd.date_range(start_date, periods=days)

    all_pump_data = []

    # ---------------------------
    # Simulation Loop
    # ---------------------------

    for pump_id, pump_info in PUMPS.items():

        fuel_type = pump_info["fuel_type"]
        currency = pump_info["currency"]

        base_volume = BASE_DAILY_VOLUME[fuel_type]
        amplitude = SEASONAL_AMPLITUDE[fuel_type]

        current_meter = np.random.uniform(100_000, 200_000)

        for date in dates:

            day_of_year = date.dayofyear
            seasonal_factor = np.sin(2 * np.pi * day_of_year / 365)

            if fuel_type == "gasoline":
                daily_volume = base_volume - amplitude * seasonal_factor
            else:
                daily_volume = base_volume + amplitude * seasonal_factor

            noise = np.random.normal(0, base_volume * 0.08)
            daily_volume = max(0, daily_volume + noise)

            opening_meter = current_meter
            closing_meter = current_meter + daily_volume

            all_pump_data.append({
                "date": date,
                "pump_id": pump_id,
                "fuel_type": fuel_type,
                "currency": currency,
                "opening_meter": opening_meter,
                "closing_meter": closing_meter,
                "liters_sold": daily_volume
            })

            current_meter = closing_meter

    fuel_df = pd.DataFrame(all_pump_data)

    # ---------------------------
    # Validation Checks
    # ---------------------------

    assert (fuel_df["liters_sold"] >= 0).all()

    for pump in fuel_df["pump_id"].unique():
        pump_data = fuel_df[fuel_df["pump_id"] == pump]
        assert (pump_data["closing_meter"].diff().fillna(1) >= 0).all()
    return fuel_df

def inject_fraud_scenarios(df):

    df = df.copy()

    df["fraud_type"] = "normal"

    # randomly choose days where fraud happens
    fraud_indices = np.random.choice(df.index, size=int(len(df) * 0.05), replace=False)

    for idx in fraud_indices:

        scenario = np.random.choice([
            "cash_theft",
            "pump_malfunction",
            "suspicious_service"
        ])

        if scenario == "cash_theft":

            df.loc[idx, "actual_cash"] *= 0.75
            df.loc[idx, "fraud_type"] = "cash_theft"

        elif scenario == "pump_malfunction":

            df.loc[idx, "gasoline"] *= 1.8
            df.loc[idx, "fraud_type"] = "pump_malfunction"

        elif scenario == "suspicious_service":

            df.loc[idx, "service_revenue"] *= 3
            df.loc[idx, "fraud_type"] = "suspicious_service"

# simulate fraud scenarios

    fraud_days = np.random.choice(df.index, size=int(len(df)*0.15), replace=False)

    for i in fraud_days:

        fraud_type = np.random.choice([
            "cash_theft",
            "pump_manipulation",
            "service_fraud"
    ])

        if fraud_type == "cash_theft":
            df.loc[i, "actual_cash"] -= np.random.uniform(300, 800)

        elif fraud_type == "pump_manipulation":
            df.loc[i, "gasoline"] *= np.random.uniform(0.7, 0.85)

        elif fraud_type == "service_fraud":
            df.loc[i, "service_revenue"] *= np.random.uniform(1.8, 2.5)

        df.loc[i, "fraud_type"] = fraud_type

    return df