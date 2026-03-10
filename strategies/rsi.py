import backtrader as bt
import backtrader.indicators as btind

class RSIStrategy(bt.Strategy):
    params = (('period', 14), ('overbought', 70), ('oversold', 30),)

    def __init__(self):
        self.rsi = btind.RSI(self.data.close, period=self.p.period)

    def next(self):
        size = max(1, int((self.broker.getvalue() * 0.02) / self.data.close[0]))
        if not self.position:
            if self.rsi < self.p.oversold:
                self.buy(size=size)
        else:
            if self.rsi > self.p.overbought:
                self.sell()