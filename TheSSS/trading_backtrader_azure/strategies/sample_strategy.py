import backtrader as bt
import pandas as pd
from TheSSS.R1_V.rl_trader import RLTrader

class RLBacktraderStrategy(bt.Strategy):
    params = (
        ('training_episodes', 10),
        ('historical_data_path', 'TheSSS/trading-backtrader-azure/data/historical_data.csv')
    )

    def __init__(self):
        # Initialize RL Trader with Backtrader integration
        self.rl_trader = RLTrader(
            client=None,
            symbol=self.data._name,
            timeframe='M1',
            data_path=self.params.historical_data_path,
            train_interval=1
        )
        self.rl_trader.initialize_trainer()
        
        # Trackers for RL performance
        self.episode_rewards = []
        self.trade_history = []

    def next(self):
        # Train RL model periodically
        if len(self) % 1000 == 0:  # Train every 1000 bars
            self.rl_trader.train()
            
        # Get RL action
        action = self.rl_trader.get_action()
        
        # Execute trading logic
        if action == 'BUY' and not self.position:
            self.order = self.buy()
        elif action == 'SELL' and self.position:
            self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Completed]:
            price = order.executed.price
            size = order.executed.size
            trade_type = 'BUY' if order.isbuy() else 'SELL'
            
            # Record trade for RL feedback
            self.trade_history.append({
                'datetime': self.data.datetime.datetime(),
                'type': trade_type,
                'price': price,
                'size': size
            })

    def notify_trade(self, trade):
        # Calculate reward based on trade outcome
        if trade.isclosed:
            reward = trade.pnl
            self.rl_trader.total_reward += reward
            self.episode_rewards.append(reward)

    def stop(self):
        # Final training and cleanup
        print("\n=== Final Training ===")
        self.rl_trader.train()
        print(f"Total Cumulative Reward: {self.rl_trader.total_reward:.2f}")
