from src.simulation import simulate_pump_data
from src.business_logic import *
from src.control_layer import simulate_actual_cash
from src.statistical_layer import apply_robust_zscore
from src.anomaly_model import run_isolation_forest
from src.features import create_features
from src.evaluation import classify_risk
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_pipeline():

    logging.info("Pipeline started")

    fuel_df = simulate_pump_data()
    logging.info("Pump data simulated")

    daily_fuel = aggregate_daily_fuel(fuel_df)
    logging.info("Daily fuel aggregated")

    white_bon_df = simulate_white_bon_usage(daily_fuel)
    home_delivery_df = simulate_home_delivery(daily_fuel)
    services_df = simulate_services()
    debt_df = simulate_debt()
    logging.info("Operational components simulated")

    final_df = compute_expected_cash(
        daily_fuel,
        white_bon_df,
        home_delivery_df,
        services_df,
        debt_df
    )
    logging.info("Expected cash computed")

    final_df = simulate_actual_cash(final_df)
    logging.info("Actual cash simulated")

    final_df = apply_robust_zscore(final_df)
    logging.info("Statistical anomalies detected")

    final_df = create_features(final_df)
    logging.info("Features engineered")

    final_df = run_isolation_forest(final_df)
    logging.info("Isolation Forest executed")

    final_df = classify_risk(final_df)
    logging.info("Risk classification completed")

    logging.info("Pipeline completed successfully")

    return final_df
    final_df.to_csv("data/predictions.csv", index=False)
if __name__ == "__main__":
    run_pipeline()