from TheSSS.R1_V.rl_trader import RLTrader
from datetime import datetime

if __name__ == "__main__":
    print(f"Starting RLTrader at {datetime.now()}")
    trader = RLTrader(train_interval=1)
    print("Running trading with 30-minute time limit...")
    trader.run_trading()
    print(f"Completed at {datetime.now()}")
