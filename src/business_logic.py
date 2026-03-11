import pandas as pd
import numpy as np


def aggregate_daily_fuel(fuel_df):
    """
    Aggregates pump-level data into daily fuel totals.
    """

    daily_fuel = (
        fuel_df
        .groupby(["date", "fuel_type"])["liters_sold"]
        .sum()
        .unstack()
        .fillna(0)
        .reset_index()
    )

    daily_fuel.columns.name = None

    return daily_fuel


def simulate_white_bon_usage(daily_fuel, seed=42):
    """
    Simulates white bon liters used (prepaid fuel usage).
    White bon usage reduces chargeable liters.
    """

    np.random.seed(seed)

    white_bon_usage = []

    for _, row in daily_fuel.iterrows():
        gasoline_bon = np.random.uniform(0, row.get("gasoline", 0) * 0.1)
        diesel_bon = np.random.uniform(0, row.get("diesel", 0) * 0.1)

        white_bon_usage.append({
            "date": row["date"],
            "white_bon_gasoline": gasoline_bon,
            "white_bon_diesel": diesel_bon
        })

    white_bon_df = pd.DataFrame(white_bon_usage)

    return white_bon_df


def simulate_home_delivery(daily_fuel, seed=42):
    """
    Simulates diesel home delivery (outside pump meters).
    """

    np.random.seed(seed + 1)

    home_delivery = []

    for _, row in daily_fuel.iterrows():
        delivery = np.random.uniform(0, 1500)

        home_delivery.append({
            "date": row["date"],
            "diesel_home_delivery_liters": delivery
        })

    return pd.DataFrame(home_delivery)


def simulate_services(seed=42, days=365, start_date="2023-01-01"):
    """
    Simulates service revenue: car wash, oil change, accessories.
    """

    np.random.seed(seed + 2)

    dates = pd.date_range(start_date, periods=days)

    services = []

    for date in dates:
        car_wash = np.random.uniform(200, 600)
        oil_change = np.random.uniform(300, 800)
        accessories = np.random.uniform(150, 500)

        services.append({
            "date": date,
            "car_wash_revenue": car_wash,
            "oil_change_revenue": oil_change,
            "accessories_revenue": accessories
        })

    return pd.DataFrame(services)


def simulate_debt(seed=42, days=365, start_date="2023-01-01"):
    """
    Simulates new debt and old debt payments.
    """

    np.random.seed(seed + 3)

    dates = pd.date_range(start_date, periods=days)

    debt = []

    for date in dates:
        new_debt = np.random.uniform(0, 2000)
        old_debt_paid = np.random.uniform(0, 1500)

        debt.append({
            "date": date,
            "new_debt": new_debt,
            "old_debt_paid": old_debt_paid
        })

    return pd.DataFrame(debt)

def compute_expected_cash(
    daily_fuel,
    white_bon_df,
    home_delivery_df,
    services_df,
    debt_df,
    gasoline_price=1.0,
    diesel_price=1.0
):
    df = daily_fuel.merge(white_bon_df, on="date", how="left")
    df = df.merge(home_delivery_df, on="date", how="left")
    df = df.merge(services_df, on="date", how="left")
    df = df.merge(debt_df, on="date", how="left")

    df[["white_bon_gasoline", "white_bon_diesel"]] = df[
        ["white_bon_gasoline", "white_bon_diesel"]
    ].fillna(0)

    df["diesel_home_delivery_liters"] = df[
        "diesel_home_delivery_liters"
    ].fillna(0)

    df[["new_debt", "old_debt_paid"]] = df[
        ["new_debt", "old_debt_paid"]
    ].fillna(0)

    df["net_gasoline_liters"] = df["gasoline"] - df["white_bon_gasoline"]
    df["net_diesel_liters"] = df["diesel"] - df["white_bon_diesel"]

    df["fuel_revenue"] = (
        df["net_gasoline_liters"] * gasoline_price
        + df["net_diesel_liters"] * diesel_price
        + df["diesel_home_delivery_liters"] * diesel_price
    )

    df["service_revenue"] = (
        df["car_wash_revenue"]
        + df["oil_change_revenue"]
        + df["accessories_revenue"]
    )

    df["expected_cash"] = (
        df["fuel_revenue"]
        + df["service_revenue"]
        - df["new_debt"]
        + df["old_debt_paid"]
    )

    return df