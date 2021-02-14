import pandas as pd
import numpy as np
import datetime
from tensorflow import keras
import time
import pickle

get_csv_name = r".\FX_GBPJPY, 30.csv"
train_data_name = r".\Intermediate\predict.py中間ファイル.csv"
pred_data_name = r".\Intermediate\predict.py予測ファイル.csv"

pred30m = 0
pred8h = 0
pred16h = 0
pred24h = 0

# 特徴量データを取得
def create_train_data(file_name):
    df = pd.read_csv(file_name, encoding='shift_jis')
    df = df.dropna()
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
    X_train_save_scaler = pickle.load(open(r'.\dump\X_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    y_train_save_scaler = pickle.load(open(r'.\dump\y_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み

    X_train_columns = len(df.columns) - 1  # 特徴量のカラム数を計算
    time = df.iloc[column_start, 0]        # 時間[行, 列]
    df = df.loc[:, 'open':'time(weekday)']  # [行 , 列名称(始まり):列名称(終わり)]
    df = X_train_save_scaler.transform(df)  # 予測結果の正規化
    X_train = df.copy()                           # 最終行から2番目のみ抜き出す

    X_train = np.array(X_train).reshape(-1, X_train_columns, 1)  # 特徴量の形状(3次元)
    pred = model(X_train)  # 予測
    pred = y_train_save_scaler.inverse_transform(pred)  # 予測結果の正規化をデコード

    a = pd.DataFrame(pred)
   # df['predict'] = int(a)
    a.to_csv(pred_data_name, index=False)

    pred = pred[column_start:column_end]  # 対象の行を抜き出す
    pred = "{:.3f}".format(float(pred))  # 書式編集
    after_time = time + datetime.timedelta(hours=hour+9+0.5)  # 日本時間を計算、30分足のデータのため予測値は29分59秒≒0.5時間
    after_time = "{0:%Y-%m-%d %H:%M}".format(after_time)
    pred_time = {str(after_time) : str(pred)}  # 時間、予測レートを辞書化


    return pred_time, pred, after_time

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

    dict_pred30m, pred30m, pred_after_time = read_model('.\model\GBPJPY_30m', df, 0.5, -2, -1) # 0.5時間後の予測

    # 1週目に限り前回の予測も行う
    if syukai_flag == False:
      #  before_pred30m, before_pred_one30m, pred_after_time = read_model('.\model\GBPJPY_30m', df, 0.5, -3, -2)  # 0.5時間後の予測
        diff_30m = 0  # 差額は初回は0固定

    # 2週目以降は前回の予測との差を求める
    elif syukai_flag == True:
        diff_30m = float(pred30m) - float(last_pred30m)
        diff_30m = format(diff_30m)

    syukai_flag = True
    return syukai_flag, pred30m, diff_30m, pred_after_time

# デバッグ用
if __name__ == '__main__':
    syukai_flag = False
    while True:
        df = create_train_data(get_csv_name)  # 取ってきたcsvからdfを作成
        syukai_flag, pred30m, diff_30m, pred_time = pred(df, syukai_flag, pred30m)
        print('完了')
        time.sleep(5)











