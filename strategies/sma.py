import backtrader as bt

class SMACross(bt.Strategy):
    params = (('fast', 9), ('slow', 21),)  # EMA 9/21 as per task

    def __init__(self):
        ema_fast = bt.ind.EMA(period=self.p.fast)
        ema_slow = bt.ind.EMA(period=self.p.slow)
        self.crossover = bt.ind.CrossOver(ema_fast, ema_slow)

    def next(self):
        size = max(1, int((self.broker.getvalue() * 0.02) / self.data.close[0]))
        if not self.position:
            if self.crossover > 0:
                self.buy(size=size)
        else:
            if self.crossover < 0:
                self.sell()