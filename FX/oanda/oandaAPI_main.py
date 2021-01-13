import  orderbook_column
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

# 現在のオーダーポジション取得
InstrumentsOrderBook_filename = '.\output\instruments_order_book.csv'
def InstrumentsOrderBook(instrument):
    instruments_order_book = instruments.InstrumentsOrderBook(instrument=instrument)
    response = api_response(instruments_order_book)  # レスポンス送信
    json_to_csv_mode_W(response["orderBook"]["buckets"], InstrumentsOrderBook_filename)  # csv化

# 現在のオーダーポジション取得のデータ整形
InstrumentsOrderBook_shaping_filename = '.\output\InstrumentsOrderBook_shaping.csv'
def InstrumentsOrderBook_shaping(column_list):  # 引数はオーダーポジションから行数決め打ち
    df = pd.read_csv(InstrumentsOrderBook_filename, encoding='shift_jis', index_col=0)

    min = column_list[0]  #dfのインデックスの最小値
    max = column_list[-1]  #dfのインデックスの最大値
    df_index_frame = pd.DataFrame(index=column_list, columns=[])  # dfのindexのみ作成
    df_new = pd.concat([df_index_frame, df], axis=1)  # インデックスとオーダーブックの結果を結合
    df_new = df_new.loc[min:max]  # 最小-最大までを抜き出す
    df_new = df_new.fillna(0)  # 欠損値を0に置換
    #df_new.to_csv(r'.\output\a.csv', encoding='shift_jis')
    with open(InstrumentsOrderBook_shaping_filename, mode='w', encoding='shift_jis') as f:
        for row in df_new['shortCountPercent']:
            f.write(str(row) + ',')
        for row in df_new['longCountPercent']:
            f.write(str(row) + ',')
        f.write('\n')

# 現在のオープンポジション取得
InstrumentsPositionBook_filename = '.\output\instruments_position_book.csv'
def InstrumentsPositionBook(instrument):
    instruments_position_book = instruments.InstrumentsPositionBook(instrument=instrument)
    response = api_response(instruments_position_book)  # レスポンス送信
    json_to_csv_mode_W(response["positionBook"]["buckets"], InstrumentsPositionBook_filename)  # csv化

# 現在のオープンポジション取得データの整形
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
    with open(InstrumentsPositionBook_shaping_filename, mode='r', encoding='shift_jis') as f: # ポジションデータ
        with open(InstrumentsCandles_filename, mode='r', encoding='shift_jis', ) as ff:  # ロウソク足データ
            with open(InstrumentsOrderBook_shaping_filename, mode='r', encoding='shift_jis', ) as fff: # オーダーデータ
                row = f.readline()  # 文字列でファイル読み込み
                row1 = ff.readlines()[1]  # 文字列でファイル読み込み
                row2 = fff.readline()  # 文字列でファイル読み込み
                row = row.rstrip()
                row1 = row1.rstrip()
                row2 = row2.rstrip()
                join = today+ ',' + row + row2 +row1 # 文字列結合

                with open(filepath, mode='a', encoding='shift_jis') as wf:
                    wf.write(join)
                    wf.write('\n')

#**********************lineチャットボット***************
line_notify_token = '2uRCEknoPXNnyy7PVPpBJDIxqXdnkSepWvErkVql0YC'  # lineチャットボット
line_notify_api = 'https://notify-api.line.me/api/notify'  # lineチャットボット
def Line_bot(message):  # lineチャットボット
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)
#**********************lineチャットボット***************

USD_JPY_order = orderbook_column.USD_JPY_order
GBP_JPY_order = orderbook_column.GBP_JPY_order

i = 0
while True:
    try:
        AccountSummary()
        today = DATE()

        # 過去5分のデータ収集
        InstrumentsCandles("USD_JPY", "M5")  # 過去5分のUSD_JPYのデータ取得
        #PricingStream()
        InstrumentsOrderBook("USD_JPY")  # 現在のオーダーデータ
        InstrumentsOrderBook_shaping(USD_JPY_order)  # 現在のオーダーデータ整形
        InstrumentsPositionBook("USD_JPY")  # 現在のポジションデータ
        InstrumentsPositionBook_shaping()   # 現在のポジションデータ整形
        train_data_create(today, r".\shape\USD_JPY_X_train_data.csv")  # USD_JPYのトレーニングデータ作成

        # 過去5分のデータ収集
        InstrumentsCandles("GBP_JPY", "M5")  # 過去5分のGBP_JPYのデータ取得
        #PricingStream()
        InstrumentsOrderBook("GBP_JPY")  # 現在のオーダーデータ
        InstrumentsOrderBook_shaping(GBP_JPY_order)  # 現在のオーダーデータ整形
        InstrumentsPositionBook("GBP_JPY")  # 現在のポジションデータ
        InstrumentsPositionBook_shaping()  # 現在のポジションデータ整形
        train_data_create(today, r".\shape\GBP_JPY_X_train_data.csv")  # GBP_JPYのトレーニングデータ作成
        print(today, '5min:DataCreate')


        # 4時間毎にポジションデータ、ローソク足取得
        if i % 48 == 0:  # 4時間 = 5分×12回×4(時間)
            # 4時間毎のポジションデータ、ローソク足
            InstrumentsCandles("USD_JPY", "H4")  # 過去5分のGBP_JPYのデータ取得
            # PricingStream()
            InstrumentsOrderBook("USD_JPY")
            InstrumentsOrderBook_shaping(USD_JPY_order)  # 現在のオーダーデータ整形
            InstrumentsPositionBook("USD_JPY")  # 現在のポジションデータ
            InstrumentsPositionBook_shaping()  # 現在のポジションデータ整形
            train_data_create(today, r".\shape\4H_USD_JPY_X_train_data.csv")  # GBP_JPYのトレーニングデータ作成

            # 4時間毎のポジションデータ、ローソク足
            InstrumentsCandles("GBP_JPY", "H4")  # 過去5分のGBP_JPYのデータ取得
            # PricingStream()
            InstrumentsOrderBook("GBP_JPY")
            InstrumentsOrderBook_shaping(GBP_JPY_order)  # 現在のオーダーデータ整形
            InstrumentsPositionBook("GBP_JPY")  # 現在のポジションデータ
            InstrumentsPositionBook_shaping()  # 現在のポジションデータ整形
            train_data_create(today, r".\shape\4H_GBP_JPY_X_train_data.csv")  # GBP_JPYのトレーニングデータ作成
            print(today, '5hour:DataCreate')
        i += 1
        time.sleep(300)

    except:
        Line_bot('エラーが発生しました。')
        time.sleep(60)  # 60秒待って繰り返しに戻る
# ロング　= 買い
# ショート = 売り