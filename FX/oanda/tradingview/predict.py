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

    X_train_columns = len(df.columns) - 1  # 特徴量のカラム数
    df = df.loc[:, 'open':'time(weekday)']  # 全行 , 列名称(始まり):列名称(終わり)
    df = mm.fit_transform(df)  # 正規化
    X_train = df[-1:]  # 最終行のみ抜き出す

    X_train = np.array(X_train).reshape(1, X_train_columns, -1)  # 特徴量の形状(3次元)
    pred = model(X_train)  # 予測
    print("予測:", pred)

read_model(r'C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\model\GBPJPY_1h', df) # 1時間後の予測