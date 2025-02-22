import os
import json
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config(config_path="config/mt5_config.json"):
    with open(config_path, "r") as file:
        config = json.load(file)
    return config

def process_and_upload_data():
    config = load_config()
    symbols = config.get("symbols", [])
    data_window = config.get("data_window", 1000)
    
    for symbol in symbols:
        file_path = os.path.join("data", f"{symbol}_historical_data.csv")
        if os.path.exists(file_path):
            df = pd.read_csv(file_path, index_col=0)
            logger.info("Loaded %s data with %d rows", symbol, len(df))
            # Trim the data to the latest data_window entries if necessary
            if len(df) > data_window:
                df = df.tail(data_window)
                logger.info("Trimmed %s data to latest %d rows", symbol, data_window)
            # Print summary statistics
            logger.info("%s data statistics:\n%s", symbol, df.describe())
            # If needed, you can upload this data into your simulation or training modules here.
        else:
            logger.warning("Data file for %s not found at %s", symbol, file_path)

def main():
    process_and_upload_data()

if __name__ == "__main__":
    main()