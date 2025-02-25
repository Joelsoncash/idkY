import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import backtrader as bt
import pandas as pd
from strategies.sample_strategy import RLBacktraderStrategy

def run_backtest():
    cerebro = bt.Cerebro()
    
    # Load historical data
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, 'data', 'historical_data.csv')
    
    data = pd.read_csv(
        data_path,
        parse_dates=['date'],
        index_col='date'
    )
    
    # Add data feed
    data_feed = bt.feeds.PandasData(
        dataname=data,
        timeframe=bt.TimeFrame.Minutes,
        compression=1
    )
    cerebro.adddata(data_feed)
    
    # Add RL-Backtrader strategy
    cerebro.addstrategy(RLBacktraderStrategy)
    
    # Set initial capital
    cerebro.broker.setcash(10000.0)
    
    # Run backtest
    print("Starting Portfolio Value: %.2f" % cerebro.broker.getvalue())
    cerebro.run()
    print("Final Portfolio Value: %.2f" % cerebro.broker.getvalue())
    
    # Plot results
    cerebro.plot()

if __name__ == '__main__':
    run_backtest()
