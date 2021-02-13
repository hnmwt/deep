#import TradingView
import pandas as pd
import numpy as np
import datetime
import tensorflow as tf
from tensorflow import keras
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import preprocessing
import matplotlib as mpl
import matplotlib.pyplot as plt
import pickle
import requests


get_csv_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview\FX_GBPJPY, 30.csv"

train_data_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview\train_data.csv"
mm = preprocessing.MinMaxScaler()  # 正規化エンコード、デコード
line_notify_token = '2uRCEknoPXNnyy7PVPpBJDIxqXdnkSepWvErkVql0YC'  # lineチャットボット
line_notify_api = 'https://notify-api.line.me/api/notify'  # lineチャットボット

pred30m = 0
pred8h = 0
pred16h = 0
pred24h = 0

# lineチャットボット
def Line_bot(message):
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)

# 特徴量データを取得
def create_train_data(file_name):
    df = pd.read_csv(file_name, encoding='shift_jis')
    #df = df[-1:]  # 最終行のみ抜き出す
    df['time'] = pd.to_datetime(df['time']  )#, format='%Y-%m-%d-%A %H:%M:%S')  # 日付カラムを日付型に変換
    df['time(hour)'] = df['time'].dt.hour  # hourをデータに追加
    df['time(minute)'] = df['time'].dt.minute  # minuteをデータに追加
    df['time(weekday)'] = df['time'].dt.dayofweek  # minuteをデータに追加
    df.to_csv(train_data_name, index=False)
    return df

def format(num):
    num = "{:.3f}".format(float(num))  # 書式編集
    return num

# モデルデータから未来のレートを予測
def read_model(dir, df, hour, column_start, column_end):
    model = keras.models.load_model(dir +'\model.hdf5')  # モデルを読込み
    model.load_weights(dir +'\param.hdf5')  # 重みを読込み
    #X_train_save_scaler = pickle.load(open('../dump/X_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    X_train_save_scaler = pickle.load(open(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview\dump\X_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    y_train_save_scaler = pickle.load(open(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview\dump\y_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    X_train_columns = len(df.columns) - 1  # 特徴量のカラム数

    time = df.iloc[column_start, 0]  # 時間を変数に代入して避難する
    df = df.loc[:, 'open':'time(weekday)']  # 全行 , 列名称(始まり):列名称(終わり)
    df = X_train_save_scaler.transform(df)  # 予測結果の正規化
    X_train = df#[column_start:column_end]  # 最終行から2番目のみ抜き出す

    X_train = np.array(X_train).reshape(-1, X_train_columns, 1)  # 特徴量の形状(3次元)
    pred = model(X_train)  # 予測
    pred = pred[column_start:column_end]
    pred = y_train_save_scaler.inverse_transform(pred)  # 予測結果の正規化をデコード
    pred = "{:.3f}".format(float(pred))  # 書式編集
    #print(time)
    after_time = time + datetime.timedelta(hours=hour+9+0.5)  # 日本時間を計算、30分足のデータのため予測値は29分59秒≒0.5時間
    after_time = "{0:%Y-%m-%d %H:%M}".format(after_time)

    pred_time = {str(after_time) : str(pred)}  # 時間、予測レートを辞書化
    return pred_time ,pred

# 前回の予測値を変数に格納
def last_pred():
    last_pred30m = pred30m
    last_pred8h = pred8h
    last_pred16h = pred16h
    last_pred24h = pred24h
    return last_pred30m, last_pred8h, last_pred16h, last_pred24h

# 前回の予測と今回の予測の差
def rate_diff():
    diff_30m = last_pred30m - pred30m
    diff_8h = last_pred8h - pred8h
    diff_16h = last_pred16h - pred16h
    diff_24h = last_pred24h - pred24h

# 24時間後までの予測
def pred(df, syukai_flag, pred30m):

    # 2週目以降は前回の予測値を変数に格納  ※処理1/2
    if syukai_flag == True:
        last_pred30m = pred30m
#        last_pred8h = pred8h
#        last_pred16h = pred16h
#        last_pred24h = pred24h

    dict_pred30m, pred30m = read_model('.\model\GBPJPY_30m', df, 0.5, -2, -1) # 0.5時間後の予測
#    pred2h = read_model('.\model\GBPJPY_2h', df, 2) # 2時間後の予測
#    pred3h = read_model('.\model\GBPJPY_3h', df, 3) # 3時間後の予測
#    pred4h = read_model('.\model\GBPJPY_4h', df, 4) # 4時間後の予測
#    pred5h = read_model('.\model\GBPJPY_5h', df, 5) # 5時間後の予測
#    pred6h = read_model('.\model\GBPJPY_6h', df, 6) # 6時間後の予測
#    pred7h = read_model('.\model\GBPJPY_7h', df, 7) # 7時間後の予測
#    dict_pred8h, pred8h = read_model('.\model\GBPJPY_8h', df, 8) # 8時間後の予測
#    pred9h = read_model('.\model\GBPJPY_9h', df, 9) # 9時間後の予測
#    pred10h = read_model('.\model\GBPJPY_10h', df, 10) # 10時間後の予測
#    pred130m = read_model('.\model\GBPJPY_130m', df, 11) # 11時間後の予測
#    pred12h = read_model('.\model\GBPJPY_12h', df, 12) # 12時間後の予測
#    pred13h = read_model('.\model\GBPJPY_13h', df, 13) # 13時間後の予測
#    pred14h = read_model('.\model\GBPJPY_14h', df, 14) # 14時間後の予測
#    pred15h = read_model('.\model\GBPJPY_15h', df, 15) # 15時間後の予測
#    dict_pred16h, pred16h = read_model('.\model\GBPJPY_16h', df, 16) # 16時間後の予測
#    pred17h = read_model('.\model\GBPJPY_17h', df, 17) # 17時間後の予測
#    pred18h = read_model('.\model\GBPJPY_18h', df, 18) # 18時間後の予測
#    pred19h = read_model('.\model\GBPJPY_19h', df, 19) # 19時間後の予測
#    pred20h = read_model('.\model\GBPJPY_20h', df, 20) # 20時間後の予測
#    pred230m = read_model('.\model\GBPJPY_230m', df, 21) # 21時間後の予測
#    pred22h = read_model('.\model\GBPJPY_22h', df, 22) # 22時間後の予測
#    pred23h = read_model('.\model\GBPJPY_23h', df, 23) # 23時間後の予測
#    dict_pred24h, pred24h = read_model('.\model\GBPJPY_24h', df, 24) # 24時間後の予測
#    Line_bot(str(pred30m) + '\n' + str(pred2h) + '\n' + str(pred3h) + '\n' + str(pred4h) + '\n' + str(pred5h) + '\n' + str(pred6h) + '\n' +
#             str(pred7h) + '\n' + str(pred8h) + '\n' + str(pred9h) + '\n' + str(pred10h) + '\n' + str(pred130m) + '\n' + str(pred12h) + '\n' +
#             str(pred13h) + '\n' + str(pred14h) + '\n' + str(pred15h) + '\n' + str(pred16h) + '\n' + str(pred17h) + '\n' + str(pred18h) + '\n' +
#             str(pred19h) + '\n' + str(pred20h) + '\n' + str(pred230m) + '\n' + str(pred22h) + '\n' + str(pred23h) + '\n' + str(pred24h))

    # 1週目に限り前回の予測も行う
    if syukai_flag == False:
        before_pred30m, before_pred_one30m = read_model('.\model\GBPJPY_30m', df, 0.5, -3, -2)  # 0.5時間後の予測
        Line_bot('前回の予測' + str(before_pred30m))
        print('前回の予測' + str(before_pred30m))
        diff_30m = 0  # 初回は0固定
    # 2週目以降は前回の予測と今回の予測の差を計算  ※処理2/2
    elif syukai_flag == True:
        diff_30m = float(pred30m) - float(last_pred30m)
        diff_30m = format(diff_30m)
#        diff_8h = float(pred8h) - float(last_pred8h)
#        diff_8h = format(diff_8h)
#        diff_16h = float(pred16h) - float(last_pred16h)
#        diff_16h = format(diff_16h)
#        diff_24h = float(pred24h) - float(last_pred24h)
#        diff_24h = format(diff_24h)
        Line_bot('\n30m差額' + str(diff_30m)
#                 + '\n8h差額' + str(diff_8h)
#                 + '\n16h差額' + str(diff_16h)
#                 + '\n24h差額' + str(diff_24h)
                 )
        print('\n30m差額' + str(diff_30m)
#              + '\n8h差額' + str(diff_8h)
#              + '\n16h差額' + str(diff_16h)
#              + '\n24h差額' + str(diff_24h)
              )


# 予測値のプリント
    Line_bot('\n30m' + str(dict_pred30m)
                 #             + '\n8h' + str(dict_pred8h)
                 #             + '\n16h' + str(dict_pred16h)
                 #             + '\n24h' + str(dict_pred24h)
                 )
    print('\n30m' + str(dict_pred30m)
              #         + '\n8h' + str(dict_pred8h)
              #         + '\n16h' + str(dict_pred16h)
              #         + '\n24h' + str(dict_pred24h)
              )

    syukai_flag = True
    return syukai_flag, pred30m, diff_30m

# デバッグ用
if __name__ == '__main__':
    syukai_flag = False
    while True:
        df = create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
        syukai_flag, pred30m, diff_30m = pred(df, syukai_flag, pred30m)
        print('完了')
        time.sleep(5)











