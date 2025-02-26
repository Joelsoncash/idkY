import requests
import json
import time
import sys
import os
from datetime import datetime
import pandas as pd
from TheSSS.R1_V.rl_trader import RLTrader
from R1_V_repo.src.r1_v.src.open_r1 import DeepSeekR1

# Define PaperTrading class
class PaperTrading:
    def __init__(self, initial_balance=10000):
        self.balance = initial_balance
        self.positions = []

    def execute_trade(self, symbol, volume, order_type, price):
        """Simulate trade execution"""
        trade_type_str = "BUY" if order_type == 'BUY' else 'SELL'
        trade = {
            'symbol': symbol,
            'volume': volume,
            'type': trade_type_str,
            'price': price,
            'time': datetime.now()
        }
        self.positions.append(trade)
        print(f"Simulated trade: {trade}")

        # Update balance (simplified update: no commissions or slippage)
        if order_type == 'BUY':
            self.balance -= volume * price
        else:
            self.balance += volume * price

    def get_balance(self):
        return self.balance

    def get_positions(self):
        return self.positions

def main():
    # Initialize DeepSeek R1 model
    r1_model = DeepSeekR1.from_pretrained('deepseek-r1:latest')

    # Initialize RLTrader with enhanced configuration
    rl_trader = RLTrader(
        client=None,
        symbol='EURUSD',
        timeframe='M1',
        data_path='TheSSS/trading-backtrader-azure/data/historical_data.csv',
        train_interval=1,  # Train after every episode
        model=r1_model  # Add R1 model
    )
    rl_trader.initialize_trainer()
    
    # Run 10 training episodes with full dataset
    for episode in range(1, 11):
        print(f"\n=== Starting Training Episode {episode} ===")
        episode_reward = rl_trader.train()
        print(f"Episode complete. Total Accumulated Reward: {rl_trader.total_reward:.2f}")

if __name__ == "__main__":
    main()
