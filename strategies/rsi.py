import backtrader as bt
import backtrader.indicators as btind

class RSIStrategy(bt.Strategy):
    params = (('period', 14), ('overbought', 70), ('oversold', 30),)

    def __init__(self):
        self.rsi = btind.RSI(self.data.close, period=self.p.period)

    def next(self):
        if not self.position:
            if self.rsi < self.p.oversold:
                self.buy()
        elif self.rsi > self.p.overbought:
            self.sell()
