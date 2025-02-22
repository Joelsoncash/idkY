import backtrader as bt
import pandas as pd
import json

# Load configuration settings
with open('config/backtrader_config.json') as config_file:
    config = json.load(config_file)

# Create a subclass of bt.Strategy
class SampleStrategy(bt.Strategy):
    params = (
        ('sma_period', config['sma_period']),
    )

    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.sma_period)

    def next(self):
        if not self.position:
            if self.data.close[0] > self.sma[0]:
                self.buy()
        elif self.data.close[0] < self.sma[0]:
            self.sell()

def run_backtest():
    cerebro = bt.Cerebro()
    
    # Load historical data
    data = pd.read_csv('data/historical_data.csv', parse_dates=True, index_col='date')
    data_feed = bt.feeds.PandasData(dataname=data)

    cerebro.adddata(data_feed)
    cerebro.addstrategy(SampleStrategy)
    
    # Set initial cash
    cerebro.broker.setcash(config['initial_cash'])
    
    # Run the backtest
    cerebro.run()
    
    # Print final portfolio value
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

if __name__ == '__main__':
    run_backtest()