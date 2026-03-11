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