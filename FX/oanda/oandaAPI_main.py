import pandas as pd
import numpy as np
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
#numpy配列を省略しないようにする
np.set_printoptions(threshold=np.inf)

access_token = 'ff123428dffcc26c50a1991605df24b7-85946fa231df46d2ac24bf30e1e424b2'
api = API(access_token=access_token, environment='live')


params = {
    "granularity": "D",  # 取得する足(day)
    "count": 50,         # 取得する足数
    "price": "B",        # Bid(売り)
}
instrument = "USD_JPY"   # 通貨ペア


instruments_candles = instruments.InstrumentsCandles(instrument=instrument, params=params)
api.request(instruments_candles)
response = instruments_candles.response

df =pd.DataFrame(response['candles'])
print(df.head())
df.to_csv('.\output\param.csv', encoding='shift_jis')