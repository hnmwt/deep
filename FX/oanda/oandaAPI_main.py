import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import datetime
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.pricing as pricing
#numpy配列を省略しないようにする
np.set_printoptions(threshold=np.inf)

def DATE():
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%Y年%m月%d日 %H:%M:%S')
    print(dt_now)
    return dt_now

access_token_production = 'ff123428dffcc26c50a1991605df24b7-85946fa231df46d2ac24bf30e1e424b2'
accountID = '101-009-17604085-001'
access_token = '8f700c7d32cfa05988fede188bac48f0-72b3bcf05a1a02fbd487f05dc22e6a6e'  # デモ口座
api = API(access_token=access_token, environment='practice')

params = {
    "granularity": "M5",  # 取得する足 D=1日  M5=5分
    "count": 1,         # 取得する件数
    "price": "B",        # Bid (売り)
}

instrument = "USD_JPY"

def api_response(request): # リクエストをdef化
    api.request(request)
    response = request.response
    return response

def to_csv(f, name):
    df = pd.DataFrame(f)
    df.to_csv(name, mode='a', encoding='shift_jis', header=False)

def json_to_csv(json, name):
    df = pd.json_normalize(json)
    df.to_csv(name, mode='a' , encoding='shift_jis', header=False, index=False)

#  アカウント情報取得
AccountSummary_filename = '.\output\AccountSummary.csv'
def AccountSummary():
    account_summary = accounts.AccountSummary(accountID)  # アカウント情報取得
    response = api_response(account_summary)  # レスポンス送信
    json_to_csv(response, AccountSummary_filename)  # csv化

#  過去5分間の為替情報取得
InstrumentsCandles_filename = '.\output\instruments_candles.csv'
def InstrumentsCandles():
    instruments_candles = instruments.InstrumentsCandles(instrument=instrument, params=params)  # 為替情報取得
    response = api_response(instruments_candles)  # レスポンス送信
    json_to_csv(response['candles'], InstrumentsCandles_filename)  # csv化

# リアルタイムレート取得
PricingStream_filename = '.\output\pricing_stream.csv'
def PricingStream():
    pricing_stream = pricing.PricingStream(accountID=accountID, params=params)
    response = api_response(pricing_stream)  # レスポンス送信
    json_to_csv(response, PricingStream_filename)  # csv化

# 現在のオープンポジション取得
InstrumentsOrderBook_filename = '.\output\instruments_order_book.csv'
def InstrumentsOrderBook():
    instruments_order_book = instruments.InstrumentsOrderBook(instrument=instrument)
    response = api_response(instruments_order_book)  # レスポンス送信
    json_to_csv(response["orderBook"]["buckets"], InstrumentsOrderBook_filename)  # csv化

# 現在のオーダーポジション取得
InstrumentsPositionBook_filename = '.\output\instruments_position_book.csv'
def InstrumentsPositionBook():
    instruments_position_book = instruments.InstrumentsPositionBook(instrument=instrument)
    response = api_response(instruments_position_book)  # レスポンス送信
    json_to_csv(response["positionBook"]["buckets"], InstrumentsPositionBook_filename)  # csv化

# 現在のオーダーポジション取得データの整形
InstrumentsPositionBook_shaping_filename = '.\output\InstrumentsPositionBook_shaping.csv'
def InstrumentsPositionBook_shaping():
    df = pd.read_csv(InstrumentsPositionBook_filename, encoding='shift_jis', index_col=0)
    # longCountPercentとshortCountPercentを結合
    df_shape = pd.concat([df['shortCountPercent'], df['longCountPercent']])  # shortCountPercent,longCountPercentを1つの行に結合
    with open(InstrumentsPositionBook_shaping_filename ,mode='w' , encoding='shift_jis') as f:
        for row in df_shape:
            f.write(str(row) + ',')

#AccountSummary()
#InstrumentsCandles()
#PricingStream()
#InstrumentsOrderBook()
#InstrumentsPositionBook()

today = DATE()
InstrumentsPositionBook_shaping()


pd.read_csv(InstrumentsPositionBook_shaping_filename, encoding='shift_jis')
pd.read_csv(InstrumentsCandles_filename, encoding='shift_jis')

# ロング　= 買い
# ショート = 売り