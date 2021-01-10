import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import json
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
from oandapyV20.endpoints.pricing import PricingStream
#numpy配列を省略しないようにする
np.set_printoptions(threshold=np.inf)

access_token_production = 'ff123428dffcc26c50a1991605df24b7-85946fa231df46d2ac24bf30e1e424b2'
accountID = '101-009-17604085-001'
access_token = '8f700c7d32cfa05988fede188bac48f0-72b3bcf05a1a02fbd487f05dc22e6a6e'  # デモ口座
api = API(access_token=access_token, environment='practice')

params = {
    "granularity": "M5",  # 取得する足 D=1日  M5=5分
    "count": 1,         # 取得する件数
    "price": "B",        # Bid (売り)
}
instrument = "USD_JPY"   # 通貨ペア

def api_response(request): # リクエストをdef化
    api.request(request)
    response = request.response
    return response

def to_csv(f, name):
    df = pd.DataFrame(f)
    df.to_csv(name, mode='a', encoding='shift_jis', header=False)

def json_to_csv(json, name):
    df = pd.json_normalize(json)
    df.to_csv(name, mode='a' , encoding='shift_jis', header=False)

#  アカウント情報取得
account_summary = accounts.AccountSummary(accountID)  # アカウント情報取得
response = api_response(account_summary)  # レスポンス送信
json_to_csv(response,'.\output\AccountSummary.csv')  # csv化

#  過去5分間の為替情報取得
instruments_candles = instruments.InstrumentsCandles(instrument=instrument, params=params)  # 為替情報取得
response = api_response(instruments_candles)  # レスポンス送信
json_to_csv(response['candles'], '.\output\instruments_candles.csv')  # csv化

# リアルタイムレート取得
pricing_stream = PricingStream(accountID, params)
response = api_response(account_summary)  # レスポンス送信
json_to_csv(response,'.\output\pricing_stream.csv')  # csv化

# 現在のオープンポジション取得
instruments_order_book = instruments.InstrumentsOrderBook(instrument=instrument,params=params)
response = api_response(account_summary)  # レスポンス送信
json_to_csv(response,'.\output\instruments_order_book.csv')  # csv化

# 現在のオーダーポジション取得
instruments_position_book = instruments.InstrumentsPositionBook(instrument=instrument,params=params)
response = api_response(account_summary)  # レスポンス送信
json_to_csv(response,'.\output\instruments_position_book.csv')  # csv化

print('終了')