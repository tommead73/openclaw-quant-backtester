import backtrader as bt
import backtrader.indicators as btind

class StochStrategy(bt.Strategy):
    params = (('period', 14), ('period_dfast', 3), ('period_dslow', 3), ('oversold', 20), ('overbought', 80),)

    def __init__(self):
        self.stoch = btind.Stochastic(self.data, period=self.p.period, period_dfast=self.p.period_dfast, period_dslow=self.p.period_dslow)
        self.k = self.stoch.lines.percK
        self.d = self.stoch.lines.percD

    def next(self):
        size = max(1, int((self.broker.getvalue() * 0.02) / self.data.close[0]))
        if not self.position:
            if self.k[0] < self.p.oversold and self.k[0] > self.d[0]:
                self.buy(size=size)
        else:
            if self.k[0] > self.p.overbought and self.k[0] < self.d[0]:
                self.sell()