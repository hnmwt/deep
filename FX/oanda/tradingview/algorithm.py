import datetime
import MetaTrader5 as mt5
import pandas as pd


mt5.initialize()
dt_now = datetime.datetime.now()
time_from = dt_now - datetime.timedelta(hours=3) # 3時間前の東京時間
time_to = dt_now
# 2020.01.10 00:00-2020.01.11 13:00 UTCでUSDJPY M15からバーを取得する
rates = mt5.copy_rates_range("USDJPY", mt5.TIMEFRAME_M15, time_from, time_to)

df = pd.DataFrame(rates)

df['time'] = pd.to_datetime(df['time'].astype(int), unit='s')  # unix→標準
df["time"] = df["time"] + pd.tseries.offsets.Hour(9)  # utc→9時間後

print(df)
print(df.info())

print(df['close'][-1:])
print(df[-1:])