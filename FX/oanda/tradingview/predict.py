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


get_csv_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview\FX_GBPJPY, 60.csv"

train_data_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview/train_data.csv"
mm = preprocessing.MinMaxScaler()  # 正規化エンコード、デコード

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
df = create_train_data(get_csv_name)

# モデルデータから未来のレートを予測
def read_model(dir, df):
    model = keras.models.load_model(dir +'\model.hdf5')  # モデルを読込み
    model.load_weights(dir +'\param.hdf5')  # 重みを読込み
    X_train_save_scaler = pickle.load(open('../dump/X_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    y_train_save_scaler = pickle.load(open('../dump/y_train_scaler.sav', 'rb'))  # 正規化パラメータを読込み
    X_train_columns = len(df.columns) - 1  # 特徴量のカラム数

    df = df.loc[:, 'open':'time(weekday)']  # 全行 , 列名称(始まり):列名称(終わり)
    df = X_train_save_scaler.transform(df)  # 予測結果の正規化をデコード
    X_train = df[-1:]  # 最終行のみ抜き出す

    X_train = np.array(X_train).reshape(1, X_train_columns, -1)  # 特徴量の形状(3次元)
    pred = model(X_train)  # 予測
    pred = y_train_save_scaler.inverse_transform(pred)  # 予測結果の正規化をデコード
    print("予測:", pred)
    return pred

pred1h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_1h', df) # 1時間後の予測
pred2h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_2h', df) # 2時間後の予測
pred3h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_3h', df) # 3時間後の予測
pred4h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_4h', df) # 4時間後の予測
pred5h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_5h', df) # 5時間後の予測
pred6h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_6h', df) # 6時間後の予測
pred7h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_7h', df) # 7時間後の予測
pred8h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_8h', df) # 8時間後の予測
pred9h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_9h', df) # 9時間後の予測
pred10h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_10h', df) # 10時間後の予測
pred11h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_11h', df) # 11時間後の予測
pred12h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_12h', df) # 12時間後の予測
pred13h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_13h', df) # 13時間後の予測
pred14h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_14h', df) # 14時間後の予測
pred15h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_15h', df) # 15時間後の予測
pred16h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_16h', df) # 16時間後の予測
pred17h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_17h', df) # 17時間後の予測
pred18h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_18h', df) # 18時間後の予測
pred19h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_19h', df) # 19時間後の予測
pred20h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_20h', df) # 20時間後の予測
pred21h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_21h', df) # 21時間後の予測
pred22h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_22h', df) # 22時間後の予測
pred23h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_23h', df) # 23時間後の予測
pred24h = read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_24h', df) # 24時間後の予測

















