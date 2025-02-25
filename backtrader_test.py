import backtrader as bt
import pandas as pd

class TestStrategy(bt.Strategy):
    params = (
        ('sma_period', 20),
    )

    def __init__(self):
        # Add SMA as a new data line
        self.sma = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.sma_period)
        
        # Add the SMA to cerebro's data feeds
        self.data.sma = self.sma
        
    def next(self):
        # Access both close and SMA values
        print(f"Close: {self.data.close[0]:.2f}, 20-SMA: {self.data.sma[0]:.2f}")

if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(TestStrategy)
    
    # Create a simple data feed
    df = pd.DataFrame({
        'datetime': pd.to_datetime(pd.date_range('2025-01-01', periods=30)),
        'close': [100 + i for i in range(30)]  # Prices from 100 to 129
    })
    df.set_index('datetime', inplace=True)
    data = bt.feeds.PandasData(dataname=df)
    
    cerebro.adddata(data)
    cerebro.run()
