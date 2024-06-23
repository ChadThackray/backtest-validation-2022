import datetime
import pandas_ta as ta
import pandas as pd

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover

df = pd.read_csv(
        "BTCUSDT-1m-2022-08.csv",
        usecols = [0,1,2,3,4],
        names = ["Date","Open","High","Low","Close"]
        )
df["Date"] = pd.to_datetime(df["Date"], unit="ms")
df.set_index("Date", inplace = True)
print(df)

# Optimized parameters:
# lower_bound = 25
# upper_bound = 75
# rsi_window = 23
class RsiOscillator(Strategy):
    
    upper_bound = 25
    lower_bound = 75
    rsi_window = 23

    # Do as much initial computation as possible
    def init(self):
        self.rsi = self.I(ta.rsi, self.data.Close.s, length = self.rsi_window)

    # Step through bars one by one
    # Note that multiple buys are a thing here
    def next(self):

        if crossover(self.rsi, self.upper_bound):
            self.position.close()

        elif crossover(self.lower_bound, self.rsi):
            self.buy()

bt = Backtest(df, RsiOscillator, cash=10_000_000, commission=.002)
stats = bt.run(upper_bound=75,lower_bound=25,rsi_window=23)

"""
stats = bt.optimize(
        upper_bound = range(50,85,5),
        lower_bound = range(15,45,5),
        rsi_window = range(10,30,1),
        maximize=optim_func,
        #maximize='Win Rate [%]',
        constraint = lambda param: param.lower_bound < param.upper_bound)
"""

print(stats)
bt.plot()

