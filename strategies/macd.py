import backtrader as bt
import backtrader.indicators as btind

class MACDStrategy(bt.Strategy):
    params = (('period_me1', 12), ('period_me2', 26), ('period_signal', 9),)

    def __init__(self):
        macd = btind.MACD(self.data.close,
                          period_me1=self.p.period_me1,
                          period_me2=self.p.period_me2,
                          period_signal=self.p.period_signal)
        self.macd_cross = btind.CrossOver(macd.macd, macd.signal)

    def next(self):
        if not self.position:
            if self.macd_cross > 0:
                self.buy()
        elif self.macd_cross < 0:
            self.sell()
