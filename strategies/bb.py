import backtrader as bt
import backtrader.indicators as btind

class BBStrategy(bt.Strategy):
    params = (('period', 20), ('devfactor', 2.0), ('squeeze_threshold', 0.04),)

    def __init__(self):
        self.bb = btind.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        self.mid = self.bb.lines.mid
        self.top = self.bb.lines.top
        self.bot = self.bb.lines.bot
        self.width = (self.top - self.bot) / self.mid
        self.squeeze = False

    def next(self):
        size = max(1, int((self.broker.getvalue() * 0.02) / self.data.close[0]))
        if self.width[0] < self.p.squeeze_threshold:
            self.squeeze = True
        if not self.position:
            if self.squeeze and self.data.close[0] > self.top[0]:
                self.buy(size=size)
                self.squeeze = False
        else:
            if self.data.close[0] < self.bot[0]:
                self.sell()