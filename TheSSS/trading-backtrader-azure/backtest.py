from datetime import datetime
import backtrader as bt
import pandas as pd

class Backtest:
    def __init__(self, data_file, strategy, cash=10000, commission=0.001):
        self.data_file = data_file
        self.strategy = strategy
        self.cash = cash
        self.commission = commission
        self.cerebro = bt.Cerebro()

    def load_data(self):
        data = pd.read_csv(self.data_file, parse_dates=True, index_col='date')
        data_feed = bt.feeds.PandasData(dataname=data)
        self.cerebro.adddata(data_feed)

    def setup(self):
        self.cerebro.addstrategy(self.strategy)
        self.cerebro.broker.setcash(self.cash)
        self.cerebro.broker.setcommission(commission=self.commission)

    def run(self):
        self.load_data()
        self.setup()
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        self.cerebro.run()
        print('Ending Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

if __name__ == '__main__':
    from strategies.sample_strategy import SampleStrategy  # Adjust the import based on your strategy class name
    backtest = Backtest(data_file='data/historical_data.csv', strategy=SampleStrategy)
    backtest.run()