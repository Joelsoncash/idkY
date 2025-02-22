class SampleStrategy(bt.Strategy):
    params = (
        ('short_window', 10),
        ('long_window', 30),
        ('stop_loss', 0.02),
        ('take_profit', 0.05),
    )

    def __init__(self):
        self.short_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.short_window)
        self.long_mavg = bt.indicators.SimpleMovingAverage(self.data.close, period=self.params.long_window)
        self.order = None

    def next(self):
        if self.order:
            return

        if self.short_mavg[0] > self.long_mavg[0]:
            if not self.position:
                self.order = self.buy()
        elif self.short_mavg[0] < self.long_mavg[0]:
            if self.position:
                self.order = self.sell()

    def notify_order(self, order):
        if order.status in [order.Completed]:
            self.order = None
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.order = None