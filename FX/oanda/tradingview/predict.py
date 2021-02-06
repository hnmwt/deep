import TradingView
import pandas as pd
import numpy as np
import datetime
#import tensorflow as tf
#from tensorflow import keras
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn import preprocessing
import matplotlib as mpl
import matplotlib.pyplot as plt

file_name = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview/1.csv"

train_data = r"C:\Users\hnmwt\PycharmProjects\deep\FX\oanda\tradingview/train_data.csv"

def create_train_data(file_name):
    df = pd.read_csv(file_name, encoding='shift_jis')
    df = df[-1:]  # 最終行のみ抜き出す
    df['time'] = pd.to_datetime(df['time']  )#, format='%Y-%m-%d-%A %H:%M:%S')  # 日付カラムを日付型に変換
    df['time(hour)'] = df['time'].dt.hour  # hourをデータに追加
    df['time(minute)'] = df['time'].dt.minute  # minuteをデータに追加
    df['time(weekday)'] = df['time'].dt.dayofweek  # minuteをデータに追加
    df.to_csv(train_data, index=False)
    print(df)

create_train_data(file_name)