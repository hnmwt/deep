import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import datetime
import time
import schedule
from oandapyV20 import API
import oandapyV20.endpoints.instruments as instruments
import oandapyV20.endpoints.accounts as accounts
import oandapyV20.endpoints.pricing as pricing
#numpy配列を省略しないようにする
np.set_printoptions(threshold=np.inf)

def DATE():
    dt_now = datetime.datetime.now()
    dt_now = dt_now.strftime('%Y-%m-%d-%A %H:%M:%S')
    print(dt_now)
    return dt_now

access_token_production = 'ff123428dffcc26c50a1991605df24b7-85946fa231df46d2ac24bf30e1e424b2'
accountID = '101-009-17604085-001'
access_token = '8f700c7d32cfa05988fede188bac48f0-72b3bcf05a1a02fbd487f05dc22e6a6e'  # デモ口座
api = API(access_token=access_token, environment='practice')


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
    df.to_csv(name, mode='a' , encoding='shift_jis', header=True, index=False)

def json_to_csv_mode_W(json, name):
    df = pd.json_normalize(json)
    df.to_csv(name, mode='w' , encoding='shift_jis', header=True, index=False)

#  アカウント情報取得
AccountSummary_filename = '.\output\AccountSummary.csv'
def AccountSummary():
    account_summary = accounts.AccountSummary(accountID)  # アカウント情報取得
    response = api_response(account_summary)  # レスポンス送信
    json_to_csv_mode_W(response, AccountSummary_filename)  # csv化

#  過去の為替情報取得
InstrumentsCandles_filename = '.\output\instruments_candles.csv'
def InstrumentsCandles(instrument, granularity):
    params = {
        "granularity": granularity,  # 取得する足 D=1日  M5=5分
        "count": 1,  # 取得する件数
        "price": "B",  # Bid (売り)
    }
    instruments_candles = instruments.InstrumentsCandles(instrument=instrument, params=params)  # 為替情報取得
    response = api_response(instruments_candles)  # レスポンス送信
    json_to_csv_mode_W(response['candles'], InstrumentsCandles_filename)  # csv化

# リアルタイムレート取得
PricingStream_filename = '.\output\pricing_stream.csv'
def PricingStream(instrument):
    pricing_stream = pricing.PricingStream(accountID=accountID, params=params)
    response = api_response(pricing_stream)  # レスポンス送信
    json_to_csv_mode_W(response, PricingStream_filename)  # csv化

# 現在のオープンポジション取得
InstrumentsOrderBook_filename = '.\output\instruments_order_book.csv'
def InstrumentsOrderBook(instrument):
    instruments_order_book = instruments.InstrumentsOrderBook(instrument=instrument)
    response = api_response(instruments_order_book)  # レスポンス送信
    json_to_csv_mode_W(response["orderBook"]["buckets"], InstrumentsOrderBook_filename)  # csv化

# 現在のオーダーポジション取得
InstrumentsPositionBook_filename = '.\output\instruments_position_book.csv'
def InstrumentsPositionBook(instrument):
    instruments_position_book = instruments.InstrumentsPositionBook(instrument=instrument)
    response = api_response(instruments_position_book)  # レスポンス送信
    json_to_csv_mode_W(response["positionBook"]["buckets"], InstrumentsPositionBook_filename)  # csv化

# 現在のオーダーポジション取得データの整形
InstrumentsPositionBook_shaping_filename = '.\output\InstrumentsPositionBook_shaping.csv'
def InstrumentsPositionBook_shaping():
    df = pd.read_csv(InstrumentsPositionBook_filename, encoding='shift_jis', index_col=0)
    # longCountPercentとshortCountPercentを結合
    df_shape = pd.concat([df['shortCountPercent'], df['longCountPercent']])  # shortCountPercent,longCountPercentを1つの行に結合
    with open(InstrumentsPositionBook_shaping_filename ,mode='w' , encoding='shift_jis') as f:
        for row in df_shape:
            f.write(str(row) + ',')
        f.write('\n')

# トレーニングデータ作成
def train_data_create(today, filepath):
    with open(InstrumentsPositionBook_shaping_filename, mode='r', encoding='shift_jis') as f:
        with open(InstrumentsCandles_filename, mode='r', encoding='shift_jis', ) as ff:
            row = f.readline()  # 文字列でファイル読み込み
            row1 = ff.readlines()[1]  # 文字列でファイル読み込み
            row = row.rstrip()
            row1 = row1.rstrip()
            join = today+ ',' + row + row1  # 文字列結合
            with open(filepath, mode='a', encoding='shift_jis') as wf:
                wf.write(join)
                wf.write('\n')

def job():
    InstrumentsCandles("GBP_JPY", "H4")  # 過去5分のGBP_JPYのデータ取得
    # PricingStream()
    # InstrumentsOrderBook()
    InstrumentsPositionBook("GBP_JPY")  # 現在のポジションデータ
    InstrumentsPositionBook_shaping()  # 現在のポジションデータ整形
    train_data_create(today, r".\shape\4H_GBP_JPY_X_train_data.csv")  # GBP_JPYのトレーニングデータ作成


i = 0
while True:
    AccountSummary()
    today = DATE()

    # 過去5分のデータ収集
    InstrumentsCandles("USD_JPY", "M5")  # 過去5分のUSD_JPYのデータ取得
    #PricingStream()
    #InstrumentsOrderBook()
    InstrumentsPositionBook("USD_JPY")  # 現在のポジションデータ
    InstrumentsPositionBook_shaping()   # 現在のポジションデータ整形
    train_data_create(today, r".\shape\USD_JPY_X_train_data.csv")  # USD_JPYのトレーニングデータ作成

    # 過去5分のデータ収集
    InstrumentsCandles("GBP_JPY", "M5")  # 過去5分のGBP_JPYのデータ取得
    #PricingStream()
    #InstrumentsOrderBook()
    InstrumentsPositionBook("GBP_JPY")  # 現在のポジションデータ
    InstrumentsPositionBook_shaping()  # 現在のポジションデータ整形
    train_data_create(today, r".\shape\GBP_JPY_X_train_data.csv")  # GBP_JPYのトレーニングデータ作成


    if i % 48 == 0:  # 4時間 = 5分×12回×4(時間)
        # 4時間毎のポジションデータ、ローソク足
        InstrumentsCandles("USD_JPY", "H4")  # 過去5分のGBP_JPYのデータ取得
        # PricingStream()
        # InstrumentsOrderBook()
        InstrumentsPositionBook("USD_JPY")  # 現在のポジションデータ
        InstrumentsPositionBook_shaping()  # 現在のポジションデータ整形
        train_data_create(today, r".\shape\4H_USD_JPY_X_train_data.csv")  # GBP_JPYのトレーニングデータ作成

        # 4時間毎のポジションデータ、ローソク足
        InstrumentsCandles("GBP_JPY", "H4")  # 過去5分のGBP_JPYのデータ取得
        # PricingStream()
        # InstrumentsOrderBook()
        InstrumentsPositionBook("GBP_JPY")  # 現在のポジションデータ
        InstrumentsPositionBook_shaping()  # 現在のポジションデータ整形
        train_data_create(today, r".\shape\4H_GBP_JPY_X_train_data.csv")  # GBP_JPYのトレーニングデータ作成
        print('4時間毎のデータ作成')


    i += 1
    time.sleep(300)

# ロング　= 買い
# ショート = 売り