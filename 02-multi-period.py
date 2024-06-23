import datetime
import pandas_ta as ta
import pandas as pd

import plotly.express as px

from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover

df = pd.read_csv(
        "BTCUSDT-1m-2022-YTD.csv",
        usecols = [0,1,2,3,4],
        names = ["Date","Open","High","Low","Close"]
        )
df["Date"] = pd.to_datetime(df["Date"], unit="ms")
df.set_index("Date", inplace = True)
print(df)

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

returns = []
minutes_in_day = 24*60
for x in range(30*minutes_in_day, len(df)+1, minutes_in_day):

    bt = Backtest(df.iloc[x-30*minutes_in_day:x], 
            RsiOscillator, cash=10_000_000, commission=.002)

    stats = bt.run(upper_bound=75,lower_bound=25,rsi_window=23)

    print(stats["Return [%]"])
    returns.append(stats["Return [%]"])

fig = px.box(returns, points = "all")
fig.update_layout(
    xaxis_title="Strategy",
    yaxis_title="Returns (%)",
)
fig.show()

